import re

CONFIG_PREFIX = "/home/mint/yomiage"
romaji = {
    'a': 'ア', 'i': 'イ', 'u': 'ウ', 'e': 'エ', 'o': 'オ',
    'ka': 'カ', 'ki': 'キ', 'ku': 'ク', 'ke': 'ケ', 'ko': 'コ',
    'sa': 'サ', 'shi': 'シ', 'su': 'ス', 'se': 'セ', 'so': 'ソ',
    'ta': 'タ', 'chi': 'チ', 'tu': 'ツ', 'te': 'テ', 'to': 'ト',
    'na': 'ナ', 'ni': 'ニ', 'nu': 'ヌ', 'ne': 'ネ', 'no': 'ノ',
    'ha': 'ハ', 'hi': 'ヒ', 'fu': 'フ', 'he': 'ヘ', 'ho': 'ホ',
    'ma': 'マ', 'mi': 'ミ', 'mu': 'ム', 'me': 'メ', 'mo': 'モ',
    'ya': 'ヤ', 'yu': 'ユ', 'yo': 'ヨ',
    'ra': 'ラ', 'ri': 'リ', 'ru': 'ル', 're': 'レ', 'ro': 'ロ',
    'wa': 'ワ', 'wo': 'ヲ', 'n': 'ン', 'vu': 'ヴ',
    'ga': 'ガ', 'gi': 'ギ', 'gu': 'グ', 'ge': 'ゲ', 'go': 'ゴ',
    'za': 'ザ', 'ji': 'ジ', 'zu': 'ズ', 'ze': 'ゼ', 'zo': 'ゾ',
    'da': 'ダ', 'di': 'ヂ', 'du': 'ヅ', 'de': 'デ', 'do': 'ド',
    'ba': 'バ', 'bi': 'ビ', 'bu': 'ブ', 'be': 'ベ', 'bo': 'ボ',
    'pa': 'パ', 'pi': 'ピ', 'pu': 'プ', 'pe': 'ペ', 'po': 'ポ',

    'kya': 'キャ', 'kyi': 'キィ', 'kyu': 'キュ', 'kye': 'キェ', 'kyo': 'キョ',
    'gya': 'ギャ', 'gyi': 'ギィ', 'gyu': 'ギュ', 'gye': 'ギェ', 'gyo': 'ギョ',
    'sha': 'シャ', 'shu': 'シュ', 'she': 'シェ', 'sho': 'ショ',
    'ja': 'ジャ', 'ju': 'ジュ', 'je': 'ジェ', 'jo': 'ジョ',
    'cha': 'チャ', 'chu': 'チュ', 'che': 'チェ', 'cho': 'チョ',
    'dya': 'ヂャ', 'dyi': 'ヂィ', 'dyu': 'ヂュ', 'dhe': 'デェ', 'dyo': 'ヂョ',
    'nya': 'ニャ', 'nyi': 'ニィ', 'nyu': 'ニュ', 'nye': 'ニェ', 'nyo': 'ニョ',
    'hya': 'ヒャ', 'hyi': 'ヒィ', 'hyu': 'ヒュ', 'hye': 'ヒェ', 'hyo': 'ヒョ',
    'bya': 'ビャ', 'byi': 'ビィ', 'byu': 'ビュ', 'bye': 'ビェ', 'byo': 'ビョ',
    'pya': 'ピャ', 'pyi': 'ピィ', 'pyu': 'ピュ', 'pye': 'ピェ', 'pyo': 'ピョ',
    'mya': 'ミャ', 'myi': 'ミィ', 'myu': 'ミュ', 'mye': 'ミェ', 'myo': 'ミョ',
    'rya': 'リャ', 'ryi': 'リィ', 'ryu': 'リュ', 'rye': 'リェ', 'ryo': 'リョ',
    'fa': 'ファ', 'fi': 'フィ', 'fe': 'フェ', 'fo': 'フォ',
    
    'va': 'ヴァ', 'vi': 'ヴィ', 've': 'ヴェ', 'vo': 'ヴォ',

    'kwa': 'クァ', 'kwi': 'クィ', 'kwu': 'クゥ', 'kwe': 'クェ', 'kwo': 'クォ',
    'kha': 'クァ', 'khi': 'クィ', 'khu': 'クゥ', 'khe': 'クェ', 'kho': 'クォ',
    'gwa': 'グァ', 'gwi': 'グィ', 'gwu': 'グゥ', 'gwe': 'グェ', 'gwo': 'グォ',
    'gha': 'グァ', 'ghi': 'グィ', 'ghu': 'グゥ', 'ghe': 'グェ', 'gho': 'グォ',
    'swa': 'スァ', 'swi': 'スィ', 'swu': 'スゥ', 'swe': 'スェ', 'swo': 'スォ',
    'zwa': 'ズヮ', 'zwi': 'ズィ', 'zwu': 'ズゥ', 'zwe': 'ズェ', 'zwo': 'ズォ',
    'twa': 'トァ', 'twi': 'トィ', 'twu': 'トゥ', 'twe': 'トェ', 'two': 'トォ',
    'dwa': 'ドァ', 'dwi': 'ドィ', 'dwu': 'ドゥ', 'dwe': 'ドェ', 'dwo': 'ドォ',
    'mwa': 'ムヮ', 'mwi': 'ムィ', 'mwu': 'ムゥ', 'mwe': 'ムェ', 'mwo': 'ムォ',
    'bwa': 'ビヮ', 'bwi': 'ビィ', 'bwu': 'ビゥ', 'bwe': 'ビェ', 'bwo': 'ビォ',
    'pwa': 'プヮ', 'pwi': 'プィ', 'pwu': 'プゥ', 'pwe': 'プェ', 'pwo': 'プォ',
    'phi': 'プィ', 'phu': 'プゥ', 'phe': 'プェ', 'pho': 'フォ',
        
    'wi': 'ウィ', 'we': 'ウェ', 'wb': 'ゥブ', 'wc': 'ゥク', 'wd': 'ゥド',
    'wf': 'ゥフ', 'wg': 'ゥグ', 'wh': 'ウ', 'wj': 'ゥジ', 'wk': 'ゥク', 
    'wl': 'ゥル', 'wm': 'ゥム', 'wn': 'ゥン', 'wp': 'ゥプ', 'wq': 'ゥク', 
    'wr': 'ウ', 'ws': 'ゥス', 'wt': 'ゥト', 'wu': 'ゥ', 'wv': 'ヴ', 
    'wx': 'ゥクス', 'wy': 'ゥィ', 'wz': 'ゥズ',
    
    'aw': 'アゥ', 'bw': 'ブゥ', 'cw': 'クゥ', 'dw': 'ドゥ', 'ew': 'ェウ', 
    'iw': 'イゥ', 'fw': 'フゥ', 'gw': 'グゥ', 'hw': 'フゥ', 'jw': 'ジゥ', 
    'kw': 'クヮ', 'lw': 'ルゥ', 'mw': 'ムゥ', 'nw': 'ンゥ', 'ow': 'ヲゥ', 
    'pw': 'プゥ', 'qw': 'クゥ', 'rw': 'ルゥ', 'sw': 'スゥ', 'tw': 'トゥ', 
    'uw': 'ゥ', 'vw': 'ヴ', 'xw': 'クス', 'yw': 'ィゥ', 'zw': 'ズゥ',
}

