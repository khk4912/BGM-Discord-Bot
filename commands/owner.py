import discord
from discord.ext import commands
import asyncio
import typing
from logs import Logs
import datetime
import traceback
from utils.embed import Embed
import aiomysql
import PW


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.owner_list = [289729741387202560]
        self.notice_channels = []
        self.logger = Logs.create_logger(self)
        self.loop = asyncio.get_event_loop()
        self.conn_pool = self.loop.create_task(self.set_db())
        self.insignia = {
            "멋짐": "https://cdn.discordapp.com/emojis/664836978520621076.png?v=1",
            "주인": "https://cdn.discordapp.com/emojis/664837274864844857.png?v=1",
            "라이타운": "https://cdn.discordapp.com/emojis/490097210168573962.png?v=1",
            "안해": "https://cdn.discordapp.com/emojis/490097831701381132.png?v=1",
        }

    async def set_db(self):
        self.conn_pool = await aiomysql.create_pool(
            host="127.0.0.1",
            user=PW.db_user,
            password=PW.db_pw,
            db="bot",
            autocommit=True,
            loop=self.loop,
            minsize=2,
            maxsize=3,
            charset="utf8mb4",
        )

    async def cog_check(self, ctx):
        if ctx.author.id in self.owner_list:
            return True
        else:
            embed = Embed.warn("주의", "이 명령어는 봇 오너만 사용이 가능해요.")
            await ctx.send(embed=embed)

    async def get_insignia(self, id) -> bool:
        try:
            async with self.conn_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        """SELECT * FROM insignia where id=%s""", (str(id))
                    )
                    row = await cur.fetchone()

            if row is None:
                return None
            return row[1]

        except:
            return False

    async def update_insignia(self, id, add) -> bool:
        try:
            async with self.conn_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    row = await self.get_insignia(id)
                    if row is None:
                        await cur.execute(
                            """INSERT INTO insignia (id, what) VALUES (%s, %s)""",
                            (id, add),
                        )
                    else:
                        await cur.execute(
                            """UPDATE insignia SET what=%s WHERE id=%s""",
                            (add, id),
                        )
            return True

        except:
            return False

    async def delete_insignia(self, id) -> bool:
        try:
            async with self.conn_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    row = await self.get_insignia(id)
                    if row is None:
                        return True
                    else:
                        await cur.execute(
                            """DELETE FROM insignia WHERE id=%s""", (id)
                        )
            return True

        except:
            return False

    def get_notice_channels(self):
        self.notice_channels = []
        priority_names = ["봇-공지", "봇공지", "공지", "notice", "bot-notice"]
        for guild in self.bot.guilds:
            for name in priority_names:
                channel = discord.utils.find(
                    lambda x: name in x.name, guild.text_channels
                )
                if channel is not None:
                    self.notice_channels.append(channel)
                    break

        print(self.notice_channels)

    @commands.command(name="리로드", aliases=["재로드"])
    async def reload(self, ctx, module=None):
        # try:
        if module is None:
            return
        self.bot.unload_extension(module)
        self.bot.load_extension(module)
        embed = discord.Embed(
            title="✅ 성공",
            description="**{}** 리로드 완료.".format(module),
            color=0x1DC73A,
        )
        await ctx.send(embed=embed)
        # except Exception as error:
        #     await ctx.send("실패 {}".format(error))

    @commands.command(name="언로드", hidden=True)
    async def unload(self, ctx, module=None):
        if module is None:
            return
        try:
            self.bot.unload_extension(module)
            embed = discord.Embed(
                title="✅ 언로드 성공",
                description="**{}** 언로드 완료.".format(module),
                color=0x1DC73A,
            )
            await ctx.send(embed=embed)
        except Exception as error:
            await ctx.send("실패 {}".format(error))

    @commands.command(name="로드", hidden=True)
    async def load(self, ctx, module=None):
        if module is None:
            return
        try:
            self.bot.load_extension(module)
            embed = discord.Embed(
                title="✅ 성공",
                description="**{}** 모듈 로드 완료.".format(module),
                color=0x1DC73A,
            )
            await ctx.send(embed=embed)
        except Exception as error:

            await ctx.send("실패 {}".format(error))

    @commands.command(name="공지", hidden=True)
    async def notice(self, ctx, *, contents=None):
        written_time = datetime.datetime.utcnow()
        if contents is None:
            return await ctx.send("내용이 없습니다!")
        else:
            notice_embed = discord.Embed(
                title="📢 공지",
                description="{}".format(contents),
                color=0x1DC73A,
                timestamp=written_time,
            )
            notice_embed.set_footer(
                icon_url=ctx.author.avatar_url, text="{}".format(ctx.author)
            )
            await ctx.send(embed=notice_embed)
            tg = await ctx.send("다음과 같이 보내집니다. 보내시겠습니까?")
            await tg.add_reaction("⭕")
            await tg.add_reaction("❌")

            def notice_check(reaction, user):
                return (
                    user == ctx.author
                    and str(reaction) in ["⭕", "❌"]
                    and tg.id == reaction.message.id
                )

            reaction, user = await self.bot.wait_for(
                "reaction_add", timeout=60.0, check=notice_check
            )
            if str(reaction) == "⭕":
                embed = discord.Embed(
                    title="🔎 채널 검색",
                    description="보낼 채널을 검색하고 있어요.",
                    color=0x1DC73A,
                )
                edit_tg = await ctx.send(embed=embed)
                await self.get_notice_channels()
                embed = discord.Embed(
                    title="✅ 채널 검색 완료",
                    description="검색 완료! {}개의 채널에 전송을 시작합니다.".format(
                        len(self.notice_channels)
                    ),
                    color=0x1DC73A,
                )
                await edit_tg.edit(embed=embed)
                fail = 0
                for i in self.notice_channels:
                    try:
                        await i.send(embed=notice_embed)
                    except:
                        fail += 1

                embed = discord.Embed(
                    title="✅ 공지 전송 완료",
                    description="공지 완료! {}개 중 {}개 실패.".format(
                        len(self.notice_channels), fail
                    ),
                    color=0x1DC73A,
                )
                await edit_tg.edit(embed=embed)

            else:
                await ctx.send("전송을 취소합니다.")

    @commands.command(name="db", hidden=True)
    async def db_debug(self, ctx, *, args):
        try:
            query = args.lstrip()
            async with self.conn_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query)
                    row = await cur.fetchall()
            if row is None or row == []:
                embed = discord.Embed(
                    title="✅ 성공", description="결과값이 없습니다.", color=0x1DC73A
                )
            else:
                embed = discord.Embed(
                    title="✅ 성공", description="%s" % (str(row)), color=0x1DC73A
                )
            await ctx.send(embed=embed)
        except Exception as error:
            embed = discord.Embed(
                title="⚠", description="```%s```" % (error), color=0xD8EF56,
            )
            await ctx.send(embed=embed)

    @commands.command(name="강제초대")
    async def force_invite(self, ctx, channel_id: typing.Union[int]):
        try:
            target = self.bot.get_channel(channel_id)
            link = await target.create_invite(
                max_uses=1, reason="봇 오너 요청으로 일회용 서버 초대 링크를 생성했어요."
            )
            await ctx.send("{} (max_uses=1)".format(link))
        except Exception as error:
            await ctx.send("{}".format(error))

    @commands.command(name="채널전송")
    async def send_to_channel(
        self, ctx, channel_id: typing.Union[int], *, contents
    ):
        channel = self.bot.get_channel(channel_id)
        embed = discord.Embed(
            title="📩 개발자로부터의 메시지",
            description="개발자에게 메시지가 도착하였습니다.",
            color=0x237CCD,
            timestamp=datetime.datetime.utcnow(),
        )
        embed.add_field(name="내용", value=contents)
        embed.set_footer(
            text="BGM#0970",
            icon_url="%s" % (self.bot.get_user(ctx.author.id).avatar_url),
        )
        await channel.send(embed=embed)
        await ctx.send("전송 완료!")

    @commands.command(name="유저전송")
    async def send_to_user(self, ctx, user_id: typing.Union[int], *, contents):
        channel = self.bot.get_user(user_id)
        embed = discord.Embed(
            title="📩 개발자로부터의 메시지",
            description="개발자에게 메시지가 도착하였습니다.",
            color=0x237CCD,
            timestamp=datetime.datetime.utcnow(),
        )
        embed.add_field(name="내용", value=contents)
        embed.set_footer(
            text="BGM#0970",
            icon_url="%s" % (self.bot.get_user(ctx.author.id).avatar_url),
        )
        await channel.send(embed=embed)
        await ctx.send("전송 완료!")

    @commands.command(name="휘장목록", hidden=True)
    async def show_insignia(self, ctx):
        embed = discord.Embed(
            title="✅ 현재 존재하는 휘장들",
            description="얻을 수 있는 모든 휘장을 보여줍니다.",
            color=0x1DC73A,
        )
        for i in self.insignia.keys():
            embed.add_field(name=i, value=self.insignia[i])
        await ctx.send(embed=embed)

    @commands.command(name="휘장부여", hidden=True)
    async def give_insignia(self, ctx, user_id: typing.Union[int], what):
        await self.update_insignia(id, self.insignia[what])
        await ctx.send("부여 성공.")

    @commands.command(name="휘장삭제", hidden=True)
    async def deletee_insignia(self, ctx, user_id: typing.Union[int]):
        await self.delete_insignia(user_id)
        await ctx.send("삭제 성공.")

    @commands.command(name="exec", aliases=["eval"], hidden=True)
    async def eval(self, ctx, *, cmd):
        try:
            context = {"ctx": ctx, "self": self, "discord": discord}
            a = await self.loop.run_in_executor(None, eval, cmd, context)
            await ctx.send(a)
        except:
            await ctx.send(traceback.format_exc())

    @commands.command(name="task", hidden=True)
    async def create(self, ctx, *, cmd):
        try:
            context = {"ctx": ctx, "self": self, "discord": discord}
            coro = await self.loop.run_in_executor(None, eval, cmd, context)
            asyncio.ensure_future(coro)

        except:
            await ctx.send(traceback.format_exc())


def setup(bot):
    bot.add_cog(Owner(bot))
