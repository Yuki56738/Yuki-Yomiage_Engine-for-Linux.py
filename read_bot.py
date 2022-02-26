import discord, asyncio, os, subprocess, ffmpeg, time, sys, re, math # Shoutout to Nemu_zz for base of this code!
from discord.ext import commands
from discord.ext.commands import cooldown
from discord.ext.commands.cooldowns import BucketType
from discord.utils import get
from voice_generator import creat_WAV
from i_o import add_server, add_word, delete_word, delete_server, \
                delete_all_server, settings_io, show_settings, \
                Settings_Username, botyomiage, reademoji, Wordlimit, \
                settings_mentions, delete_all_word, settings_bot_message, \
                settings_prefixes, get_custom_prefix, add_blacklist, \
                remove_blacklist, check_blacklist
from dictionary import Lowercase_trans
from return_token import return_token


#----- DO NOT TOUCH ABOVE THIS ------- 上のコードをいじるな！（壊れるよ！）-----------------

### Default_Prefixは空白入れろ
Default_Prefix = ".yomi " #コマンドの設定　（例："!yomi " ">" "$$" など） 
Bot_Key = return_token()
Bot_Author = "@Yuki__Trans"
CONFIG_PREFIX="/home/mint/yomiage"


#----- DO NOT TOUCH BELOW THIS ------- 下のコードをいじるな！（壊れるよ！）-----------------



settings = {} #checkbotread = int(wd[2]) and checkmentionread = int(wd[5])
last_textch_id = {}
vcconnected = {}
queues = {}
first_check = {}
custom_prefix = {}
Leave_Message = '接続解除がコマンド来たので切ります。ありがとうございました。'
global client_name
global client_id
global counter

def get_prefix(client,message):
    if message.content.startswith(Default_Prefix):
        return Default_Prefix
    else:
        global custom_prefix
        try:
            try:
                prefix = custom_prefix[message.guild.id]
                return prefix[0]
            except:
                custom_prefix[message.guild.id] = [get_custom_prefix(message.guild.id, Default_Prefix)]
                prefix = custom_prefix[message.guild.id]
                return prefix[0]
        except:
            pass
        
intents = discord.Intents.all()
client = commands.Bot(command_prefix = get_prefix, intents = intents) #コマンドの頭、読み飛ばしの頭でもあるよ～ (Shoutout to baku_reshi)
client.remove_command("help")
voice_client = None

@client.event
async def on_ready(): #ログイン
    global client_id
    global client_name
    global counter
    Bot_User_Setting_Missing = True
    counter = 0
    client_id = str(client.user.id)
    client_name = str(client.user.name)
    print('------------------------------')
    await client.change_presence(status=discord.Status.online, activity=discord.Game(Default_Prefix + "helpで説明書。"))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    
    with open(f'{CONFIG_PREFIX}/User.txt', mode='r', encoding = 'utf-8') as f:
                d = f.readlines()
                f.seek(0)
                for i in d:
                    wd = i.strip().split(',')
                    if (wd[0] == client_id):
                        Bot_User_Setting_Missing = False
                        break
    f.close()
                  
    if Bot_User_Setting_Missing == True:
        with open(f'{CONFIG_PREFIX}/User.txt', mode='a', encoding = 'utf-8') as f:
            f.write(client_id + ',' + 'woman,1.75,0,0.5,0' + '\n')         
        f.close() 
    print('------------------------------')
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@client.group(invoke_without_command=True)
@cooldown(1, 5, BucketType.user)
async def help(ctx): #操作説明
    try:
        await ctx.message.delete()
    except:
        pass
    em = discord.Embed(title = "操作説明", description = str(Default_Prefix) + "help <command>で詳細説明が調べられます。", color = 0xE67E22)
    em.add_field(name = "help", value = "help　←「今はここ」 \nsettings (setting)　\ntroubleshoot (ts) \nvoicelist (vl)")
    em.add_field(name = "commands", value = "hello (join)(start)(s)(connect) \nbye (leave)(disconnect)(dc)(end)(e) \nreboot (rb) \nmove (m) \naddword (aw) \ndeleteword (dw) \naddserver (as) \ndeleteserver (ds)")
    em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed = em, delete_after=10)    
    await ctx.author.send(embed = em)
    s = settings[ctx.guild.id]
    if s[0] == 1:
        await Play_WAV(ctx,'ヘルプ画面です、ここでコマンド覚えてください。',client_id,client_name, str(ctx.guild.id))