romaji_asist = {
    'si': 'シ', 'ti': 'チ', 'hu': 'フ', 'zi': 'ジ',
    'sya': 'シャ', 'syu': 'シュ', 'syo': 'ショ',
    'tya': 'チャ', 'tyu': 'チュ', 'tyo': 'チョ',
    'cya': 'チャ', 'cyu': 'チュ', 'cyo': 'チョ',
    'jya': 'ジャ', 'jyu': 'ジュ', 'jyo': 'ジョ', 'pha': 'ファ',
    'qa': 'クァ', 'qi': 'クィ', 'qu': 'クゥ', 'qe': 'クェ', 'qo': 'クォ',

    'ca': 'カ', 'ci': 'シ', 'cu': 'ク', 'ce': 'セ', 'co': 'コ',
    'la': 'ラ', 'li': 'リ', 'lu': 'ル', 'le': 'レ', 'lo': 'ロ',

    'mb': 'ム', 'py': 'パイ', 'tho': 'ソ', 'thy': 'ティ', 'oh': 'オウ',
    'by': 'ビィ', 'cy': 'シィ', 'dy': 'ディ', 'fy': 'フィ', 'gy': 'ジィ',
    'hy': 'シー', 'ly': 'リィ', 'ny': 'ニィ', 'my': 'ミィ', 'ry': 'リィ',
    'ty': 'ティ', 'vy': 'ヴィ', 'zy': 'ジィ',

    'b': 'ブ', 'c': 'ク', 'd': 'ド', 'f': 'フ', 'g': 'グ', 'h': 'フ', 'j': 'ジ',
    'k': 'ク', 'l': 'ル', 'm': 'ム', 'p': 'プ', 'q': 'ク', 'r': 'ル', 's': 'ス',
    't': 'ト', 'v': 'ヴ', 'w': 'わら', 'x': 'クス', 'y': 'ィ', 'z': 'ズ',
    
    'xtu': 'ッ', 'xa': 'ァ', 'xi': 'ィ', 'xu': 'ゥ', 'xe': 'ェ', 'xo': 'ォ',
}

