import re, discord
from discord.ext import commands
#shoutout to LTom and Baku_Reshi for Emoji

CONFIG_PREFIX="/home/mint/yomiage"
# ************************************************
# add_word
# 辞書に文字を追加する
# ************************************************
def add_word(arg1, arg2, guildid):
    if str(arg1) != str(arg2):
        repeat = False
        with open(f'{CONFIG_PREFIX}/dic.txt', mode='r+') as f:
            d = f.readlines()
            f.seek(0)
            for i in d:
                wd = i.strip().split(',')
                if wd[0] == arg1 and wd[2] == guildid:
                    repeat = True
                if wd[0] != arg1 or wd[2] != guildid:
                    f.write(i)
            f.truncate()
        f.close()
    
        with open(f'{CONFIG_PREFIX}/dic.txt', mode='a') as f:
            f.write(arg1 + ',' + arg2 + ',' + guildid + '\n')    
        f.close()
        
        if repeat == True:
            #print('dic.txtで手直し：'+ arg1 + ',' + arg2 + ',' + guildid)    
            msg = (arg1 + 'を' + arg2 + ' として登録し直しました。')
            em = discord.Embed(title = "読み方変更", description = ("「" + arg1 + "」を「" + arg2 + "」として登録し直しました。"), color = 0xE67E22)
          
        else:    
            #print('dic.txtに書き込み：'+ arg1 + ',' + arg2 + ',' + guildid)    
            msg = (arg1 + '　を　' + arg2 + '　として登録しました。')
            em = discord.Embed(title = "読み方登録", description = ("「" + arg1 + "」を「" + arg2 + "」として登録しました。"), color = 0xE67E22)   
    else:  
        msg = ('同じ文字です。入れ直してください。')
        em = discord.Embed(title = "エラー", description = ("同じ文字です、入れ直してください。"), color = 0xE67E22)     
        
    return str(msg), em
    
# ************************************************
# delete_word
# 辞書から文字を削除する
# ************************************************   
def delete_word(arg1, guildid):
    deleted = False
    with open(f"{CONFIG_PREFIX}/dic.txt", "r+") as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            wd = i.strip().split(',')
            if wd[0] != arg1 or wd[2] != guildid:
                f.write(i)
            else:
                deleted = True
        f.truncate()
    f.close()
        
    if deleted == True:
        msg = (arg1 + ' の辞書登録を削除しました。')
        em = discord.Embed(title = "読み方削除", description = ("「" + arg1 + "」の辞書登録を削除しました。"), color = 0xE67E22)
    else:
        msg = ('その単語登録していません。')
        em = discord.Embed(title = "エラー", description = ("その単語登録していません。"), color = 0xE67E22)        
    
    return str(msg), em

# ************************************************
# delete_all_word
# 辞書から文字をすべて削除する
# ************************************************   
def delete_all_word(guildid):
    deleted = False
    with open(f"{CONFIG_PREFIX}/dic.txt", "r+", encoding = 'utf-8') as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            wd = i.strip().split(',')
            if wd[2] != guildid:
                f.write(i)
            else:
                deleted = True
        f.truncate()
    f.close()       
    
    if deleted == True:
        msg = ('すべての辞書登録を削除しました。')
        em = discord.Embed(title = "辞書削除", description = ("すべての辞書登録を削除しました。"), color = 0xE67E22)
    else:
        msg = ('辞書登録していません。')
        em = discord.Embed(title = "エラー", description = ("辞書登録していません。"), color = 0xE67E22)        
    
    return str(msg), em

# ************************************************
# add_server
# 読み上げてほしいサーバーを追加する
# ************************************************
def add_server(guildid,msgid,msgname):
    repeat =  False
    List = ('`' + msgname + '`')
    with open(f'{CONFIG_PREFIX}/server.txt', mode='r', encoding = 'utf-8') as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            wd = i.strip().split(',')
            if wd[0] == guildid and wd[1] == msgid:  
                repeat = True
                break
            elif wd[0] == guildid and wd[1] != msgid:
                try:
                    List = List + " \n`" + wd[2] + "`"
                except:
                    pass
    f.close()
    if  repeat == False:
        with open(f'{CONFIG_PREFIX}/server.txt', mode='a', encoding = 'utf-8') as f:
            f.write(guildid + ',' + msgid + ',' + msgname +'\n')
            #print('server.txtに書き込み：'+ guildid + ',' + msgid)    
        f.close()
        msg = ('次から'+ List +'を読み上げます。')
        em = discord.Embed(title = "読み上げるサーバーを登録", description = ("次からこのサーバーを読み上げます。"), color = 0xE67E22)
        em.add_field(name = "**読み上げるサーバーのリスト**", value = List)
    elif repeat == True:
        msg = ('このサーバーはもう登録してあります。')
        em = discord.Embed(title = "エラー", description = ("このサーバーはすでに登録してあります。"), color = 0xE67E22) 
    
    return str(msg), em

