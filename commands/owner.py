import discord
from discord.ext import commands
import PW
import aiomysql
import datetime
import asyncio


async def check_owner(ctx):
    if ctx.author.id in [289729741387202560]:
        return True
    else:
        embed = discord.Embed(
            title="⚠ 주의", description="관리자만 사용이 가능한 명령어에요!", color=0xd8ef56)
        await ctx.send(embed=embed)


class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.owner_list = [289729741387202560]
        self.noticechannels = []
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.set_db())

    async def set_db(self):
        self.conn_pool = await aiomysql.create_pool(host='127.0.0.1', user=PW.db_user, password=PW.db_pw, db='bot', autocommit=True, loop=self.loop,
                                                    minsize=2, maxsize=5, charset="utf8mb4")

    async def get_notice_channels(self):
        allserver = []
        self.noticechannels = []
        allserver = self.bot.guilds
        for b in allserver:
            for i in b.channels:
                if "bot-announcement" in i.name or "bot_announcement" in i.name or "봇-공지" in i.name or "봇_공지" in i.name:
                    self.noticechannels.append(i)

        for c in self.noticechannels:
            try:
                allserver.remove(c.guild)
            except:
                pass

        for b in allserver:
            for i in b.channels:
                if "bot-notice" in i.name or "bot_notice" in i.name:
                    self.noticechannels.append(i)
        for c in self.noticechannels:
            try:
                allserver.remove(c.guild)
            except:
                pass

        for b in allserver:
            for i in b.channels:
                if "notice" in i.name or "공지" in i.name:
                    self.noticechannels.append(i)
        for c in self.noticechannels:
            try:
                allserver.remove(c.guild)
            except:
                pass

        self.noserver = []
        for b in allserver:
            for i in b.channels:
                if "announcement" in i.name or "annoucement" in i.name:
                    self.noticechannels.append(i)

        for c in self.noticechannels:
            try:
                allserver.remove(c.guild)
            except:
                pass
        for a in allserver:
            self.noserver.append(a.name)

    @commands.command(name="경고보기", aliases=["내경고"])
    async def check_warn(self, ctx):
        if ctx.message.mentions == []:
            user = ctx.author
        else:
            user = ctx.message.mentions[0]
        
        async with self.conn_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""SELECT * FROM warn WHERE id = %s""", (str(user.id) ))
                row = await cur.fetchone()
                
        if row is None:
            warns = 0
            embed=discord.Embed(title="✅ 경고 조회", description="%s 님의 경고를 불러옵니다." %(user.mention) ,color=0x1dc73a )
            embed.add_field(name="경고 수", value=str(warns) + "회" )
            embed.set_footer(text="5회 이상 경고 발생시 제제 처리됩니다.")

        else:
            warns = row[1]
            embed=discord.Embed(title="✅ 경고 조회", description="%s 님의 경고를 불러옵니다." %(user.mention) ,color=0x1dc73a )
            embed.add_field(name="경고 수", value=str(warns) + "회" )
            embed.set_footer(text="5회 이상 경고 발생시 제제 처리됩니다.")

        await ctx.send(embed=embed)

    @commands.command(name="경고추가", hidden=True)
    @commands.check(check_owner)
    async def add_warn(self, ctx, user:discord.Member):
        async with self.conn_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""SELECT * FROM warn WHERE id = %s""", (str(user.id) ))
                row = await cur.fetchone()
                
                if row is None:
                    warns = 1
                    await cur.execute("""INSERT INTO warn (id, times) VALUES (%s, %s)""", (str(user.id), 1 ))
                else:
                    warns = row[1] + 1
                    await cur.execute("""UPDATE warn SET times=%s WHERE id = %s""", (warns, str(user.id)))

        embed=discord.Embed(title="✅ 경고 추가", description="%s 님의 경고를 성공했어요." %(user.mention) ,color=0x1dc73a )
        embed.add_field(name="경고 수", value=str(warns) + "회" )
        embed.set_footer(text="5회 이상 경고 발생시 제제 처리됩니다.")
        await ctx.send(embed=embed)


    @commands.command(name="리로드", aliases=["재로드"], hidden=True)
    @commands.check(check_owner)
    async def reload(self, ctx, module):
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
            embed = discord.Embed(
                title="✅ 재로드 성공", description="**{}** 모듈 재로드 완료!".format(module), color=0x1dc73a)
            await ctx.send(embed=embed)
        except Exception as error:
            await ctx.send("실패 {}".format(error))

    @commands.command(name="언로드", hidden=True)
    @commands.check(check_owner)
    async def unload(self, ctx, module):
        try:
            self.bot.unload_extension(module)
            embed = discord.Embed(
                title="✅ 언로드 성공", description="**{}** 모듈 언로드 완료!".format(module), color=0x1dc73a)
            await ctx.send(embed=embed)
        except Exception as error:
            await ctx.send("실패 {}".format(error))

    @commands.command(name="로드", hidden=True)
    @commands.check(check_owner)
    async def load(self, ctx, module):
        try:
            self.bot.load_extension(module)
            embed = discord.Embed(
                title="✅ 로드 성공", description="**{}** 모듈 로드 완료!".format(module), color=0x1dc73a)
            await ctx.send(embed=embed)
        except Exception as error:
            await ctx.send("실패 {}".format(error))

    @commands.command(name="공지", hidden=True, rest_is_raw=True)
    @commands.check(check_owner)
    async def notice(self, ctx, *, args):
        written_time = datetime.datetime.utcnow()
        contents = args.lstrip()
        if contents == "":
            await ctx.send("내용이 없습니다!")
        else:
            notice_embed = discord.Embed(title="📢 공지", description="{}".format(
                contents), color=0x1dc73a, timestamp=written_time)
            notice_embed.set_footer(
                icon_url=ctx.author.avatar_url, text="문의는 {}".format(ctx.author))
            await ctx.send(embed=notice_embed)
            tg = await ctx.send("다음과 같이 보내집니다. 보내시겠습니까?")
            await tg.add_reaction("⭕")
            await tg.add_reaction("❌")

            def notice_check(reaction, user):
                return user == ctx.author and str(reaction) in ["⭕", "❌"] and tg.id == reaction.message.id

            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=notice_check)
            if str(reaction) == "⭕":
                embed = discord.Embed(
                    title="🔎 채널 검색", description="보낼 채널을 검색하고 있어요.", color=0x1dc73a)
                edit_tg = await ctx.send(embed=embed)
                await self.get_notice_channels()
                embed = discord.Embed(title="✅ 채널 검색 완료", description="검색 완료! {}개의 채널에 전송을 시작합니다.".format(
                    len(self.noticechannels)), color=0x1dc73a)
                await edit_tg.edit(embed=embed)
                fail = 0
                for i in self.noticechannels:
                    try:
                        await i.send(embed=notice_embed)
                    except:
                        fail += 1

                embed = discord.Embed(title="✅ 공지 전송 완료", description="공지 완료! {}개 중 {}개 실패.".format(
                    len(self.noticechannels), fail), color=0x1dc73a)
                await edit_tg.edit(embed=embed)

            else:
                await ctx.send("전송을 취소합니다.")

    @commands.command(name="db", rest_is_raw=True, hidden=True)
    @commands.check(check_owner)
    async def db_debug(self, ctx, *, args):
        try:
            query = args.lstrip()
            async with self.conn_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query)
                    row = await cur.fetchall()
            if row is None or row == []:
                embed=discord.Embed(title="✅ 성공", description="결과값이 없습니다.",color=0x1dc73a )
            else:
                embed=discord.Embed(title="✅ 성공", description="%s" %(str(row)),color=0x1dc73a )
            await ctx.send(embed=embed)
        except Exception as error:
            embed=discord.Embed(title="⚠ 주의", description="오류 발생!\n```%s```" %(error),color=0xd8ef56)
            await ctx.send(embed=embed)

    @commands.command(name="강제초대", rest_is_raw=True, hidden=True)
    @commands.check(check_owner)
    async def force_invite(self, ctx, *, args):
        try:
            channelid = args.lstrip()
            invite = self.bot.get_channel(int(channelid))
            link = await invite.create_invite(max_uses=1, reason="봇의 관리자가 여러가지 요인으로 현재 서버에 초대가 필요하다고 판단되어 초대링크가 생성되었습니다.")
            await ctx.send("{} (max_uses=1)".format(link))
        except Exception as error:
            await ctx.send("{}".format(error))

    @commands.command(name="채널전송", rest_is_raw=True, hidden=True)
    @commands.check(check_owner)
    async def send_to_channel(self, ctx, *, args):
        try:
            contents = args.lstrip()
            await ctx.send("전송할 채널 아이디를 입력해주세요!")
            def sendcheck(a):
                return a.author == ctx.author
            answer = await self.bot.wait_for('message', check=sendcheck, timeout=30)
            channel = self.bot.get_channel(int(answer.content))
            embed=discord.Embed(title="📩 개발자로부터의 메시지", description="개발자에게 메시지가 도착하였습니다.",color=0x237ccd, timestamp=datetime.datetime.utcnow())
            embed.add_field(name="내용", value=contents)
            embed.set_footer(text="BGM#0970", icon_url="%s" %(self.bot.get_user(ctx.author.id).avatar_url) )
            await channel.send(embed=embed)
            await ctx.send("전송 완료!")
        except Exception as error:
            await ctx.send("{}".format(error))

    @commands.command(name="유저전송", rest_is_raw=True, hidden=True)
    @commands.check(check_owner)
    async def send_to_user(self, ctx, *, args):
        try:
            contents = args.lstrip()
            await ctx.send("전송할 유저 아이디를 입력해주세요!")
            def sendcheck(a):
                return a.author == ctx.author
            answer = await self.bot.wait_for('message', check=sendcheck, timeout=30)
            channel = self.bot.get_user(int(answer.content))
            embed=discord.Embed(title   ="📩 개발자로부터의 메시지", description="개발자에게 메시지가 도착하였습니다.",color=0x237ccd, timestamp=datetime.datetime.utcnow())
            embed.add_field(name="내용", value=contents)
            embed.set_footer(text="BGM#0970", icon_url="%s" %(self.bot.get_user(ctx.author.id).avatar_url) )
            await channel.send(embed=embed)
            await ctx.send("전송 완료!")
        except Exception as error:
            await ctx.send("{}".format(error))

def setup(bot):
    bot.add_cog(Owner(bot))