Lowercase = {
    'A': 'a', 'B': 'b', 'C': 'c', 'D': 'd', 'E': 'e',
    'F': 'f', 'G': 'g', 'H': 'h', 'I': 'i', 'J': 'j',
    'K': 'k', 'L': 'l', 'M': 'm', 'N': 'n', 'O': 'o',
    'P': 'p', 'Q': 'q', 'R': 'r', 'S': 's', 'T': 't',
    'U': 'u', 'V': 'v', 'W': 'w', 'X': 'x', 'Y': 'y',
    'Z': 'z',
}
 
Lowercase_asist = {   
    'ａ': 'a', 'ｂ': 'b', 'ｃ': 'c', 'ｄ': 'd', 'ｅ': 'e',
    'ｆ': 'f', 'ｇ': 'g', 'ｈ': 'h', 'ｉ': 'i', 'ｊ': 'j',
    'ｋ': 'k', 'ｌ': 'l', 'ｍ': 'm', 'ｎ': 'n', 'ｏ': 'o',
    'ｐ': 'p', 'ｑ': 'q', 'ｒ': 'r', 'ｓ': 's', 'ｔ': 't',
    'ｕ': 'u', 'ｖ': 'v', 'ｗ': 'w', 'ｘ': 'x', 'ｙ': 'y',
    'ｚ': 'z',
    
    'Ａ': 'a', 'Ｂ': 'b', 'Ｃ': 'c', 'Ｄ': 'd','Ｅ': 'e', 
    'Ｆ': 'f', 'Ｇ': 'g', 'Ｈ': 'h', 'Ｉ': 'i','Ｊ': 'j',
    'Ｋ': 'k', 'Ｌ': 'l', 'Ｍ': 'm', 'Ｎ': 'n','Ｏ': 'o',
    'Ｐ': 'p', 'Ｑ': 'q', 'Ｒ': 'r', 'Ｓ': 's','Ｔ': 't',
    'Ｕ': 'u', 'Ｖ': 'v', 'Ｗ': 'w', 'Ｘ': 'x','Ｙ': 'y',
    'Ｚ': 'z', 
}