# ************************************************
# delete_server
# 読み上げてほしくないサーバーを追加する
# ************************************************
def delete_server(guildid,msgid):
    deleted = False
    with open(f"{CONFIG_PREFIX}/server.txt", "r+", encoding = 'utf-8') as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            wd = i.strip().split(',')
            if (wd[0] != guildid or wd[1] != msgid):
                f.write(i)
            else:
                deleted = True
        f.truncate()
    f.close()
    
    if deleted == True:
        #print('server.txtで削除：'+ guildid + ',' + msgid) 
        msg = ('次からこのサーバーを読み上げません。')
        em = discord.Embed(title = "読み上げるサーバーを削除", description = ("次からこのサーバーを読み上げません。"), color = 0xE67E22) 
    else:
        msg = ('このサーバーは登録してありません。')
        em = discord.Embed(title = "エラー", description = ("このサーバーは登録してありません。"), color = 0xE67E22)   
        
    return str(msg), em

# ************************************************
# delete_all_server
# サーバー全部削除
# ************************************************
def delete_all_server(guildid):
    with open(f"{CONFIG_PREFIX}/server.txt", "r+") as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            wd = i.strip().split(',')
            if (wd[0] != guildid):
                f.write(i)
            else:
                pass
        f.truncate()
    f.close()

# ************************************************
# settings_io
# ユーザーボイスの設定
# ************************************************
def settings_io(Username,Message_Author,arg1,arg2,arg3,arg4,arg5):
    repeat =  False
    Voice_List = False
    
    with open(f'i{CONFIG_PREFIX}/voice.txt', mode='r', encoding = 'utf-8') as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            wd = i.strip().split(',')
            if (wd[0] == arg1):
                Voice_List = True
                break
    f.close()

    if Voice_List == True:       
        if not (0 < float(arg2)):
            msg = ('その速度設定はできません。入れ直してください。')
            em = discord.Embed(title = "エラー", description = ("その速度設定はできません。入れ直してください。[0.0から]"), color = 0xE67E22)
        elif not (0 <= float(arg3)):
                msg = ('その重みの設定はできません。入れ直してください。')
                em = discord.Embed(title = "エラー", description = ("その重みの設定はできません。入れ直してください。[0.0から] (おすすめは0)"), color = 0xE67E22)
        elif not (0 <= float(arg4)) or not (float(arg4) <= 1):
                msg = ('そのフィルターの設定はできません。入れ直してください。')
                em = discord.Embed(title = "エラー", description = ("そのフィルターの設定はできません。入れ直してください。[0.0と1.0の間] (おすすめは0.5)"), color = 0xE67E22)
        else:
            with open(f'{CONFIG_PREFIX}/User.txt', mode='r+') as f:
                    d = f.readlines()
                    f.seek(0)
                    for i in d:
                        wd = i.strip().split(',')
                        if (wd[0] == Message_Author):
                            repeat = True
                        if (wd[0] != Message_Author):
                            f.write(i)
                    f.truncate()
            f.close()
                
            with open(f'{CONFIG_PREFIX}/User.txt', mode='a', encoding = 'utf-8') as f:
                f.write(Message_Author + ',' + arg1 + ',' + arg2 + ',' + arg3 + ',' + arg4 + ',' + arg5 + '\n')    
            f.close()    
            
            if repeat == True:
                #print('User.txtで手直し：'+ Message_Author + ',' + arg1 + ',' + arg2 + ',' + arg3 + ',' + arg4 + ',' + arg5)    
                msg = (Username + 'の声を以下の設定で登録し直しました。')
                em = discord.Embed(title = (Username + "の設定"), description = (Username + "の声の設定を変更しました。"), color = 0xE67E22)    
                em.add_field(name = "**声優**", value = arg1)
                em.add_field(name = "**速さ**", value = arg2)
                em.add_field(name = "**重み**", value = arg3)
                em.add_field(name = "**フィルター**", value = arg4)
                em.add_field(name = "**音程**", value = arg5)
                
            elif repeat == False:    
                #print('User.txtに書き込み：'+ Message_Author + ',' + arg1 + ',' + arg2 + ',' + arg3 + ',' + arg4 + ',' + arg5)
                msg = (Username + 'の声を以下の設定で登録しました。')
                em = discord.Embed(title = (Username + "の設定"), description = (Username + "の声の設定を足しました。"), color = 0xE67E22)    
                em.add_field(name = "**声優**", value = arg1)
                em.add_field(name = "**速さ**", value = arg2)
                em.add_field(name = "**重み**", value = arg3)
                em.add_field(name = "**フィルター**", value = arg4)
                em.add_field(name = "**音程**", value = arg5)
    else:
        msg = ('その声優さんはいません。入れ直してください。')
        em = discord.Embed(title = "エラー", description = ("その声優さんはいません。入れ直してください。"), color = 0xE67E22)    
            
    return str(msg), em

