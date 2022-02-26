import subprocess, re
from dictionary import romaji_trans, user_custom, Pick_Voice, Lowercase_trans
import discord
from discord.utils import get
    
CONFIG_PREFIX="/home/mint/yomiage"
# ************************************************
# remove_custom_emoji
# 絵文字IDは読み上げない
# ************************************************
def remove_custom_emoji(text, guildid):

    
    Read_Emoji_Settings = False
    with open(f'{CONFIG_PREFIX}/settings.txt', mode='r', encoding = 'utf-8') as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            wd = i.strip().split(',')
            if (wd[0] == guildid) and (wd[4] == '1'):
                Read_Emoji_Settings = True
                break
    f.close()
    
    if Read_Emoji_Settings == True:
        pattern = r'<a:'    # カスタム絵文字のパターン
        text = re.sub(pattern,'',text)   # 置換処理
        pattern = r'<:'    # カスタム絵文字のパターン
        text = re.sub(pattern,'',text)   # 置換処理
        pattern = r':[0-9]+>'    # カスタム絵文字のパターン 
        text = re.sub(pattern,'',text)   # 置換処理
        f = open('C:/open_jtalk/bin/emoji.txt', 'r', encoding="utf-8")
        line = f.readline()
        
        try:
            while line:
                pattern = line.strip().split(',')
                if pattern[0] in text:
                    text = text.replace(pattern[0], pattern[1])
                else:
                    line = f.readline()
        except:
            pass   
        f.close()
    else:
        pattern = r'<:[a-zA-Z0-9_]+:[0-9]+>'
        text = re.sub(pattern,'',text)   # 置換処理
        pattern = r'<a:[a-zA-Z0-9_]+:[0-9]+>'
        text = re.sub(pattern,'',text)   # 置換処理
        f = open('C:/open_jtalk/bin/emoji.txt', 'r', encoding="utf-8")
        line = f.readline()
        
        try:
            while line:
                pattern = line.strip().split(',')
                if pattern[0] in text:
                    text = text.replace(pattern[0], '')
                else:
                    line = f.readline()
        except:
            pass   
        f.close()
        
    emoji_pattern = re.compile("["
        u"\ufe0f"
        u"\U0001f3fb-\U0001f3ff"
        u"\U000000A1-\U000004FF"
        u"\U00002000-\U000025FF"
        u"\U00002600-\U000026FF"
        u"\U0001FB00-\U0001FBF9"
        "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    
    return text

# ************************************************
# Hear_Aid
# 聞きやすいように、変換
# ************************************************
def Hear_Aid(text):

    pattern = r'~'
    text = re.sub(pattern,'～',text)
    pattern = r'～'
    text = re.sub(pattern,'ー',text)
    pattern = r'…'
    return re.sub(pattern,',',text)

# ************************************************
# url_shouryaku
# URLなら省略
# ************************************************
def url_shouryaku(text):
    pattern = "https?:[//\w/:%#\$&\?\(\)~\.=\+\-]+"
    return re.sub(pattern,'URLは省略だよ！',text)   # 置換処理

# ************************************************
# remove_picture
# 画像ファイルなら読み上げない
# ************************************************
def remove_picture(text):
    pattern = r'.(\.jpg|\.jpeg|\.gif|\.png|\.bmp)'
    return re.sub(pattern,'',text)   # 置換処理

# ************************************************
# remove_enter
# ＠[\n]を外す機能　（アイルン
# ************************************************
def remove_enter(text):

     pattern = r'\n'
     return re.sub(pattern,'',text) # 置換処理

# ************************************************
# fuseji
# ||＜文字＞||は読まない　（アイルン
# ************************************************
def fuseji(text):
    
    pattern = re.compile('\|\|[u"\U00000000-\U0010FFFF"]+\|\|')
    return pattern.sub(r'伏せ字',text) # 置換処理

# ************************************************
# ikaryaku
# サーバーが指定した文字超える文を省略　（Shoutout to yhay81
# ************************************************
def ikaryaku(text, guildid):
    Word_Length = 0
    
    with open(f'{CONFIG_PREFIX}/settings.txt', mode='r', encoding = 'utf-8') as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            wd = i.strip().split(',')
            if (wd[0] == guildid):
                    Word_Length = int(wd[3])
                    break
    f.close()
    
    
    if len(text) > (int(Word_Length) + 5):
        text = text[:int(Word_Length)] + "。イカリャク"
    return text

# ************************************************
# readuser
# ユーザー名読み上げ
# ************************************************
def readuser(text, Username, guildid):
    Read_Username_Settings = False
    with open(f'{CONFIG_PREFIX}/settings.txt', mode='r', encoding = 'utf-8') as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            wd = i.strip().split(',')
            if (wd[0] == guildid) and (wd[1] == '1'):
                Read_Username_Settings = True
                break
    f.close()
    
    if Read_Username_Settings == True:
        text = (str(Username) + ", " + str(text))
    else:
        pass
        
    return text

# ************************************************
# creat_WAV
# message.contentをテキストファイルと音声ファイルに書き込む
# 引数：inputText
# 書き込みファイル：input.txt、output.wav
# ************************************************
def creat_WAV(inputText, Message_Author, Username, guildid, counter):
    # message.contentをテキストファイルに書き込み

    inputText = url_shouryaku(inputText)  # URLなら省略
    inputText = readuser(inputText, Username, guildid) # ユーザー名読み上げ
    # inputText = Lowercase_trans(inputText) # 大文字を小文字に書き換える
    inputText = fuseji(inputText) # ||＜文字＞||は読まない
    inputText = user_custom(inputText, guildid)   # ユーザ登録した文字を読み替える
    inputText = Hear_Aid(inputText) # ～からーの変換　（アイルン
    inputText = remove_picture(inputText)   # 画像なら読み上げない
    inputText = remove_enter(inputText) # [\n]を外す機能（アイルン
    inputText = romaji_trans(inputText) #ローマ字をひらがなに書き換える
    inputText = ikaryaku(inputText, guildid) # サーバーが指定した文字超える文を省略
    #inputText = remove_custom_emoji(inputText, guildid)   # 絵文字IDは読み上げない
    
    text_counter = (int(counter) % 2)
    
    if text_counter == 0:
        text_counter = 2
        
    input_file = "input" + str(text_counter) + ".txt"

    with open((f"{CONFIG_PREFIX}/"  + str(input_file)), 'w', errors = 'ignore') as file:
        file.write(inputText)
    
    command = '/usr/bin/open_jtalk -x {x} -m {m} -ow {ow} {input_file} -r {r} -jf {jf} -a {a} -fm {fm}'

    with open(f"{CONFIG_PREFIX}/User.txt", "r", encoding = 'utf-8') as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            wd = i.strip().split(',')
            if wd[0] == Message_Author:
                m  = wd[1]     #ボイス名 （ボイスファイルのPath）
                r  = wd[2]     #発声のスピード
                jf = wd[3]     #重み
                a  = wd[4]     #フィルター　（オールパス）
                fm = wd[5]     #音程
                break
    f.close()
                 
    #ボイス名→ボイスファイルのPath
    m  = Pick_Voice(m)
    
    #辞書のPath
    x = '/var/lib/mecab/dic/'

    #出力ファイル名　and　Path
    ow = "(" + str(counter) + ").wav"
    
    args={'x':x,'m':m,'ow': f'{CONFIG_PREFIX}/output/' + ow,'input_file': f"{CONFIG_PREFIX}/" + input_file,'r':r,'jf':jf,'a':a,'fm':fm}

    cmd= command.format(**args)
    cmd2 = cmd.split(" ")

    subprocess.run(cmd2)
    return inputText, counter

if __name__ == '__main__':
    creat_WAV('テスト','テスト','テスト','テスト','テスト')