words = {
    'ok': 'オーケィ', 'bots': 'ボッズ', 'bot': 'ボット', 'discha': 'ディスチャ', 'microsoft': 'マイクロソフト',
    'google': 'グーグル', 'twitter': 'ツイッター','skype': 'スカイプ', 'mac': 'マック',
    'url':'ユーアルーエル', 'line':'ライン', 'instagram': 'インスタグラム', 'os': 'オーエス',
    'insta': 'インスタ', 'code': 'コード', 'mouse': 'マウス', 'keyboard': 'キーボード',
    'wiiu': 'ウィーユー', 'switch': 'スウィッチ', 'ps4': 'ピーエスフォー', '3ds': 'スリーディーエス',
    'minecraft': 'マインクラフト','omg':'オーエムジー', 'facebook':'フェイスブック', 'chrome':'クロム',
    'pokemon': 'ポケモン', 'edge': 'エッジ', 'drive': 'ドライブ', 'sd': 'エスディー', 'zoom':'ズーム',
    'adobe': 'アドベ', 'word':'ワード', 'excel':'エクセル', 'powerpoint':'パワーポイント', 'docs':'ドック',
    'doc':'ドック', 'slides': 'スライド', 'slide': 'スライド', 'spreadsheets': 'スプレッドシート',
    'spreadsheet': 'スプレッドシート', 'bing': 'ビング', 'yahoo': 'ヤフー','nice': 'ナイス',
    'good': 'グッド', 'job': 'ジョブ', 'bye': 'バーイ', 'welcome': 'ウェルカム', 'fantastic': 'ファンタジック',
    'book': 'ブック', 'laptop': 'ラップトップ', 'desktop': 'デスクトップ', 'notebook': 'ノートブック',
    'hello': 'ハロー', 'windows': 'ウインドウズ', 'window': 'ウインドウ', 'opera': 'オペラ', 'internet': 'インターネット',
    'explorer': 'エクスプローラー', 'gx': 'ジーエックス', 'vivaldi': 'ヴィダルディ', 'alpha': 'アルファ', 'beta': 'ベータ',
    'firefox': 'ファイアーフォックス', 'waterfox': 'ウオーターフォックス', 'palemoon': 'ペールムーン', 'brave': 'ブレーブ',
    'tor': 'トア', 'browser': 'ブラウザー', 'email': 'イーメール', 'chat': 'チャット', 'apple': 'アップル', 
    'android': 'アンドロイド', 'text': 'テキスト', 'teams': 'チームズ', 'team': 'チーム', 'store': 'ストア',
    'control': 'コントロール', 'panel': 'パネル', 'wifi': 'ワイファイ', 'wi-fi': 'ワイファイ', 'ms': 'ミリセカンズ',
    'pc': 'ピーシー', 'blacklist': 'ブラックリスト', 'whitelist': 'ホワイトリスト',
}

re_words = re.compile("|".join(map(re.escape, words.keys())))

romaji_dict = {}
for tbl in romaji, romaji_asist:
    for k, v in tbl.items():
        romaji_dict[k] = v

romaji_keys = romaji_dict.keys()
romaji_keys = sorted(romaji_keys, key=lambda x: len(x), reverse=True)

re_roma2kana = re.compile("|".join(map(re.escape, romaji_keys)))
rx_mba = re.compile("m(b|p)([aiueo])")
rx_xtu = re.compile(r"([bcdfghjklmpqrstvxyz])\1")
rx_a__ = re.compile(r"([aiueo])\1")

Lowercase_dict = {}
for tbl in Lowercase, Lowercase_asist:
    for k, v in tbl.items():
        Lowercase_dict[k] = v
        
Lowercase_keys = Lowercase_dict.keys()
Lowercase_keys = sorted(Lowercase_keys, key=lambda x: len(x), reverse=True)

re_Up2Low = re.compile("|".join(map(re.escape, Lowercase_keys)))
    
# ************************************************
# user_custom
# ユーザ登録した文字を読み替える
# ************************************************
def user_custom(text, guildid):

    f = open(f'{CONFIG_PREFIX}/dic.txt', 'r', encoding = 'utf-8')
    line = f.readline()
    
    while line:
        pattern = line.strip().split(',')
        if pattern[0] in text and pattern[2] == guildid:
            text = text.replace(pattern[0], pattern[1])
        else:
            line = f.readline()
    f.close()

    return text
    
# ************************************************
# Lowercase_trans (#zenkaku_trans)
# 大文字を小文字に書き換える （全角を半角にする役目もある）（Shoutout to yhay81
# ************************************************
def Lowercase_trans(text):
    return re_Up2Low.sub(lambda x: Lowercase_dict[x.group(0)], text)

# ************************************************
# romaji_trans
# ローマ字をひらがなに書き換える （Shoutout to yhay81
# ************************************************
def romaji_trans(text):    
    text = text.lower()
    text = re_words.sub(lambda x: words[x.group(0)], text)
    text = rx_mba.sub(r"ン\1\2", text)
    text = rx_xtu.sub(r"ッ\1", text)
    text = rx_a__.sub(r"\1ー", text)
    text = re.sub(r'(?i)discord', "ディスコード", text)
    text = re.sub(r'<:.*>', " ", text)
    return re_roma2kana.sub(lambda x: romaji_dict[x.group(0)], text)