# ************************************************
# show_settings
# ユーザーボイスの設定の確認
# ************************************************
def show_settings(Username,Message_Author):
    repeat = False
    
    with open(f'{CONFIG_PREFIX}/User.txt', mode='r', encoding = 'utf-8') as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            wd = i.strip().split(',')
            if (wd[0] == Message_Author):
                repeat = True
                m  = wd[1] 
                r  = wd[2]
                jf = wd[3]
                a  = wd[4]
                fm = wd[5]
                break
    f.close()
    
    if repeat == True:
        msg = (Username + 'の声は以下の通りの設定です。')
        em = discord.Embed(title = (Username + "の設定!"), description = (Username + "の声の設定です。"), color = 0xE67E22)    
        em.add_field(name = "**声優**", value = m)
        em.add_field(name = "**速さ**", value = r)
        em.add_field(name = "**重み**", value = jf)
        em.add_field(name = "**フィルター**", value = a)
        em.add_field(name = "**音程**", value = fm)
    else:
        msg = (Username + 'の声は見つかりませんでした。')
        em = discord.Embed(title = "エラー", description = (Username + "の声は見つかりませんでした。"), color = 0xE67E22)   

    return str(msg), em 

# ************************************************
# Settings_username
# ユーザーネームの読み上げ
# ************************************************
def Settings_Username(guildid):
    with open(f'{CONFIG_PREFIX}/settings.txt', mode='r+', encoding = 'utf-8') as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            wd = i.strip().split(',')
            if (wd[0] == guildid):
                if (wd[1] == '0'):
                    Switch = 1
                elif (wd[1] == '1'):
                    Switch = 0
                Read_BotMessage = wd[2]
                Word_Limit = wd[3]
                Read_Emoji = wd[4]
                Read_Mention = wd[5]
                Read_Bot = wd[6]
            elif (wd[0] != guildid):
                f.write(i)
        f.truncate()
    f.close()
    
    with open(f'{CONFIG_PREFIX}/settings.txt', mode='a', encoding = 'utf-8') as f:
        f.write(guildid + ',' + str(Switch) + ',' + Read_BotMessage + ',' + Word_Limit + ',' + Read_Emoji + ',' + Read_Mention + ',' + Read_Bot + '\n') 
    f.close()
    
    if Switch == 0:
        msg = ('これからはユーザーネームを読み上げません。')
        em = discord.Embed(title = "ユーザーネーム読み上げの設定", description = ("これからはユーザーネームを読み上げません。"), color = 0xE67E22)  
    elif Switch == 1:         
        msg = ('これからはユーザーネームを読み上げます。')
        em = discord.Embed(title = ("ユーザーネーム読み上げの設定"), description = ("これからはユーザーネームを読み上げます。"), color = 0xE67E22)   
        
    return str(msg), em

