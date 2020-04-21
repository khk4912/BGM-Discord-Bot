import discord
from discord.ext import commands
import asyncio
import typing
from logs import Logs
from utils.embed import Embed
import aiomysql
import PW


class Admin(commands.Cog):
    def __init__(self, bot):
        super()
        self.bot = bot
        self.logger = Logs.create_logger(self)
        self.loop = asyncio.get_event_loop()
        self.conn_pool = self.loop.create_task(self.set_db())

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
        if ctx.guild is None:
            return None

        if ctx.author.guild_permissions.administrator:
            return True

        else:
            embed = Embed.warn("주의", "이 명령어는 서버에 **관리자 권한**이 있어야 사용할 수 있어요!")
            await ctx.send(embed=embed)

    @commands.command(name="뮤트")
    @commands.guild_only()
    async def mute_user(self, ctx, member: discord.Member):
        await ctx.channel.set_permissions(member, send_messages=False)
        embed = Embed.check("유저 뮤트", "해당 유저를 이 채널에서 뮤트했어요!")
        await ctx.send(embed=embed)

    @commands.command(name="언뮤트", aliases=["뮤트해제"])
    @commands.guild_only()
    async def unmute_user(self, ctx, member: discord.Member):
        await ctx.channel.set_permissions(member, send_messages=None)
        embed = Embed.check("유저 언뮤트", "해당 유저를 이 채널에서 언뮤트했어요!")
        await ctx.send(embed=embed)

    @commands.command(name="전체뮤트", aliases=["채널뮤트"])
    @commands.guild_only()
    async def channel_mute(self, ctx):
        await ctx.channel.set_permissions(
            ctx.guild.default_role, send_messages=False
        )
        embed = Embed.check("채널 얼리기", "관리자를 제외한 모든 유저는 이제 이 채널에 메시지를 보낼 수 없어요.")
        await ctx.send(embed=embed)

    @commands.command(name="전체언뮤트", aliases=["전체뮤트해제", "전체뮤트 해제", "채널뮤트해제"])
    @commands.guild_only()
    async def channel_unmute(self, ctx):
        await ctx.channel.set_permissions(
            ctx.guild.default_role, send_messages=None
        )
        embed = Embed.check("채널 얼리기 해제", "채널 얼리기를 해제했어요.")
        await ctx.send(embed=embed)

    @commands.command(name="슬로우모드")
    @commands.guild_only()
    async def set_slowmode(self, ctx, seconds: typing.Union[int]):
        if seconds > 0 and seconds < 21601:
            await ctx.channel.edit(slowmode_delay=seconds)
            embed = discord.Embed(
                title="🐌 슬로우모드",
                description="{}의 슬로우모드를 {}초로 설정했어요.".format(
                    ctx.channel.mention, seconds
                ),
                color=0x1DC73A,
            )
            embed.set_footer(text="슬로우모드 해제는 `봇 슬로우해제`를 사용하세요.")
            await ctx.send(embed=embed)

        else:
            embed = Embed.warn("주의", "슬로우모드는 1~21600초 사이로만 설정할 수 있어요.")
            await ctx.send(embed=embed)

    @commands.command(name="슬로우해제")
    @commands.guild_only()
    async def unset_slowmode(self, ctx):
        await ctx.channel.edit(slowmode_delay=0)
        embed = discord.Embed(
            title="🐌 슬로우모드",
            description="{}의 슬로우모드를 해제했어요.".format(ctx.channel.mention),
            color=0x1DC73A,
        )
        await ctx.send(embed=embed)

    @commands.command(name="밴", aliases=["차단", "벤"])
    @commands.guild_only()
    async def ban(self, ctx, member: discord.Member):
        await ctx.guild.ban(
            member,
            reason=str(ctx.author) + "님의 명령어 사용으로 인해 밴 당하셨습니다.",
            delete_message_days=7,
        )
        embed = Embed.check(title="유저 밴", description="유저의 밴을 완료했어요.")
        await ctx.send(embed=embed)

    @commands.command(name="킥", aliases=["강제퇴장", "강퇴"])
    @commands.guild_only()
    async def kick(self, ctx, member: discord.Member):

        await ctx.guild.kick(
            member, reason=str(ctx.author) + "님의 명령어 사용으로 인해 킥 당하셨습니다."
        )
        embed = Embed.check(title="멤버 킥", description="선택한 유저를 추방했어요.")
        await ctx.send(embed=embed)

    @commands.command(name="지우기", aliases=["삭제"])
    @commands.guild_only()
    async def delete_message(self, ctx, amount: typing.Union[int]):
        if amount > 0 and amount <= 100:
            deleted_message = await ctx.channel.purge(limit=amount)
            embed = Embed.check(
                title="메시지 삭제",
                description="%s개의 메시지를 지웠어요." % len(deleted_message),
            )
            await ctx.send(embed=embed, delete_after=3)
        else:
            embed = Embed.warn(
                title="오류 발생", description="지우는 메시지의 개수는 1개~100개여야 해요."
            )
            await ctx.send(embed=embed, delete_after=3)

    @commands.command(name="웰컴설정", aliases=["환영설정"])
    async def set_welcome_message(self, ctx):
        async with self.conn_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """SELECT id, welcome, welcome_message FROM welcome WHERE id=%s""",
                    (ctx.guild.id),
                )
                row = await cur.fetchone()

        if row is None or row[1] == 0:
            embed = discord.Embed(
                title="📝 웰컴 설정",
                description="현재 웰컴 메시지가 설정되어 있지 않아요. 추가하시려면 ✅ 이모티콘을 눌러주세요.",
            )
            msg = await ctx.send(embed=embed)
            await msg.add_reaction("✅")

            def posi_check(reaction, user):
                # if user.is_bot: return False
                return (
                    user == ctx.author
                    and str(reaction.emoji) == "✅"
                    and msg.id == reaction.message.id
                )

            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", timeout=60.0, check=posi_check
                )
                if str(reaction) == "✅":
                    edit = True
                else:
                    return
            except:
                return

        else:
            embed = discord.Embed(
                title="📝 웰컴 설정",
                description="현재 웰컴 메시지는 다음과 같습니다.\n```%s```\n\n 수정하시려면 ✅ 이모티콘을, 제거하시려면 ❌ 이모티콘을 클릭해주세요. "
                % (row[2]),
            )
            embed.set_footer(
                text="메시지는 `서버 설정 > SYSTEM MESSAGES CHANNEL`에 보내집니다."
            )
            msg = await ctx.send(embed=embed)
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")

            def posi_check2(reaction, user):
                # # if user.is_bot: return False
                # print(user, ctx.author, msg.id, reaction.message.id)
                return (
                    user == ctx.author
                    and (
                        str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌"
                    )
                    and msg.id == reaction.message.id
                )

            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", timeout=60.0, check=posi_check2
                )
                if str(reaction) == "✅":
                    edit = True
                    print(edit)
                else:
                    edit = False
            except:
                await ctx.send("타임아웃으로 취소되었어요.")
                return

        if edit:
            embed = discord.Embed(
                title="📝 웰컴 설정",
                description="유저가 들어올때 봇이 보낼 메시지를 설정해주세요. 취소하시려면 `봇 취소` 를 입력하세요.\n\n{멘션} > 유저를 언급합니다.\n{서버이름} > 서버 이름을 표시합니다.",
            )
            await ctx.send(embed=embed)

            def check_msg(m):
                return m.channel == ctx.channel and m.author == ctx.author

            msg = await self.bot.wait_for("message", check=check_msg)
            if msg.content == "봇 취소":
                await ctx.send("취소되었습니다.")
            else:
                async with self.conn_pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute(
                            """INSERT INTO welcome (id, welcome, welcome_message) VALUES (%s, %s, %s)  ON DUPLICATE KEY UPDATE welcome=%s, welcome_message=%s;""",
                            (ctx.guild.id, 1, msg.content, 1, msg.content),
                        )
                embed = discord.Embed(
                    title="✅ 웰컴 메시지",
                    description="```%s```\n로 웰컴 메시지가 설정되었습니다." % (msg.content),
                    color=0x1DC73A,
                )
                embed.set_footer(
                    text="메시지는 `서버 설정 > SYSTEM MESSAGES CHANNEL`에 보내집니다."
                )

                await ctx.send(embed=embed)

        else:
            async with self.conn_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        """INSERT INTO welcome (id, welcome, welcome_message) VALUES (%s, %s, %s)  ON DUPLICATE KEY UPDATE welcome='%s';""",
                        (ctx.guild.id, 0, None, 0),
                    )
                embed = discord.Embed(
                    title="✅ 웰컴 메시지",
                    description="웰컴 메시지 사용이 중지되었습니다.",
                    color=0x1DC73A,
                )
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Admin(bot))