# ************************************************
# Pick_Voice
# ボイス名→ボイスファイルのPath
# 引数：m
# ************************************************
def Pick_Voice(Koe):
    switcher = {
        'man'          : '/usr/share/hts-voice/hts_voice_nitech_jp_atr503_m001-1.05/nitech_jp_atr503_m001.htsvoice',
        'woman'        : '/usr/share/hts_voice/mei/mei_normal.htsvoice',
        'mei_angry'    : '/usr/share/hts_voice/mei/mei_angry.htsvoice',
        'mei_bashful'  : '/usr/share/hts_voice/mei/mei_bashful.htsvoice',
        'mei_happy'    : '/usr/share/hts_voice/mei/mei_happy.htsvoice',
        'mei_sad'      : '/usr/share/hts_voice/mei/mei_sad.htsvoice',
        'tohoku'       : '/usr/share/hts_voice/htsvoice-tohoku-f01-master/tohoku-f01-neutral.htsvoice',
        'tohoku_angry' : '/usr/share/hts_voice/htsvoice-tohoku-f01-master/tohoku-f01-angry.htsvoice',
        'tohoku_happy' : '/usr/share/hts_voice/htsvoice-tohoku-f01-master/tohoku-f01-happy.htsvoice',
        'tohoku_sad'   : '/usr/share/hts_voice/htsvoice-tohoku-f01-master/tohoku-f01-sad.htsvoice',
        'ai'           : '/usr/share/hts_voice/遠藤愛.htsvoice',
        'fuuki'        : '/usr/share/hts_voice/薪宮風季.htsvoice',
        'giruko'       : '/usr/share/hts_voice/カマ声ギル子.htsvoice',
        'homu'         : '/usr/share/hts_voice/沙音ほむ.htsvoice',
        'ikuru'        : '/usr/share/hts_voice/想音いくる.htsvoice',
        'ikuto'        : '/usr/share/hts_voice/想音いくと.htsvoice',
        'kanata'       : '/usr/share/hts_voice/空唄カナタ.htsvoice',
        'kono'         : '/usr/share/hts_voice/句音コノ。.htsvoice',
        'mai'          : '/usr/share/hts_voice/白狐舞.htsvoice',
        'matsuo'       : '/usr/share/hts_voice/松尾P.htsvoice',
        'nero'         : '/usr/share/hts_voice/蒼歌ネロ.htsvoice',
        'niji'         : '/usr/share/hts_voice/なないろニジ.htsvoice',
        'otoko'        : '/usr/share/hts_voice/20代男性01.htsvoice',
        'rakan'        : '/usr/share/hts_voice/戯歌ラカン.htsvoice',
        'riyon'        : '/usr/share/hts_voice/天月りよん.htsvoice',
        'rou'          : '/usr/share/hts_voice/獣音ロウ.htsvoice',
        'sou'          : '/usr/share/hts_voice/能民音ソウ.htsvoice',
        'wamea'        : '/usr/share/hts_voice/飴音わめあ.htsvoice',
        'watashi'      : '/usr/share/hts_voice/ワタシ.htsvoice',
        'yoe'          : '/usr/share/hts_voice/唱地ヨエ.htsvoice',
        'hitori'       : '/usr/share/hts_voice/遊音一莉.htsvoice',
        'sakura'       : '/usr/share/hts_voice/闇夜桜_1.0.htsvoice',
        'koto'         : '/usr/share/hts_voice/誠音コト.htsvoice',
        'akesato'      : '/usr/share/hts_voice/緋惺.htsvoice',
        'mizuki'       : '/usr/share/hts_voice/瑞歌ミズキ_Talk.htsvoice',
        'momo'         : '/usr/share/hts_voice/桃音モモ.htsvoice',
        'rami'         : '/usr/share/hts_voice/月音ラミ_1.0.htsvoice',
        'shiba'        : '/usr/share/hts_voice/和音シバ.htsvoice',
        'kaoru'        : '/usr/share/hts_voice/京歌カオル.htsvoice',
        'suranki'      : '/usr/share/hts_voice/スランキ.htsvoice',
        'gurimarukin'  : '/usr/share/hts_voice/グリマルキン_1.0.htsvoice',                                          
    }

    return switcher.get(Koe, "Error")
