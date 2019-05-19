import discord
from discord.ext import commands
import TOKEN
import asyncio
import PW
import aiomysql
import datetime
import traceback
import sys
import background
import pickle
import logging 


async def set_db():
    global conn_pool
    conn_pool = await aiomysql.create_pool(host='127.0.0.1', user=PW.db_user, password=PW.db_pw, db='bot', autocommit=True, loop=loop,
                                                minsize=2, maxsize=3, charset="utf8mb4")


async def check_cc(message):

    command = message.content[2:]
    async with conn_pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""SELECT * FROM cc WHERE server = %s AND command = %s""", (str(message.guild.id), command))
            row = await cur.fetchone()
            # print(row)
            if not row is None:
                await message.channel.send(row[2])

def is_owner():
    async def predicate(ctx):
        return ctx.author.id == 289729741387202560
    return commands.check(predicate)

async def message_helper(message):
    if message.guild is None:
        message_channel = "DM"
        message_channel_id = "DM"
        guild = "DM"
        guild_id = "DM"
    else:
        message_channel = message.channel.name
        message_channel_id = message.channel.id
        guild = message.guild.name
        guild_id = message.guild.id

    text = """
{}
Server : {} ({})
Channel : {} ({})
User : {}
Content : {}
Embed : {}
File : {}
             """.format(datetime.datetime.now(), guild, guild_id,
                        message_channel, message_channel_id, message.content,
                        message.author.name + "#" + message.author.discriminator, message.embeds,
                        message.attachments)
    print(text)
formatter = logging.Formatter('[%(levelname)s]: %(message)s')

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
filehandler = logging.FileHandler('bot_log.txt', 'w')
streamhandler = logging.StreamHandler()
filehandler.setFormatter(formatter)
streamhandler.setFormatter(formatter)

logger.addHandler(filehandler)
logger.addHandler(streamhandler)

bot = commands.AutoShardedBot(command_prefix=["봇 ", "봇"])
loop = asyncio.get_event_loop()
conn_pool_task = loop.create_task(set_db())
backgruond_task = loop.create_task(background.change_activity(bot))
afk = {}
blacklist = []
with open('blacklist.pickle','rb') as f:
   blacklist = pickle.load(f)

@bot.event
async def on_ready():
    print("=====")
    print("{}로 로그인 완료!".format(bot.user.name))
    print("=====")


# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.CheckFailure):
#         return
@bot.event
async def on_member_join(member):
    loop = asyncio.get_event_loop()
    conn = await aiomysql.connect(host='127.0.0.1',
                                  user=PW.db_user, password=PW.db_pw, db="bot", autocommit=True,
                                  loop=loop, charset="utf8mb4")

    async with conn.cursor() as cur:
        try:
            await cur.execute("""SELECT id, welcome, welcome_message FROM welcome WHERE id = %s""", (member.guild.id))
            row = await cur.fetchone()
            if not row:
                return
        except:
            return
        if row[1] == 1:
            tg = row[2]
            tg = tg.replace("{멘션}", member.mention)
            tg = tg.replace("{서버이름}", member.guild.name)
            await member.guild.system_channel.send(tg)


@bot.event
async def on_message(message):

    await message_helper(message)

    if message.author.bot or str(message.author.id) in blacklist:
        return

    if message.author.id in afk.keys():    
        get = afk[message.author.id]
        embed=discord.Embed(title="👐 잠수 종료!", description="<@{}>님이 잠수를 종료하셨습니다.".format(message.author.id), color=get["color"], timestamp=get["utcstarttime"])
        embed.add_field(name="잠수 사유", value="{0}".format(get["reason"]), inline=True)
        del afk[message.author.id]
        await message.channel.send(embed=embed)

    if not message.author.bot:
        await bot.process_commands(message)

    if message.content.startswith("봇 "):
        await check_cc(message)



@bot.command(name="잠수", aliases=["afk"], rest_is_raw=True)
async def afk_define(ctx, *, args):
    if args is None or args == "":
        reason = "사유가 없습니다."
    else:
        reason = args.lstrip()

    try:
        author_color = ctx.author.colour
    except:
        author_color = 0x237ccd
    afk_start_time = datetime.datetime.now()
    afk_start_utc_time = datetime.datetime.utcnow()
    afk[ctx.author.id] = {"reason": reason, "starttime": afk_start_time,
                          "utcstarttime": afk_start_utc_time, "color": author_color}
    embed = discord.Embed(title="💤 잠수", description="<@{0}>님이 잠수를 시전하셨습니다.\n".format(
        ctx.author.id), color=author_color)
    embed.add_field(name="잠수 사유", value="{0}".format(reason), inline=False)
    embed.set_footer(text="{0}\n".format(afk_start_time))
    await ctx.send(embed=embed)
    
@bot.command(name="블랙추가", hidden=True)
@is_owner()
async def add_to_black(ctx):
    user = str(ctx.message.mentions[0].id)
    blacklist.append(user)
    thefile = open('blacklist.pickle', mode='w+')
    thefile.write("")
    thefile.close
    try:
        with open('blacklist.pickle','ab') as f:
            pickle.dump(blacklist,f)
    except:
        pass

    await ctx.send("<@%s>를 블랙리스트에 추가했어." %user)
            

    
@bot.command(name="블랙삭제", hidden=True)
@is_owner()
async def rest_black(ctx):
    a = ctx.message.content
    a = a[7:]
    a = a.replace("<", "")
    a = a.replace("@", "")
    a = a.replace("!", "")
    a = a.replace(">", "")
    blacklist.remove(a)
    f = open("blacklist.pickle", mode="w+")
    f.write("")
    f.close()
    try:
        with open('blacklist.pickle','ab') as f:
            pickle.dump(blacklist, f)
    except:
        pass
    
    await ctx.send("<@{}> 블랙에서 삭제함.".format(a) )
   
@bot.command(name="블랙보기", hidden=True)
@is_owner()
async def show_black(ctx):
    await ctx.send("블랙리스트 목록 : %s" %blacklist)


for i in TOKEN.initial_extensions:
    bot.load_extension(i)


bot.run(TOKEN.bot_token)