# ************************************************
# botyomiage
# ボットの文章の読み上げ
# ************************************************
def botyomiage(guildid):
    with open(f'{CONFIG_PREFIX}/settings.txt', mode='r+', encoding = 'utf-8') as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            wd = i.strip().split(',')
            if (wd[0] == guildid):
                if (wd[2] == '0'):
                    Switch = 1
                elif (wd[2] == '1'):
                    Switch = 0
                Read_Username = wd[1]
                Word_Limit = wd[3]
                Read_Emoji = wd[4]
                Read_Mention = wd[5]
                Read_Bot = wd[6]
            elif (wd[0] != guildid):
                f.write(i)
        f.truncate()
    f.close()
    
    with open(f'{CONFIG_PREFIX}/settings.txt', mode='a') as f:
        f.write(guildid + ',' + Read_Username + ',' + str(Switch) + ',' + Word_Limit + ',' + Read_Emoji + ',' + Read_Mention + ',' + Read_Bot + '\n')  
    f.close()
    
    if Switch == 0:  
        msg = ('これからは読み上げエンジンの文章を読み上げません。')
        em = discord.Embed(title = "Yomiage文章読み上げの設定", description = ("これからはYomiage_Engineの文章を読み上げません。"), color = 0xE67E22)  
    elif Switch == 1:
        msg = ('これからは読み上げエンジンの文章を読み上げます。')
        em = discord.Embed(title = "Yomiage文章読み上げの設定", description = ("これからはYomiage_Engineの文章を読み上げます。"), color = 0xE67E22)
        
    return str(msg), em, Switch

# ************************************************
# Wordlimit
# 読み上げる文字数の上限
# ************************************************
def Wordlimit(guildid, arg1):
    if not (20 <= float(arg1)):
        msg = ('少ない文字数を設定はできません。入れ直してください。')
        em = discord.Embed(title = "エラー", description = ("少ない文字数を設定はできません。入れ直してください。[20から]"), color = 0xE67E22)
    else:
        with open(f'{CONFIG_PREFIX}/settings.txt', mode='r+', encoding = 'utf-8') as f:
            d = f.readlines()
            f.seek(0)
            for i in d:
                wd = i.strip().split(',')
                if (wd[0] == guildid):
                    Read_Username = wd[1]
                    Read_BotMessage = wd[2]
                    Read_Emoji = wd[4]
                    Read_Mention = wd[5]
                    Read_Bot = wd[6]
                elif (wd[0] != guildid):
                    f.write(i)
            f.truncate()
        f.close()
        
        with open(f'{CONFIG_PREFIX}/settings.txt', mode='a', encoding = 'utf-8') as f:
            f.write(guildid + ',' + Read_Username + ',' + Read_BotMessage + ',' + str(arg1) + ',' + Read_Emoji + ',' + Read_Mention + ',' + Read_Bot + '\n') 
        f.close()
        
        msg = ('これからは' + arg1 + '文字まで読み上げます。')
        em = discord.Embed(title = "読み上げる文字数", description = ("これからは" + arg1 + "文字まで読み上げます。"), color = 0xE67E22)     
        
    return str(msg), em 

# ************************************************
# reademoji
# 絵文字の文章の読み上げ
# ************************************************
def reademoji(guildid):
    with open(f'{CONFIG_PREFIX}/settings.txt', mode='r+', encoding = 'utf-8') as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            wd = i.strip().split(',')
            if (wd[0] == guildid):
                if (wd[4] == '0'):
                    Switch = 1
                elif (wd[4] == '1'):
                    Switch = 0
                Read_Username = wd[1]
                Read_BotMessage = wd[2]
                Word_Limit = wd[3]
                Read_Mention = wd[5]
                Read_Bot = wd[6]
            elif (wd[0] != guildid):
                f.write(i)
        f.truncate()
    f.close()
    
    with open(f'{CONFIG_PREFIX}/settings.txt', mode='a', encoding = 'utf-8') as f:
        f.write(guildid + ',' + Read_Username + ',' + Read_BotMessage + ',' + Word_Limit + ',' + str(Switch) + ',' + Read_Mention + ',' + Read_Bot + '\n')  
    f.close()
    
    if Switch == 0:  
        msg = ('これからは絵文字を読み上げません。')
        em = discord.Embed(title = "絵文字読み上げの設定", description = ("これからは絵文字を読み上げません。"), color = 0xE67E22)  
    elif Switch == 1:
        msg = ('これからは絵文字を読み上げます。')
        em = discord.Embed(title = "絵文字読み上げの設定", description = ("これからは絵文字を読み上げます。"), color = 0xE67E22)
        
    return str(msg), em