@help.command(aliases=['vl'])
@cooldown(1, 5, BucketType.user)
async def voicelist(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    em = discord.Embed(title = "voicelist", description = "声優さんのリストが見ることができます、しかし長いので気をつけてください。", color = 0xE67E22)
    em.add_field(name = "**やり方　(syntax)**", value = str(Default_Prefix) + "voicelist (もしくは" + str(Default_Prefix) + "vl)")
    em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
    await ctx.send(embed = em, delete_after=5)
    s = settings[ctx.guild.id]
    if s[0] == 1:
        await Play_WAV(ctx,'声優さんのリストが見ることができます、しかし長いので気をつけてください。',client_id,client_name, str(ctx.guild.id))
    
@help.command(aliases=['ts'])
@cooldown(1, 5, BucketType.user)
async def troubleshoot(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    em = discord.Embed(title = "troubleshoot", description = "もしYomiage_Engineが動かなくなったときにはこれで試してください。", color = 0xE67E22)
    em.add_field(name = "**やり方　(syntax)**", value = str(Default_Prefix) + "troubleshoot (もしくは" + str(Default_Prefix) + "ts)")
    em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
    await ctx.send(embed = em, delete_after=5)
    s = settings[ctx.guild.id]
    if s[0] == 1:
        await Play_WAV(ctx,'もし読み上げエンジンが動かなくなったときにはこれで試してください。',client_id,client_name, str(ctx.guild.id))

@help.command()
@cooldown(1, 5, BucketType.user)
async def ping(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    em = discord.Embed(title = "ping", description = "Yomiage_Engineの反応時間を調べます。", color = 0xE67E22)
    em.add_field(name = "**やり方　(syntax)**", value = str(Default_Prefix) + "ping")
    await ctx.send(embed = em, delete_after=5)
    s = settings[ctx.guild.id]
    if s[0] == 1:
        await Play_WAV(ctx,'読み上げエンジンの反応時間を調べます。',client_id,client_name, str(ctx.guild.id)) 

@help.command(aliases=['join','start','connect','call','s'])
@cooldown(1, 5, BucketType.user)
async def hello(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    em = discord.Embed(title = "hello", description = "Yomiage_Engineを呼びます。", color = 0xE67E22)
    em.add_field(name = "**やり方　(syntax)**", value =  str(Default_Prefix) + "hello (もしくは" + str(Default_Prefix) + "join," + str(Default_Prefix) + "connect," + str(Default_Prefix) + "call," + str(Default_Prefix) + "s)")
    em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
    await ctx.send(embed = em, delete_after=5)
    s = settings[ctx.guild.id]
    if s[0] == 1:
        await Play_WAV(ctx,'読み上げエンジンを呼べます。',client_id,client_name, str(ctx.guild.id))  
    
@help.command(aliases=['leave','dc','disconnect', 'end', 'e'])
@cooldown(1, 5, BucketType.user)
async def bye(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    em = discord.Embed(title = "bye", description = "Yomiage_Engineが抜けます。", color = 0xE67E22)
    em.add_field(name = "**やり方　(syntax)**", value = str(Default_Prefix) + "bye (もしくは" + str(Default_Prefix) + "leave, " + str(Default_Prefix) + "dc, " + str(Default_Prefix) + "disconnect, "  + str(Default_Prefix) + "end, " + str(Default_Prefix) + "e)")
    em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name)) 
    await ctx.send(embed = em, delete_after=5)
    s = settings[ctx.guild.id]
    if s[0] == 1:
        await Play_WAV(ctx,'読み上げエンジンが抜けます。',client_id,client_name, str(ctx.guild.id))
    
@help.command(aliases=['rb'])
@cooldown(1, 5, BucketType.user)
async def reboot(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    em = discord.Embed(title = "reboot", description = "Yomiage_Engineを再起動できます。", color = 0xE67E22)
    em.add_field(name = "**やり方　(syntax)**", value = str(Default_Prefix) + "reboot (もしくは" + str(Default_Prefix) + "rb)")
    em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
    await ctx.send(embed = em, delete_after=10)
    s = settings[ctx.guild.id]
    if s[0] == 1:
        await Play_WAV(ctx, '読み上げエンジンを再起動できます。',client_id,client_name, str(ctx.guild.id))   
 
@help.command(aliases=['m'])
@cooldown(1, 5, BucketType.user)
async def move(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    em = discord.Embed(title = "move", description = "Yomiage_Engineを別の所に移動できます。", color = 0xE67E22)
    em.add_field(name = "**やり方　(syntax)**", value = str(Default_Prefix) + "move (もしくは" + str(Default_Prefix) + "m)")
    em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
    await ctx.send(embed = em, delete_after=10)
    s = settings[ctx.guild.id]
    if s[0] == 1:
        await Play_WAV(ctx, 'Yomiage_Engineを別の所に移動ですます。',client_id,client_name, str(ctx.guild.id))    
    
@help.command(aliases=['addword'])
@cooldown(1, 5, BucketType.user)
async def aw(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    em = discord.Embed(title = "add word", description = "カスタム文字を足すことができます。", color = 0xE67E22)    
    em.add_field(name = "**やり方　(syntax)**", value = str(Default_Prefix) + "addword `登録したい文字``置き換えたい読み方` (もしくは" + str(Default_Prefix) + "aw)")
    em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
    await ctx.send(embed = em, delete_after=5)
    s = settings[ctx.guild.id]
    if s[0] == 1:
        await Play_WAV(ctx,'カスタム文字を足すことができます。',client_id,client_name, str(ctx.guild.id))
    
@help.command(aliases=['deleteword'])
@cooldown(1, 5, BucketType.user)
async def dw(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    em = discord.Embed(title = "delete word", description = "カスタム文字を消すことができます。", color = 0xE67E22)
    em.add_field(name = "**やり方　(syntax)**", value = str(Default_Prefix) + "deleteword `削除したい文字` (もしくは" + str(Default_Prefix) + "dw)")
    em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))    
    await ctx.send(embed = em, delete_after=5)
    s = settings[ctx.guild.id]
    if s[0] == 1:
        await Play_WAV(ctx,'カスタム文字を消すことができます。',client_id,client_name, str(ctx.guild.id))     
    
@help.command(aliases=['settings'])
@cooldown(1, 5, BucketType.user)
async def setting(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    em = discord.Embed(title = "settings", description = "細かい設定ができます。", color = 0xE67E22)
    em.add_field(name = "**やり方　(syntax)**", value = str(Default_Prefix) + "settings (もしくは" + str(Default_Prefix) + "setting)")
    em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
    await ctx.send(embed = em, delete_after=15)
    s = settings[ctx.guild.id]
    if s[0] == 1:
        await Play_WAV(ctx,'細かい設定ができます。',client_id,client_name, str(ctx.guild.id))
            
@help.command(aliases=['as'])
@cooldown(1, 5, BucketType.user)
async def addserver(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    em = discord.Embed(title = "add server", description = "読み上げたいサーバーを足すことができます。", color = 0xE67E22)
    em.add_field(name = "**やり方　(syntax)**", value = str(Default_Prefix) + "addserver (もしくは" + str(Default_Prefix) + "as)")
    em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name)) 
    await ctx.send(embed = em, delete_after=5)
    s = settings[ctx.guild.id]
    if s[0] == 1:
        await Play_WAV(ctx,'読み上げたいサーバーを足すことができます。',client_id,client_name, str(ctx.guild.id))
    
@help.command(aliases=['deleteserver'])
@cooldown(1, 5, BucketType.user)
async def ds(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    em = discord.Embed(title = "delete server", description = "読み上げたくないサーバーを足すことができます。", color = 0xE67E22)
    em.add_field(name = "**やり方　(syntax)**", value = str(Default_Prefix) + "deleteserver (もしくは" + str(Default_Prefix) + "ds)")
    em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
    await ctx.send(embed = em, delete_after=5)
    s = settings[ctx.guild.id]
    if s[0] == 1:
        await Play_WAV(ctx,'読み上げたくないサーバーを足すことができます。',client_id,client_name, str(ctx.guild.id))  

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.group(invoke_without_command=True, aliases=['settings'])
@cooldown(1, 30, BucketType.user)
async def setting(ctx): #設定説明
    try:
        await ctx.message.delete()
    except:
        pass
    em = discord.Embed(title = "設定説明", description = str(Default_Prefix) + "settings <command>で設定ができます。(" + str(Default_Prefix) + "setting <command>でもできます。)", color = 0xE67E22)
    em.add_field(name = "**voice (voices)**", value = "声の設定ができます。\n 例：" + str(Default_Prefix) + "settings voice `<声優さん>` `<スピード:0.0から>` `<重み:0.0から>` `<フィルター:0.0-1.0の間>` `<音程:自由に>`", inline = False)
    em.add_field(name = "**show**", value = "声の設定が確認できます。", inline = False)
    em.add_field(name = "**name (username)**", value = "ユーザーネームの読み上げをつけることができます。", inline = False)
    em.add_field(name = "**botread (br)(bn)(botname)(readbot)(rb)**", value = "ボット文章の読み上げが設定できます。", inline = False)
    em.add_field(name = "**mention (mentions)**", value = "メンションの読み上げを設定できます。", inline = False)
    em.add_field(name = "**readotherbot (readotherbots)**", value = "Yomiage_Engine以外のボット文章の読み上げを設定できます。（オススメしない）", inline = False)
    em.add_field(name = "**length (ln)(wordlength)(limit)(wordlimit)(wl)**", value = "ボットが読み上げる文字数の設定ができます。 \n例: " + str(Default_Prefix) + "settings length `<文字数>`", inline = False)
    em.add_field(name = "**emoji (emojis)(reademoji)**", value = "絵文字読み上げの設定ができます。", inline = False)
    em.add_field(name = "**deleteallword (dal)**", value = "[**注意！**]登録した辞書を全部消します。", inline = False)
    em.add_field(name = "**prefix (changeprefix)(cp)**", value = "サーバー固有のPrefixの設定ができます。\n 例：" + str(Default_Prefix) + "settings prefix `<プレフェックスにスペース:[0か1]>` `<新しいPrefix:自由に>`", inline = False)
    em.add_field(name = "**addblacklist (abl)**", value = "**(権限者オンリー)** ユーザーのBot命令を制限します。", inline = False)
    em.add_field(name = "**removeblacklist (rbl)**", value = "**(権限者オンリー)** ユーザーのBot命令の制限から解除します。", inline = False)
    em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed = em, delete_after=20)
    await ctx.author.send(embed = em)
    s = settings[ctx.guild.id]
    if s[0] == 1:
        await Play_WAV(ctx,'設定です。ここのコマンドは少し特殊なのでご注意を。',client_id,client_name, str(ctx.guild.id))  

@setting.command(aliases=['username','readusername','readusernames', 'readname', 'readnames'])
@cooldown(1, 10, BucketType.user)
async def name(ctx): #設定:ユーザー名読み上げ
    if isinstance(ctx.channel, discord.channel.DMChannel):
        em = discord.Embed(title = "エラー", description = "ここはDMです。そのコマンドはここでは使えません。", color = 0xE67E22)
        await ctx.send(embed = em, delete_after=10)
    else:
        try:
            await ctx.message.delete()
        except:
            pass
        if check_blacklist(str(ctx.guild.id),str(ctx.message.author)) == True:
            await blacklisted(ctx)
            return
        msg, em = Settings_Username(str(ctx.guild.id))
        em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
        await ctx.send(embed = em, delete_after=5)
        s = settings[ctx.guild.id]
        if s[0] == 1:
            await Play_WAV(ctx,msg,client_id,client_name, str(ctx.guild.id))
    
@setting.command(aliases=['br', 'bn', 'botname', 'readbot', 'rb'])
@cooldown(1, 10, BucketType.user)
async def botread(ctx): #設定:ボットの文章の読み上げ
    if isinstance(ctx.channel, discord.channel.DMChannel):
        em = discord.Embed(title = "エラー", description = "ここはDMです。そのコマンドはここでは使えません。", color = 0xE67E22)
        await ctx.send(embed = em, delete_after=10)
    else:
        try:
            await ctx.message.delete()
        except:
            pass
        if check_blacklist(str(ctx.guild.id),str(ctx.message.author)) == True:
            await blacklisted(ctx)
            return
        global settings
        msg, em, switch = botyomiage(str(ctx.guild.id))
        try:
            s = settings[ctx.guild.id]
            if switch == 1:
                settings[ctx.guild.id] = [1,s[1],s[2]]
            elif switch == 0:
                settings[ctx.guild.id] = [0,s[1],s[2]]
        except:
            pass
        em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
        await ctx.send(embed = em, delete_after=5)
        s = settings[ctx.guild.id]
        if s[0] == 1:
            await Play_WAV(ctx,msg,client_id,client_name, str(ctx.guild.id))

@setting.command(aliases=['mentions','readmentions','readmention'])
@cooldown(1, 10, BucketType.user)
async def mention(ctx): #設定:ボットの文章の読み上げ
    if isinstance(ctx.channel, discord.channel.DMChannel):
        em = discord.Embed(title = "エラー", description = "ここはDMです。そのコマンドはここでは使えません。", color = 0xE67E22)
        await ctx.send(embed = em, delete_after=10)
    else:
        try:
            await ctx.message.delete()
        except:
            pass
        if check_blacklist(str(ctx.guild.id),str(ctx.message.author)) == True:
            await blacklisted(ctx)
            return
        global settings
        msg, em, switch = settings_mentions(str(ctx.guild.id))
        try:
            s = settings[ctx.guild.id]
            if switch == 1:
                settings[ctx.guild.id] = [s[0],1,s[2]]
            elif switch == 0:
                settings[ctx.guild.id] = [s[0],0,s[2]]
        except:
            pass
        em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
        await ctx.send(embed = em, delete_after=5)
        s = settings[ctx.guild.id]
        if s[0] == 1:
            await Play_WAV(ctx,msg,client_id,client_name, str(ctx.guild.id))

@setting.command(aliases=['readotherbots'])
@cooldown(1, 10, BucketType.user)
async def readotherbot(ctx): #設定:ボットの文章の読み上げ
    if isinstance(ctx.channel, discord.channel.DMChannel):
        em = discord.Embed(title = "エラー", description = "ここはDMです。そのコマンドはここでは使えません。", color = 0xE67E22)
        await ctx.send(embed = em, delete_after=10)
    else:
        try:
            await ctx.message.delete()
        except:
            pass
        if check_blacklist(str(ctx.guild.id),str(ctx.message.author)) == True:
            await blacklisted(ctx)
            return
        global settings
        msg, em, switch = settings_bot_message(str(ctx.guild.id))
        try:
            s = settings[ctx.guild.id]
            if switch == 1:
                settings[ctx.guild.id] = [s[0],s[1],1]
            elif switch == 0:
                settings[ctx.guild.id] = [s[0],s[1],0]
        except:
            pass
        em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
        await ctx.send(embed = em, delete_after=5)
        s = settings[ctx.guild.id]
        if s[0] == 1:
            await Play_WAV(ctx,msg,client_id,client_name, str(ctx.guild.id))

@setting.command(aliases=['emojis','reademoji'])
@cooldown(1, 10, BucketType.user)
async def emoji(ctx): #設定:ボットの文章の読み上げ
    if isinstance(ctx.channel, discord.channel.DMChannel):
        em = discord.Embed(title = "エラー", description = "ここはDMです。そのコマンドはここでは使えません。", color = 0xE67E22)
        await ctx.send(embed = em, delete_after=10)
    else:
        try:
            await ctx.message.delete()
        except:
            pass
        if check_blacklist(str(ctx.guild.id),str(ctx.message.author)) == True:
            await blacklisted(ctx)
            return
        msg, em = reademoji(str(ctx.guild.id))
        em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
        await ctx.send(embed = em, delete_after=5)
        s = settings[ctx.guild.id]
        if s[0] == 1:
            await Play_WAV(ctx,msg,client_id,client_name, str(ctx.guild.id))
    
@setting.command(aliases=['voices'])
@cooldown(1, 10, BucketType.user)
async def voice(ctx, arg1, arg2, arg3, arg4, arg5): # settings_io
    try:
        await ctx.message.delete()
    except:
        pass
    Username = str(ctx.author.name)
    Message_Author = str(ctx.author.id)
    
    arg2 = round(float(arg2)*100)/100
    arg3 = round(float(arg3)*100)/100
    arg4 = round(float(arg4)*100)/100
    arg5 = round(float(arg5)*100)/100
    
    if not (0.5 < float(arg2) and float(arg2) <= 15):
        msg = ('その速度設定はできません。入れ直してください。')
        em = discord.Embed(title = "エラー", description = ("そんな速度設定はできません。入れ直してください。[0.5から15まで]"), color = 0xE67E22)
    elif not (0 <= float(arg3) and float(arg3) <= 1):
        msg = ('その重みの設定はできません。入れ直してください。')
        em = discord.Embed(title = "エラー", description = ("その重みの設定はできません。入れ直してください。[0から1まで] (おすすめは0)"), color = 0xE67E22)
    elif not (0 <= float(arg4) and float(arg4) <= 1):
        msg = ('そのフィルターの設定はできません。入れ直してください。')
        em = discord.Embed(title = "エラー", description = ("そのフィルターの設定はできません。入れ直してください。[0から1まで] (おすすめは0.5)"), color = 0xE67E22)
    elif not (-30 <= float(arg5) and float(arg4) <= 30):
        msg = ('その音程の設定はできません。入れ直してください。')
        em = discord.Embed(title = "エラー", description = ("その音程の設定はできません。入れ直してください。[-30と30の間] (おすすめは0.5)"), color = 0xE67E22)
    else:
        msg, em = settings_io(Username,Message_Author,arg1,str(arg2),str(arg3),str(arg4),str(arg5))
        em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
    await ctx.send(embed = em, delete_after=10)
    s = settings[ctx.guild.id]
    if s[0] == 1:
        await Play_WAV(ctx,msg,client_id,client_name, str(ctx.guild.id))

@setting.command(aliases=['showvoices','showvoice','showsetting','showsettings','koe'])
@cooldown(1, 10, BucketType.user)
async def show(ctx): #show
    try:
        await ctx.message.delete()
    except:
        pass
    Username = str(ctx.author.name)
    Message_Author = str(ctx.author.id)
    msg, em = show_settings(Username,Message_Author)
    em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
    await ctx.send(embed = em, delete_after=5)
    s = settings[ctx.guild.id]
    if s[0] == 1:
        await Play_WAV(ctx,msg,client_id,client_name, str(ctx.guild.id))

@setting.command(aliases=['ln', 'wordlength', 'limit', 'wordlimit', 'wl'])
@cooldown(1, 10, BucketType.user)
async def length(ctx, arg1): #設定:ボットが読み上げる文章の上限
    if isinstance(ctx.channel, discord.channel.DMChannel):
        em = discord.Embed(title = "エラー", description = "ここはDMです。そのコマンドはここでは使えません。", color = 0xE67E22)
        await ctx.send(embed = em, delete_after=10)
    else:
        try:
            await ctx.message.delete()
        except:
            pass
        if check_blacklist(str(ctx.guild.id),str(ctx.message.author)) == True:
            await blacklisted(ctx)
            return
        arg1 = (math.floor(float(arg1)))
        if not float(arg1) < 2000:
            arg1 = 2000
        msg, em = Wordlimit(str(ctx.guild.id), str(arg1))
        em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
        await ctx.send(embed = em, delete_after=5)
        s = settings[ctx.guild.id]
        if s[0] == 1:
            await Play_WAV(ctx,msg,client_id,client_name, str(ctx.guild.id))

@setting.command(aliases=['deleteallwords','dal'])
@cooldown(1, 10, BucketType.user)
async def deleteallword(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        em = discord.Embed(title = "エラー", description = "ここはDMです。そのコマンドはここでは使えません。", color = 0xE67E22)
        await ctx.send(embed = em, delete_after=10)
    else:
        try:
            await ctx.message.delete()
        except:
            pass
        if check_blacklist(str(ctx.guild.id),str(ctx.message.author)) == True:
            await blacklisted(ctx)
            return
        msg, em = delete_all_word(str(ctx.guild.id))
        em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
        await ctx.send(embed = em, delete_after=10)
        s = settings[ctx.guild.id]
        if s[0] == 1: 
            await Play_WAV(ctx,msg,client_id,client_name, str(ctx.guild.id))

@setting.command(aliases=['changeprefix','prefixes','changeprefixes','cp'])
async def prefix(ctx, arg1, arg2):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        em = discord.Embed(title = "エラー", description = "ここはDMです。そのコマンドはここでは使えません。", color = 0xE67E22)
        await ctx.send(embed = em, delete_after=10)
    else:
        try:
            await ctx.message.delete()
        except:
            pass
        if check_blacklist(str(ctx.guild.id),str(ctx.message.author)) == True:
            await blacklisted(ctx)
            return
        try:
            global custom_prefix
            msg, em = settings_prefixes(ctx.guild.id, arg1, arg2, Default_Prefix)
            em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
            await ctx.send(embed = em, delete_after=10)
            if str(arg1) == str(0):  
                custom_prefix[ctx.guild.id] = [str(arg2)]
            elif str(arg1) == str(1):
                custom_prefix[ctx.guild.id] = [str(arg2) + ' ']
            s = settings[ctx.guild.id]
            if s[0] == 1:
                await Play_WAV(ctx,msg,client_id,client_name, str(ctx.guild.id)) 
        except:
            em = discord.Embed(title = "エラー", description = "そのPrefixのは設定できません。申し訳ございません。", color = 0xE67E22)
            em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
            await ctx.send(embed = em, delete_after=10)
            s = settings[ctx.guild.id]
            if s[0] == 1:
                await Play_WAV(ctx,'そのPrefixのは設定できません。申し訳ございません。',client_id,client_name, str(ctx.guild.id)) 
                
@setting.command(aliases=['abl'])
@commands.has_permissions(administrator=True)
async def addblacklist(ctx, member: discord.Member):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        em = discord.Embed(title = "エラー", description = "ここはDMです。そのコマンドはここでは使えません。", color = 0xE67E22)
        await ctx.send(embed = em, delete_after=10)
    else:
        try:
            await ctx.message.delete()
        except:
            pass
        try:
            msg, em = add_blacklist(str(ctx.guild.id), member)
            em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
            await ctx.send(embed = em, delete_after=10)
            s = settings[ctx.guild.id]
            if s[0] == 1: 
                await Play_WAV(ctx,msg,client_id,client_name, str(ctx.guild.id))
        except:
            em = discord.Embed(title = "エラー", description = "要件が違います。入れ直してください。", color = 0xE67E22)
            em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
            await ctx.send(embed = em, delete_after=10)
            s = settings[ctx.guild.id]
            if s[0] == 1:
                await Play_WAV(ctx,'要件が違います。入れ直してください。',client_id,client_name, str(ctx.guild.id)) 
    
@setting.command(aliases=['rbl'])
@commands.has_permissions(administrator=True)
async def removeblacklist(ctx, member: discord.Member):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        em = discord.Embed(title = "エラー", description = "ここはDMだよ！そのコマンドはここでは使えないよ！", color = 0xE67E22)
        await ctx.send(embed = em, delete_after=10)
    else:
        try:
            await ctx.message.delete()
        except:
            pass
        try:
            msg, em = remove_blacklist(str(ctx.guild.id), member)
            em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
            await ctx.send(embed = em, delete_after=10)
            s = settings[ctx.guild.id]
            if s[0] == 1: 
                await Play_WAV(ctx,msg,client_id,client_name, str(ctx.guild.id))
        except:
            em = discord.Embed(title = "エラー", description = "要件が違います。入れ直してください。", color = 0xE67E22)
            em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
            await ctx.send(embed = em, delete_after=10)
            s = settings[ctx.guild.id]
            if s[0] == 1:
                await Play_WAV(ctx,'要件が違います。入れ直してください。',client_id,client_name, str(ctx.guild.id)) 
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.command(aliases=['vl'])
@cooldown(1, 20, BucketType.user)
async def voicelist(ctx): #声優さんのリスト
    try:
        await ctx.message.delete()
    except:
        pass
    em = discord.Embed(title = "声優さんのリストです。", description = "man \nwoman \nmei_angry \nmei_bashful \nmei_happy \nmei_sad \ntohoku \ntohoku_angry \ntohoku_happy \ntohoku_sad \nai \nfuuki \ngiruko \nhomu \nikuru \nikuto \nkanata \nkono \nmai \nmatsuo \nnero \nniji \notoko \nrakan \nriyon \nrou \nsou \nwamea \nwatashi \nyoe \nhitori \nsakura \nkoto \nakesato \nmizuki \nmomo \nrami \nshiba \nkaoru \nsuranki \ngurimarukin", color = 0xE67E22)    
    em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed = em, delete_after=20)
    await ctx.author.send(embed = em)
    s = settings[ctx.guild.id]
    if s[0] == 1:
        await Play_WAV(ctx,'声優さんのリストです。',client_id,client_name, str(ctx.guild.id))
        
@client.command(aliases=['ts'])
@cooldown(1, 10, BucketType.user)
async def troubleshoot(ctx): #トラブルシュート
    try:
        await ctx.message.delete()
    except:
        pass
    em = discord.Embed(title = "トラブルシューティング", description = "もし動かなくなった場合、この処置をとってください。", color = 0xE67E22)
    em.add_field(name = "**1**", value = str(Default_Prefix) + "rebootで再起動する", inline = False)
    em.add_field(name = "**2**", value = str(Default_Prefix) + "helloで再度呼ぶ", inline = False)
    em.add_field(name = "**3**", value = str(Default_Prefix) + "addserverでサーバーを足す", inline = False)
    em.add_field(name = "**それでもダメな時には:**", value = "`" + Bot_Author +"`さんに再起動を依頼する")
    em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed = em, delete_after=10)
    await ctx.author.send(embed = em)
    s = settings[ctx.guild.id]
    if s[0] == 1:
        await Play_WAV(ctx,'大丈夫でしょうか？問題があるなら' + str(Bot_Author) +'さんに聞いてください。',client_id,client_name, str(ctx.guild.id))

@client.command(aliases=['pingcheck'])
@cooldown(1, 5, BucketType.user)
async def ping(ctx): #Pingの確認
    try:
        await ctx.message.delete()
    except:
        pass
    Pong = (round(client.latency*100000))/100
    em = discord.Embed(title = "pong", description = ("Yomiage_Engineが反応するまでの時間（レイテンシー）は`"+ str(Pong) +"ms`です。"), color = 0xE67E22)
    em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
    await ctx.send(embed = em, delete_after=7)
    s = settings[ctx.guild.id]
    if s[0] == 1:
        await Play_WAV(ctx,('読み上げエンジンが反応するまでの時間は`'+ str(Pong) +'ms`です。'),client_id,client_name, str(ctx.guild.id))

@client.command(aliases=['credits','staff','staffs','staffcredits','staffcredit','author','authors'])
@cooldown(1, 5, BucketType.user)
async def credit(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    em = discord.Embed(title = "credit", description = ("Yomiage_Engine（イルーくん、読ませてイルカ）の作成に関わってくれた人たちです。見かけたら声かけてください！"), color = 0xE67E22)
    em.add_field(name = "**作者さんからのお礼**", value = "秘密のコマンドです、関わってくれた人たちも感謝いっぱいですが、いつもイルーくんを使ってくれてるみなさんにも感謝・お礼でいっぱいです！ありがとうございます！", inline = False)
    em.add_field(name = "**Credits**", value = "Yomasete_Iruka By: \n**・**Nemy_zz \n**・**Yhay81 \n**・**TogeRaz \n**・**Tom_XV \n**・**Baku_reshi\n**・**Yuki_Trans \n**・**Airun", inline = False)
    em.add_field(name = "**Special Thanks**", value = "**・**Kazu220_ps \n**・**Wilco", inline = False)
    em.set_thumbnail(url = client.user.avatar_url)
    em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
    s = settings[ctx.guild.id]
    if s[0] == 1:
        await Play_WAV(ctx,'このBotを育ててくれた人たちです、見かけたら声かけてください！ありがとうございます！',client_id,client_name, str(ctx.guild.id))

@client.command(aliases=['join','start','s','call','connect'])
@cooldown(1, 5, BucketType.user)
async def hello(ctx): #こんにちは！
    if isinstance(ctx.channel, discord.channel.DMChannel):
        em = discord.Embed(title = "エラー", description = "ここはDMです。そのコマンドはここでは使えません。", color = 0xE67E22)
        await ctx.send(embed = em, delete_after=10)
    else:
        try:
            await ctx.message.delete()
        except:
            pass
        global last_textch_id
        global settings
        global queues
        global first_check
        try:
            queues[ctx.guild.id] = []
            first_check[ctx.guild.id] = [0]
            guildid = str(ctx.author.guild.id)
            msgid = str(ctx.message.channel.id)
            msgname = str(ctx.message.channel.name)
            Read_Settings_Missing = True
            delete_all_server(guildid)
            last_textch_id[ctx.guild.id] = [ctx.guild.id, ctx.message.channel.id]
            with open(f'{CONFIG_PREFIX}/Settings.txt', mode='r', encoding = 'utf-8') as f:
                d = f.readlines()
                f.seek(0)
                for i in d:
                    wd = i.strip().split(',')
                    if (wd[0] == str(ctx.guild.id)):
                        Read_Settings_Missing = False
                        settings[ctx.guild.id] = [int(wd[2]),int(wd[5]),int(wd[6])] 
                        break
            f.close()
            if Read_Settings_Missing == True:
                with open(f'{CONFIG_PREFIX}/Settings.txt', mode='a', encoding = 'utf-8') as f:
                    f.write(str(ctx.guild.id) + ',' + '0' + ',' + '1' + ',' + '50' +  ',' + '0' + ',' + '1' + ',' + '0' + '\n')
                    settings[ctx.guild.id] = [1,1,0] #checkbotread = 1 checkmentionread = 1
                f.close()     
            if get(client.voice_clients, guild=ctx.guild) == None:
                global vcconnected
                add_server(guildid,msgid,msgname)
                vc = ctx.author.voice.channel
                print('')
                print('------------------------------------------')
                print('#join')
                print('#voicechannelを取得:(' + str(vc) + ',' + str(ctx.author.guild) + ')')
                await vc.connect()
                vcconnected[ctx.guild.id] = [1]
                print('#voicechannelに接続:(' + str(vc) + ',' + str(ctx.author.guild) + ')')
                print('------------------------------------------')
                em = discord.Embed(title = "接続成功", description = "接続成功です。これからの文章を読み上げます。", color = 0xE67E22)
                em.set_thumbnail(url = client.user.avatar_url)
                em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
                await ctx.send(embed = em, delete_after=5)
                s = settings[ctx.guild.id]
                if s[0] == 1:
                    await Play_WAV(ctx,'接続成功です。これからの文章を読み上げます。',client_id,client_name,str(ctx.guild.id))
            else:
                em = discord.Embed(title = "エラー", description = "もうボイスチャットにつながっています。", color = 0xE67E22)
                em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
                await ctx.send(embed = em, delete_after=5)
                s = settings[ctx.guild.id]
                if s[0] == 1:
                    await Play_WAV(ctx,'もうボイスチャットにつながっています。',client_id,client_name,str(ctx.guild.id))
        except:
            em = discord.Embed(title = "エラー", description = "ボイチャにつながっていません。つないでから呼んでください。", color = 0xE67E22)
            em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
            await ctx.send(embed = em, delete_after=5)
            s = settings[ctx.guild.id]
            if s[0] == 1:
                try:
                    await Play_WAV(ctx, '他の人がつながっていません。「ここにいます」と教えてください。',client_id,client_name, str(ctx.guild.id))
                except:
                    pass

@client.command(aliases=['leave','dc','disconnect','end','e'])
@cooldown(1, 5, BucketType.user)
async def bye(ctx): #さよなら!
    if isinstance(ctx.channel, discord.channel.DMChannel):
        em = discord.Embed(title = "エラー", description = "ここはDMです。そのコマンドはここでは使えません。", color = 0xE67E22)
        await ctx.send(embed = em, delete_after=10)
    else:
        try:
            await ctx.message.delete()
        except:
            pass
        if check_blacklist(str(ctx.guild.id),str(ctx.message.author)) == True:
            await blacklisted(ctx)
            return
        try:
            guildid = str(ctx.author.guild.id)
            if get(client.voice_clients, guild=ctx.guild) != None:
                global vcconnected
                em = discord.Embed(title = "接続解除", description = str(Leave_Message), color = 0xE67E22)
                em.add_field(name = "**Credits**", value = "Yomasete_Iruka By: \nnemy_zz, Yhay81, TogeRaz, Tom_XV, baku_reshi, Yuki_Trans, Airun", inline = False)
                em.add_field(name = "**Special Thanks**", value = "kazu220_ps, Wilco", inline = False)
                em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
                await ctx.send(embed = em, delete_after=5)
                s = settings[ctx.guild.id]
                if s[0] == 1:
                    await Play_WAV(ctx,Leave_Message,client_id,client_name, str(ctx.guild.id))
                    time.sleep(1)
                else:
                    vcconnected[ctx.guild.id] = [0]
                delete_all_server(guildid)
                del queues[ctx.guild.id]
                del first_check[ctx.guild.id]
                print('')
                print('------------------------------------------')
                print('#bye')
                await ctx.voice_client.disconnect()
                print('#切断:(' + str(ctx.author.voice.channel) + ',' + str(ctx.author.guild) + ')')
                print('------------------------------------------')              
            else:     
                em = discord.Embed(title = "エラー", description = "ボイスチャットにつながっていません。", color = 0xE67E22)
                em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))        
                await ctx.send(embed = em, delete_after=5)
        except:
            em = discord.Embed(title = "エラー", description = "ボイスチャットにつながっていません。つないでから呼んでください。", color = 0xE67E22)
            em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
            await ctx.send(embed = em, delete_after=5)
            s = settings[ctx.guild.id]
            if s[0] == 1:
                await Play_WAV(ctx,'他の人がつながっていません。「ここにいます」と教えてください。',client_id,client_name, str(ctx.guild.id))

@client.command(aliases=['rb','move','m'])
@cooldown(1, 5, BucketType.user)
async def reboot(ctx): #入り直し・移動
    if isinstance(ctx.channel, discord.channel.DMChannel):
        em = discord.Embed(title = "エラー", description = "ここはDMです。そのコマンドはここでは使えません。", color = 0xE67E22)
        await ctx.send(embed = em, delete_after=10)
    else:
        try:
            await ctx.message.delete()
        except:
            pass
        if check_blacklist(str(ctx.guild.id),str(ctx.message.author)) == True:
            await blacklisted(ctx)
            return
        try:
            guildid = str(ctx.author.guild.id)
            msgid = str(ctx.message.channel.id)
            msgname = str(ctx.message.channel.name)
            delete_all_server(guildid)
            global vcconnected
            print('')
            print('------------------------------------------')
            if int(ctx.author.voice.channel.id) == int(ctx.voice_client.channel.id):
                if ctx.message.content == (str(get_prefix(client,ctx.message)) + 'move') or ctx.message.content == (str(get_prefix(client,ctx.message)) + 'm'):
                    em = discord.Embed(title = "エラー", description = "Yomiage_Engineはもう在籍しています。", color = 0xE67E22)
                    em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
                    await ctx.send(embed = em, delete_after=5)
                    s = settings[ctx.guild.id]
                    if s[0] == 1:
                        await Play_WAV(ctx,'読み上げエンジンはもう在籍しています。',client_id,client_name, str(ctx.guild.id))
                    print('同じVCでMoveコマンドなのでスキップ')
                    print('------------------------------------------')
                    return
                else:
                    print('#reboot')
                    switch = 1
            elif int(ctx.author.voice.channel.id) != int(ctx.voice_client.channel.id):
                if ctx.message.content == (str(get_prefix(client,ctx.message)) + 'reboot') or ctx.message.content == (str(get_prefix(client,ctx.message)) + 'rb'):
                    em = discord.Embed(title = "エラー", description = "Yomiage_Engineは別の場所にいます。", color = 0xE67E22)
                    em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
                    await ctx.send(embed = em, delete_after=5)
                    print('rebootコマンドだが、別部屋にいるのでスキップ')
                    return
                else:
                    print('#move')
                    switch = 0
            vcconnected[ctx.guild.id] = [0]
            del queues[ctx.guild.id]
            del first_check[ctx.guild.id]
            await ctx.voice_client.disconnect()
            print('#切断:(' + str(ctx.author.voice.channel) + ',' + str(ctx.author.guild) + ')')
            await ctx.author.voice.channel.connect()
            add_server(guildid, msgid, msgname)
            vcconnected[ctx.guild.id] = [1]
            queues[ctx.guild.id] = []
            first_check[ctx.guild.id] = [0]
            print('#接続:(' + str(ctx.author.voice.channel) + ',' + str(ctx.author.guild) + ')')
            print('------------------------------------------')
            if switch == 1:
                em = discord.Embed(title = "reboot", description = "入り直しました、聞こえますでしょうか？", color = 0xE67E22)
                em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
                await ctx.send(embed = em, delete_after=5)
                s = settings[ctx.guild.id]
                if s[0] == 1:
                    await Play_WAV(ctx,'入り直しました、聞こえますでしょうか？',client_id,client_name, str(ctx.guild.id))
            elif switch == 0:
                em = discord.Embed(title = "move", description = "`" + str(ctx.author.voice.channel) + "`に移動しました。聞こえますでしょうか？", color = 0xE67E22)
                em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
                await ctx.send(embed = em, delete_after=5)
                s = settings[ctx.guild.id]
                if s[0] == 1:
                    await Play_WAV(ctx, ('移動しました。聞こえますでしょうか？') ,client_id,client_name, str(ctx.guild.id))
        except:
            em = discord.Embed(title = "エラー", description = "ボイスチャットにつながっていません。つないでから呼んでください。", color = 0xE67E22)
            em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
            await ctx.send(embed = em, delete_after=5)
            s = settings[ctx.guild.id]
            if s[0] == 1:
                await Play_WAV(ctx,'他の人がつながっていません。「ここにいます」と教えてください。',client_id,client_name, str(ctx.guild.id))

@client.command(aliases=['addword'])
@cooldown(1, 10, BucketType.user)
async def aw(ctx, arg1, arg2): # add_word
    if isinstance(ctx.channel, discord.channel.DMChannel):
        em = discord.Embed(title = "エラー", description = "ここはDMです。そのコマンドはここでは使えません。", color = 0xE67E22)
        await ctx.send(embed = em, delete_after=10)
    else:
        try:
            await ctx.message.delete()
        except:
            pass
        if check_blacklist(str(ctx.guild.id),str(ctx.message.author)) == True:
            await blacklisted(ctx)
            return
        try:
            arg1 = Lowercase_trans(arg1)
            arg2 = Lowercase_trans(arg2)
            msg, em = add_word(arg1, arg2, str(ctx.guild.id))
            em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
            await ctx.send(embed = em, delete_after=5)
            s = settings[ctx.guild.id]
            if s[0] == 1:
                await Play_WAV(ctx,msg,client_id,client_name, str(ctx.guild.id))
        except:
            em = discord.Embed(title = "エラー", description = "その単語の設定はできません。申し訳ございません。", color = 0xE67E22)
            em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
            await ctx.send(embed = em, delete_after=5)
            s = settings[ctx.guild.id]
            if s[0] == 1:
                await Play_WAV(ctx,"その単語の設定はできません。申し訳ございません。",client_id,client_name, str(ctx.guild.id))
    
@client.command(aliases=['deleteword'])
@cooldown(1, 10, BucketType.user)
async def dw(ctx, arg1): # delete_word
    if isinstance(ctx.channel, discord.channel.DMChannel):
        em = discord.Embed(title = "エラー", description = "ここはDMです。そのコマンドはここでは使えません。", color = 0xE67E22)
        await ctx.send(embed = em, delete_after=10)
    else:
        try:
            await ctx.message.delete()
        except:
            pass
        if check_blacklist(str(ctx.guild.id),str(ctx.message.author)) == True:
            await blacklisted(ctx)
            return
        try:
            arg1 = Lowercase_trans(str(arg1))
            msg, em = delete_word(arg1, str(ctx.guild.id))
            em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
            await ctx.send(embed = em, delete_after=5)
            s = settings[ctx.guild.id]
            if s[0] == 1: 
                await Play_WAV(ctx,msg,client_id,client_name, str(ctx.guild.id))
        except:
            em = discord.Embed(title = "エラー", description = "その単語の設定はできません。申し訳ございません。", color = 0xE67E22)
            em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
            await ctx.send(embed = em, delete_after=5)
            s = settings[ctx.guild.id]
            if s[0] == 1:
                await Play_WAV(ctx,"その単語の設定はできません。申し訳ございません。",client_id,client_name, str(ctx.guild.id))

@client.command(aliases=['as'])
@cooldown(1, 10, BucketType.user)
async def addserver(ctx): # add_server
    if isinstance(ctx.channel, discord.channel.DMChannel):
        em = discord.Embed(title = "エラー", description = "ここはDMです。そのコマンドはここでは使えません。", color = 0xE67E22)
        await ctx.send(embed = em, delete_after=10)
    else:
        vc = vcconnected[ctx.guild.id]
        if vc[0] == 0:
            try:
                await ctx.message.delete()
            except:
                pass
            if check_blacklist(str(ctx.guild.id),str(ctx.message.author)) == True:
                await blacklisted(ctx)
                return
            em = discord.Embed(title = "エラー", description = "ボイスチャットにつながっていません。つないでから呼んでください。", color = 0xE67E22)
            em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
            await ctx.send(embed = em, delete_after=5)
        else:
            try:
                await ctx.message.delete()
            except:
                pass
            if check_blacklist(str(ctx.guild.id),str(ctx.message.author)) == True:
                await blacklisted(ctx)
                return
            msgid = str(ctx.message.channel.id)
            msgname = str(ctx.message.channel.name)
            guildid = str(ctx.author.guild.id)
            msg, em = add_server(guildid,msgid,msgname)
            em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name)) 
            await ctx.send(embed = em, delete_after=5)
            s = settings[ctx.guild.id]
        if s[0] == 1:
            await Play_WAV(ctx,msg,client_id,client_name, str(ctx.guild.id))
    
@client.command(aliases=['deleteserver'])
@cooldown(1, 10, BucketType.user)
async def ds(ctx): # delete_server
    if isinstance(ctx.channel, discord.channel.DMChannel):
        em = discord.Embed(title = "エラー", description = "ここはDMです。そのコマンドはここでは使えません。", color = 0xE67E22)
        await ctx.send(embed = em, delete_after=10)
    else:
        vc = vcconnected[ctx.guild.id]
        if vc[0] == 0:
            try:
                await ctx.message.delete()
            except:
                pass
            em = discord.Embed(title = "エラー", description = "ボイスチャットにつながっていません。つないでから呼んでください。", color = 0xE67E22)
            em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
            await ctx.send(embed = em, delete_after=5)
        else:
            try:
                await ctx.message.delete()
            except:
                pass
            guildid = str(ctx.author.voice.channel.id)
            msgid = str(ctx.message.channel.id)
            guildid = str(ctx.author.guild.id)
            msg, em = delete_server(guildid,msgid)
            em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
            await ctx.send(embed = em, delete_after=5)
            s = settings[ctx.guild.id]
            if s[0] == 1:
                await Play_WAV(ctx,msg,client_id,client_name, str(ctx.guild.id))

@client.event
async def on_message(message):
    try:
        if not isinstance(message.channel, discord.channel.DMChannel):
            global vcconnected
            global settings
            try:
                vc = vcconnected[message.guild.id]
                readbot = settings[message.guild.id]
            except:
                vcconnected[message.guild.id] = [0]
                vc = vcconnected[message.guild.id]
                settings[message.guild.id] = [0,0,0]
                readbot = settings[message.guild.id]
        if message.content.startswith(str(get_prefix(client,message))) or message.content.startswith(Default_Prefix):
            print('')
            print('---------------------')
            print("Prefixを感知しました、コマンドプロセスします!") #Prefixから始まる文は読み飛ばし
            print('---------------------')
            await client.process_commands(message)
            return
        elif message.author.id == client.user.id:
            print('')
            print('---------------------')
            print("Botの文なので読み飛ばし。") #Botの文は読み飛ばし
            print('---------------------')
            return
        elif message.author.bot and readbot[2] == 0:
            print('')
            print('---------------------')
            print("Botの文なので読み飛ばし。") #Botの文は読み飛ばし
            print('---------------------')
            return
        elif isinstance(message.channel, discord.channel.DMChannel):
            print('')
            print('---------------------')
            print("DMなのでパス。") #DMの文は読み飛ばし
            print('---------------------')
            return
        else:
            try:
                global last_textch_id
                textch = last_textch_id[message.guild.id]
                if message.guild.id == textch[0]:
                    last_textch_id[message.guild.id] = [message.guild.id, message.channel.id]
            except:
                pass
            if message.content.startswith(';'): #「.」または「;」から始まる文は読み飛ばし
                print('')
                print('------------------------------------------')
                print("「;」を感知しました、読み飛ばします!")
                print('------------------------------------------') 
                return
            guildid = str(message.guild.id)
            msgid = str(message.channel.id)
            Message_Author = str(message.author.id) #Shoutout to my friend Kazu
            if message.author.nick:
                Username = str(message.author.nick)
            else:
                Username = str(message.author.name)
            Affirmed_Server_List = False
            Affirmed_User_List = False
            
            #ユーザーボイスが設定されてるかチェック（Step1
            with open(f'{CONFIG_PREFIX}/User.txt', mode='r', encoding = 'utf-8') as f:
                d = f.readlines()
                f.seek(0)
                for i in d:
                    wd = i.strip().split(',')
                    if wd[0] == Message_Author:
                        Affirmed_User_List = True
                        break
            f.close()

            #ユーザーボイスが設定されてるかチェック（Step2
            if (Affirmed_User_List == False):
                with open(f'{CONFIG_PREFIX}/User.txt', mode='a', encoding = 'utf-8') as f:
                    f.write(Message_Author + ',' + 'woman,1.5,0,0.5,0' + '\n')
            f.close()
                
            #登録されてるボイチャ、テキストチャンネルを調べ、比べる。
            with open(f'{CONFIG_PREFIX}/server.txt', mode='r', encoding = 'utf-8') as f:
                d = f.readlines()
                f.seek(0)
                for i in d:
                    wd = i.strip().split(',')
                    if wd[0] == guildid and wd[1] == msgid:
                        Affirmed_Server_List = True
                        break
            f.close()

            if ((Affirmed_Server_List == True) and vc[0] == 1):
                Msg = remove_mention(message)
                await Play_WAV(message, Msg, Message_Author, Username, str(message.guild.id))
            elif vc[0] == 0:
                print('')
                print('---------------------')
                print("繋がっていないのでスルー")
                print('---------------------')
            else:
                print('')
                print('------------------------------------------')
                print("鯖外からの文章なので飛ばします！") #読み飛ばし
                print('------------------------------------------')
    except:
        print('')
        print('---------------------')
        print('エラー')
        print('---------------------')

@client.event
async def on_command_error(ctx, error):
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        vc = vcconnected[ctx.guild.id]
        if vc[0] == 1:
            s = settings[ctx.guild.id]
        else:
            settings[ctx.guild.id] = [0]
            
    if isinstance(error, commands.CommandNotFound):  
        try:
            await ctx.message.delete()
        except:
            pass
        
        em = discord.Embed(title = "エラー", description = ("そのコマンドは存在しません、入れ直してください。"), color = 0xE67E22)
        em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
        await ctx.send(embed = em, delete_after=7)
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            if vc[0] == 1 and s[0] == 1:
                await Play_WAV(ctx,'そのコマンドは存在しません、入れ直してください。',client_id,client_name, str(ctx.guild.id))
        
    if isinstance(error, commands.MissingRequiredArgument):
        try:
            await ctx.message.delete()
        except:
            pass
        em = discord.Embed(title = "エラー", description = ("要件が足りません。もう一度確認してください。"), color = 0xE67E22)
        em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
        await ctx.send(embed = em, delete_after=7)
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            if vc[0] == 1 and s[0] == 1:
                await Play_WAV(ctx,'要件が足りません。もう一度確認してください。',client_id,client_name, str(ctx.guild.id))
        
    if isinstance(error, commands.BotMissingPermissions):
        try:
            await ctx.message.delete()
        except:
            pass
        em = discord.Embed(title = "エラー", description = ("権限不足です。主さんに権限を確認もしくは足してもらってください。"), color = 0xE67E22)
        em.add_field(name = "**必要な権限：**", value = "メッセージの管理")
        em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
        await ctx.send(embed = em, delete_after=7)
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            if vc[0] == 1 and s[0] == 1:
                await Play_WAV(ctx,'送りすぎです。少し待ってください。',client_id,client_name, str(ctx.guild.id))
        
    if isinstance(error, commands.CommandOnCooldown):
        try:
            try:
                await ctx.message.delete()
            except:
                pass
            em = discord.Embed(title = "エラー", description = ("送りすぎです。少し待ってください。"), color = 0xE67E22)
            em.set_footer(icon_url = ctx.author.avatar_url, text = "呼んだ人: {}".format(ctx.author.display_name))
            await ctx.send(embed = em, delete_after=7)
            if not isinstance(ctx.channel, discord.channel.DMChannel):
                if vc[0] == 1 and s[0] == 1:
                    await Play_WAV(ctx,'送りすぎです。少し待ってください。',client_id,client_name, str(ctx.guild.id))
        except:
            pass

@client.event #Shout out to Togenom
async def on_voice_state_update(member, before, after):
    try:
        global vcconnected
        voice_state = member.guild.voice_client
        textch = last_textch_id[member.guild.id]
        vc = vcconnected[member.guild.id] 
        if len(voice_state.channel.members) == 1 and vc[0] == 1 and member.guild.id == textch[0]:
            settings == 0
            await voice_state.disconnect()
            vcconnected[member.guild.id] = [0]
            message = client.get_channel(textch[1])
            delete_all_server(str(member.guild.id))
            del queues[member.guild.id]
            del first_check[member.guild.id]
            print('')
            print('---------------------')
            em = discord.Embed(title = "バイバイ！", description = ("誰もいなくなったから降ります。ありがとうございました。"), color = 0xE67E22)
            print('(' + str(member.guild.name) + ')にあるボイチャにて誰もいなくなったので切断')
            print('#切断')
            print('---------------------')
            await message.send(embed = em, delete_after=7)
    except:
        pass

async def Play_WAV(STATUS, Msg, Message_Author, Username, guildid):
    global counter
    counter += 1
    if counter == 5001:
        counter = 1
    if int(Message_Author) == int(client.user.id) and str(Msg) == str(Leave_Message):
        global vcconnected
        vcconnected[STATUS.guild.id] = [0]
    inputText, file_num = creat_WAV(Msg, Message_Author, Username, guildid, counter) #WAV生成
    global queues
    queue = queues[STATUS.guild.id]
    first = first_check[STATUS.guild.id]
    voice = get(client.voice_clients, guild=STATUS.guild)
    queue.append('(' + str(file_num) + ').wav')
    queue.append(str(inputText))
    if not voice.is_playing() or first[0] == 0:
        Current_WAV = queue.pop(0)
        Current_Text = queue.pop(0)
        await Play(STATUS, Current_WAV, Current_Text)
    
async def Play(STATUS, Current_WAV, Current_Text):
    global first_check
    global queues
    queue = queues[STATUS.guild.id]
    first = first_check[STATUS.guild.id]
    if first[0] == 0:
        first_check[STATUS.guild.id] = [1]
    voice = get(client.voice_clients, guild=STATUS.guild)
    if not voice.is_playing():
        audio = discord.FFmpegPCMAudio(f'{CONFIG_PREFIX}/output/' + Current_WAV)
        print('')
        print('----------voice_start_[' + Current_WAV + ']----------')
        voice.play(audio)
        print(Current_Text)
        print('----------voice__end__[' + Current_WAV + ']----------')
        while voice.is_playing():
            await asyncio.sleep(0.1)
        if len(queue) > 0:
            Next_WAV = queue.pop(0) 
            Next_Text = queue.pop(0)
            await Play(STATUS, Next_WAV, Next_Text)
#---------------------------------------------------------------------------
#Thank you to Yhay81
def remove_mention(message):
    Msg = message.content
    if message.mentions:
        match = re.search(r'<@(\d+)>', Msg)
        while match:
            Msg = re.sub(r'<@(\d+)>', get_member(message, match.expand(r'\1')), Msg, count = 1)
            match = re.search(r'<@(\d+)>', Msg)
    if message.mentions:
        match = re.search(r'<@!(\d+)>', Msg)
        while match:
            Msg = re.sub(r'<@!(\d+)>', get_member(message, match.expand(r'\1')), Msg, count = 1)
            match = re.search(r'<@!(\d+)>', Msg)
    if message.role_mentions:
        match = re.search(r'<@&(\d+)>', Msg)
        while match:
            Msg = re.sub(r'<@&(\d+)>', get_role(message, match.expand(r'\1')), Msg, count = 1)
            match = re.search(r'<@&(\d+)>', Msg)
    if message.channel_mentions:
        match = re.search(r'<#(\d+)>', Msg)
        while match:
            Msg = re.sub(r'<#(\d+)>', get_channel(message, match.expand(r'\1')), Msg)
            match = re.search(r'<#(\d+)>', Msg)
    
    s = settings[message.guild.id]
    if s[1] == 1:      
        pattern = r'@here'
        Msg = re.sub(pattern,'ヒア',Msg)   # 置換処理
        pattern = r'@everyone'
        Msg = re.sub(pattern,'エブリワン',Msg)   # 置換処理
            
    return Msg

def get_member(message, member_id):
    members = message.mentions
    s = settings[message.guild.id]
    for member in members:
        if s[1] == 1 and int(member.id) == int(member_id):
            if member.nick:
                return member.nick
            else:
                return member.name
    return ""

def get_role(message, role_id):
    roles = message.role_mentions
    s = settings[message.guild.id]
    for role in roles:    
        if s[1] == 1 and int(role.id) == int(role_id):
            return role.name
    return ""

def get_channel(message, channel_id):
    channels = message.channel_mentions
    s = settings[message.guild.id]
    for channel in channels:
        if s[1] == 1 and int(channel.id) == int(channel_id):
            return channel.name
    return ""
  
#---------------------------------------------------------------------------  
async def blacklisted(STATUS):
    em = discord.Embed(title = "ブラックリスト", description = "ブラックリストに登録されています。そのコマンドは使えません。", color = 0xE67E22)
    em.set_footer(icon_url = STATUS.author.avatar_url, text = "呼んだ人: {}".format(STATUS.author.display_name))
    await STATUS.send(embed = em, delete_after=10)
    s = settings[STATUS.guild.id]
    if s[0] == 1:
        await Play_WAV(STATUS,'ブラックリストに登録されています。そのコマンドは使えません。',client_id,client_name, str(STATUS.guild.id)) 

client.run(Bot_Key) #BotID
