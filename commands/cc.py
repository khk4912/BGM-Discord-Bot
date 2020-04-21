import discord
from discord.ext import commands
import asyncio
import datetime
import aiomysql
import PW
from logs import Logs
from EZPaginator import Paginator


async def check_admin(ctx):
    if (
        ctx.author.guild_permissions.administrator
        or ctx.author.id == 289729741387202560
    ):
        return True

    else:

        embed = discord.Embed(
            title="⚠ 주의",
            description="서버에 관리자 권한이 있어야 사용이 가능해요.",
            color=0xD8EF56,
        )
        await ctx.send(embed=embed)


class CC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = Logs.create_logger(self)
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.set_db())

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

    @commands.group(name="커스텀", aliases=["커"])
    async def custom(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    @custom.command(name="보기", aliases=["보", "목록", "목"])
    async def show_cc(self, ctx):
        async with self.conn_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """SELECT command FROM cc WHERE server = %s""",
                    (str(ctx.guild.id)),
                )
                row = await cur.fetchall()

        if row != ():
            if len(row) <= 100:
                text = " | ".join(_[0] for _ in row)
                embed = discord.Embed(
                    title="✅ 커스텀 보기", description="%s" % (text), color=0x1DC73A,
                )
                embed.set_footer(text="총 CC개수는 {}개입니다.".format(len(row)))
                await ctx.send(embed=embed)

            else:
                embeds = []
                sep = 100
                row = [x[0] for x in row]
                new_row = [
                    row[i * sep : (i + 1) * sep]
                    for i in range((len(row) + sep - 1) // sep)
                ]
                total = len(new_row)
                for i in new_row:
                    text = " | ".join(i)
                    embed = discord.Embed(
                        title="✅ 커스텀 보기",
                        description="%s" % (text),
                        color=0x1DC73A,
                    )
                    embed.set_footer(
                        text="총 CC개수는 {}개입니다. ({} / {})".format(
                            len(row), new_row.index(i) + 1, total
                        )
                    )
                    embeds.append(embed)

                msg = await ctx.send(embed=embeds[0])
                page = Paginator(self.bot, msg, embeds=embeds)
                await page.start()

        else:
            embed = discord.Embed(
                title="✅ 커스텀 보기",
                description="이 서버엔 커스텀 명령어가 없어요!\n`봇 커스텀 추가 <명령어>/<대답>`으로 추가를 진행해보세요.",
                color=0x1DC73A,
            )
            await ctx.send(embed=embed)

    @custom.command(name="추가", aliases=["추"])
    @commands.check(check_admin)
    async def add_command(self, ctx, *, contents):
        split = contents.split("/", 1)
        if len(split) == 1:
            raise commands.BadArgument()
        command = split[0].strip()
        answer = split[1].strip()

        async with self.conn_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """SELECT command FROM cc WHERE server = %s AND command = %s""",
                    (str(ctx.guild.id), command),
                )
                row = await cur.fetchone()

        if row is not None:
            embed = discord.Embed(
                title="⚠ 주의",
                description="이미 존재하는 명령어에요. 수정하시려면 `봇 커스텀 수정 [명령어]/[봇의 대답]` 을 사용해주세요.",
                color=0xD8EF56,
            )
            return await ctx.send(embed=embed)

        async with self.conn_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """INSERT INTO cc (server, command, answer, who, datetime) VALUES (%s, %s, %s, %s, %s)""",
                    (
                        str(ctx.guild.id),
                        command,
                        answer,
                        str(ctx.author.id),
                        str(datetime.datetime.now()),
                    ),
                )
                embed = discord.Embed(
                    title="✅ 커스텀 추가",
                    description="커스텀 추가를 성공했어요.",
                    color=0x1DC73A,
                )
                embed.add_field(name="명령어", value=command)
                embed.add_field(name="봇의 대답", value=answer)
                await ctx.send(embed=embed)

    @custom.command(name="수정", aliases=["수"])
    @commands.check(check_admin)
    async def edit_cc(self, ctx, *, contents):
        split = contents.split("/", 1)
        if len(split) == 1:
            raise commands.BadArgument()
        command = split[0].strip()
        answer = split[1].strip()

        async with self.conn_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """SELECT command FROM cc WHERE server = %s AND command = %s""",
                    (str(ctx.guild.id), command),
                )
                row = await cur.fetchone()

        if row is not None:
            async with self.conn_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        """UPDATE cc SET answer=%s, who=%s, datetime=%s WHERE server=%s AND command=%s  """,
                        (
                            answer,
                            str(ctx.author.id),
                            str(datetime.datetime.now()),
                            str(ctx.guild.id),
                            str(command),
                        ),
                    )
                    embed = discord.Embed(
                        title="✅ 커스텀 수정",
                        description="커스텀 수정을 성공했습니다.",
                        color=0x1DC73A,
                    )
                    embed.add_field(name="명령어", value=command)
                    embed.add_field(name="수정된 봇의 대답", value=answer)
                    await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                title="⚠ 주의",
                description="선택하신 명령어가 존재하지 않아요.\n`봇 커스텀 추가 [명령어]/[봇의 대답]` 으로 추가를 해보세요!",
                color=0xD8EF56,
            )
            await ctx.send(embed=embed)

    @custom.command(name="삭제", aliases=["삭"])
    @commands.check(check_admin)
    async def del_cc(self, ctx, *, command):
        command = command.strip()
        async with self.conn_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """SELECT command FROM cc WHERE server = %s AND command = %s""",
                    (str(ctx.guild.id), command),
                )
                row = await cur.fetchone()

        if row is not None:
            async with self.conn_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        """DELETE FROM cc WHERE server = %s AND command = %s""",
                        (str(ctx.guild.id), command),
                    )
                    embed = discord.Embed(
                        title="✅ 커스텀 삭제",
                        description="커스텀 삭제를 성공했어요.",
                        color=0x1DC73A,
                    )
                    embed.add_field(name="삭제한 명령어", value=command)
                    await ctx.send(embed=embed)

    @custom.command(name="초기화", aliases=["초"])
    @commands.check(check_admin)
    async def reset_cc(self, ctx):
        async with self.conn_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """SELECT command FROM cc WHERE server = %s""",
                    (str(ctx.guild.id)),
                )
                row = await cur.fetchone()

        if row is None:
            embed = discord.Embed(
                title="⚠ 주의",
                description="현재 이 서버에 커스텀 명령어가 존재하지 않아요.",
                color=0xD8EF56,
            )
            return await ctx.send(embed=embed)

        embed = discord.Embed(
            title="⚠ 주의",
            description="정말로 모든 커스텀 명령어를 삭제하시겠어요?\n초기화 후에는 다시 복구할 수 **없습니다.**\n (y/n)",
            color=0xD8EF56,
        )
        await ctx.send(embed=embed)

        def usercheck(a):
            return a.author == ctx.author

        answer = await self.bot.wait_for("message", check=usercheck, timeout=30)
        answer = answer.content

        if answer == "y":
            async with self.conn_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        "DELETE FROM cc WHERE server = %s", (str(ctx.guild.id)),
                    )
                    embed = discord.Embed(
                        title="✅ 커스텀 초기화",
                        description="커스텀 초기화를 성공적으로 진행했어요.",
                        color=0x1DC73A,
                    )
                    await ctx.send(embed=embed)

        elif answer == "n":
            embed = discord.Embed(
                title="⚠ 주의", description="진행이 취소되었습니다.", color=0xD8EF56,
            )
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                title="⚠ 주의", description="잘못된 선택으로 취소되었습니다.", color=0xD8EF56,
            )
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CC(bot))