# ************************************************
# settings_mentions
# 絵文字の文章の読み上げ
# ************************************************
def settings_mentions(guildid):
    with open(f'{CONFIG_PREFIX}/settings.txt', mode='r+', encoding = 'utf-8') as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            wd = i.strip().split(',')
            if (wd[0] == guildid):
                if (wd[5] == '0'):
                    Switch = 1
                elif (wd[5] == '1'):
                    Switch = 0
                Read_Username = wd[1]
                Read_BotMessage = wd[2]
                Word_Limit = wd[3]
                Read_Emoji = wd[4]
                Read_Bot = wd[6]
            elif (wd[0] != guildid):
                f.write(i)
        f.truncate()
    f.close()
    
    with open(f'{CONFIG_PREFIX}/settings.txt', mode='a', encoding = 'utf-8') as f:
        f.write(guildid + ',' + Read_Username + ',' + Read_BotMessage + ',' + Word_Limit + ',' + Read_Emoji + ',' + str(Switch) + ',' + Read_Bot + '\n')  
    f.close()
    
    if Switch == 0:  
        msg = ('これからはメンションを読み上げません。')
        em = discord.Embed(title = "メンション読み上げの設定", description = ("これからはメンションを読み上げません。"), color = 0xE67E22)  
    elif Switch == 1:
        msg = ('これからはメンションを読み上げます。')
        em = discord.Embed(title = "メンション読み上げの設定", description = ("これからはメンションを読み上げます。"), color = 0xE67E22)
        
    return str(msg), em, Switch

# ************************************************
# settings_bot_message
# bot文章の読み上げ
# ************************************************
def settings_bot_message(guildid):
    with open(f'{CONFIG_PREFIX}/settings.txt', mode='r+', encoding = 'utf-8') as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            wd = i.strip().split(',')
            if (wd[0] == guildid):
                if (wd[6] == '0'):
                    Switch = 1
                elif (wd[6] == '1'):
                    Switch = 0
                Read_Username = wd[1]
                Read_BotMessage = wd[2]
                Word_Limit = wd[3]
                Read_Emoji = wd[4]
                Read_Mention = wd[5]
            elif (wd[0] != guildid):
                f.write(i)
        f.truncate()
    f.close()
    
    with open(f'{CONFIG_PREFIX}/settings.txt', mode='a', encoding = 'utf-8') as f:
        f.write(guildid + ',' + Read_Username + ',' + Read_BotMessage + ',' + Word_Limit + ',' + Read_Emoji + ',' + Read_Mention + ',' + str(Switch) + '\n')  
    f.close()
    
    if Switch == 0:  
        msg = ('これからは読み上げエンジン以外のボット文を読み上げません。')
        em = discord.Embed(title = "Bot読み上げの設定!", description = ("これからはYomiage_Engine以外のボット文を読み上げません。"), color = 0xE67E22)  
    elif Switch == 1:
        msg = ('これからは読み上げエンジン以外のボット文を読み上げます。')
        em = discord.Embed(title = "Bot読み上げの設定!", description = ("これからはYomiage_Engine以外のボット文を読み上げます。"), color = 0xE67E22)
        
    return str(msg), em, Switch

# ************************************************
# settings_prefixes
# ユーザーPrefixの変更
# ************************************************
def settings_prefixes(guildid, arg1, arg2, Default_Prefix):
    
    if str(arg1) == str(1) or str(arg1) == str(0):
        with open(f'{CONFIG_PREFIX}/prefixes.txt', 'r+', encoding = 'utf-8') as f:
            d = f.readlines()
            f.seek(0)
            for i in d:
                wd = i.strip().split(',')
                if (wd[0] != str(guildid)):
                    f.write(i)
            f.truncate()
        f.close()
        
        with open(f'{CONFIG_PREFIX}/prefixes.txt', mode='a', encoding = 'utf-8') as f:
            f.write(str(guildid) + ',' + str(arg1) + ',' + str(arg2) + '\n')
        f.close()
        
    if str(arg1) == str(0):
        em = discord.Embed(title = "Prefix", description = "Prefixを[" + arg2 + "]（スペースなし）として登録しました。\n(今まで通り「" + str(Default_Prefix) + "」でもできます。)", color = 0xE67E22)
        msg = ('Prefixを変更しました。(今まで通りのプレフェックスでもできます。)')
    elif str(arg1) == str(1):
        em = discord.Embed(title = "Prefix", description = "Prefixを[" + arg2 + " ]（スペースあり）として登録しました。\n(今まで通り「" + str(Default_Prefix) + "」でもできます。)", color = 0xE67E22)
        msg = ('Prefixを変更しました。(今まで通りのプレフェックスでもできます。)')
    else:
        em = discord.Embed(title = "エラー", description = "設定を間違えています。（Prefixの後にスペースを入れるかどうか、0か1で選んでください。）", color = 0xE67E22)
        msg = ('設定を間違えています。プレフェックスの後にスペースを入れるかどうか、0か1で選んでください。')
    
    return str(msg), em

# ************************************************
# get_custom_prefix
# ユーザーPrefixの習得
# ************************************************   
def get_custom_prefix(guildid, Default_Prefix):
    
    Read_Settings_Missing = True
    with open(f'{CONFIG_PREFIX}/prefixes.txt', mode='r', encoding = 'utf-8') as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            wd = i.strip().split(',')
            if (wd[0] == str(guildid)):
                Read_Settings_Missing = False
                space = wd[1]
                prefix = wd[2] 
                break
    f.close()
    if Read_Settings_Missing == True:
        with open(f'{CONFIG_PREFIX}/prefixes.txt', mode='a', encoding = 'utf-8') as f:
            f.write(str(guildid) + ',' + str(1) + ',' + str(Default_Prefix) + '\n')
        f.close()
        prefix = Default_Prefix
    
    if str(space) == str(1):
        prefix = str(str(prefix) + ' ')
    
    return prefix
    
# ************************************************
# remove_blacklist
# ユーザーPrefixの習得
# ************************************************   
def remove_blacklist(guildid, input):
    deleted = False
    with open(f"{CONFIG_PREFIX}/blacklist.txt", "r+", encoding = 'utf-8') as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            wd = i.strip().split(',')
            if wd[0] != str(guildid) or wd[1] != str(input):
                f.write(i)
            else:
                deleted = True
        f.truncate()
    f.close()
    
    if deleted == True:
        msg = (str(input) + 'をブラックリストから外しました。')
        em = discord.Embed(title = "エラー", description = (str(input) + "をブラックリストから外しました。"), color = 0xE67E22) 
    else:   
        msg = (str(input) + 'はもうブラックリストから外れています。')
        em = discord.Embed(title = "読み方登録！", description = (str(input) + "はもうブラックリストから外れています。"), color = 0xE67E22)
        
    return str(msg), em

# ************************************************
# add_blacklist
# ユーザーPrefixの習得
# ************************************************   
def add_blacklist(guildid, input):
    repeat = False
    with open(f'{CONFIG_PREFIX}/blacklist.txt', mode='r', encoding = 'utf-8') as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            wd = i.strip().split(',')
            if wd[0] == guildid and wd[1] == str(input):
                repeat = True
                break
    f.close()
    
    if repeat == True:
        msg = (str(input) + 'はもうブラックリストから登録されています。')
        em = discord.Embed(title = "エラー", description = (str(input) + "はもうブラックリストから登録されています。"), color = 0xE67E22) 
    else:   
        with open(f'{CONFIG_PREFIX}/blacklist.txt', mode='a', encoding = 'utf-8') as f:
            f.write(guildid + ',' + str(input) + '\n')    
        f.close()  
        msg = (str(input) + 'をブラックリストに登録しました。')
        em = discord.Embed(title = "読み方登録！", description = (str(input) + "をブラックリストに登録しました。"), color = 0xE67E22)
        
    return str(msg), em

# ************************************************
# check_blacklist
# ユーザーPrefixの習得
# ************************************************   
def check_blacklist(guildid, check):
    with open(f'{CONFIG_PREFIX}/blacklist.txt', mode='r', encoding = 'utf-8') as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            wd = i.strip().split(',')
            if wd[0] == str(guildid) and wd[1] == str(check):
                return True        
    f.close()
    
    return False
