from discord.ext import commands
import discord
import asyncio
import aiomysql
import PW
import datetime
import random
import typing
from logs import Logs
from utils.embed import Embed


class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = Logs.create_logger(self)
        self.betting = {"7⃣": 10, "🔔": 7, "⭐": 5, "🍒": 2, "🍈": 1}
        self.gaming_list = []
        self.tictactoe = {}
        self.money_list = [
            1000,
            1000,
            1000,
            1000,
            1000,
            1000,
            1000,
            2000,
            2000,
            2000,
            2000,
            2000,
            2000,
            5000,
            5000,
            5000,
            5000,
            5000,
            7000,
            7000,
            10000,
        ]

        self.tictactoe_board = [
            ["1⃣", "2⃣", "3⃣"],
            ["4⃣", "5⃣", "6⃣"],
            ["7⃣", "8⃣", "9⃣"],
        ]

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
            maxsize=5,
            charset="utf8mb4",
        )

    async def get_user_money(self, id):
        async with self.conn_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """SELECT * FROM money WHERE id = %s""", (str(id))
                )
                row = await cur.fetchone()
        return row

    async def add_user_money(self, id, add):
        try:
            async with self.conn_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    row = await self.get_user_money(id)
                    if row is None:
                        await cur.execute(
                            """INSERT INTO money (id, money) VALUES (%s, %s)""",
                            (id, add),
                        )
                    else:
                        money = row[1] + add
                        await cur.execute(
                            """UPDATE money SET money=%s WHERE id=%s""",
                            (money, id),
                        )
            return True

        except:
            return False

    async def update_user_money(self, id, money):
        try:
            async with self.conn_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    row = await self.get_user_money(id)
                    if row is None:
                        await cur.execute(
                            """INSERT INTO money (id, money) VALUES (%s, %s)""",
                            (id, money),
                        )
                    else:
                        await cur.execute(
                            """UPDATE money SET money=%s WHERE id=%s""",
                            (money, id),
                        )
            return True

        except:
            return False

    def get_playlist(self, board):
        now_board = ""
        for c in board:
            for i in c:
                now_board += i
            now_board += "\n"
        return now_board

    def change_board(self, ox, board, target):
        if target <= 3:
            board[0][target - 1] = ox
            return board
        elif target <= 6:
            board[1][target - 4] = ox
            return board
        elif target <= 9:
            board[2][target - 7] = ox
            return board

    def check_win(self, board):
        for i in board:
            if i == ["⭕"] * 3 or i == ["❌"] * 3:
                return True

        if (
            board[0][0] == board[1][0] == board[2][0]
            or board[0][2] == board[1][2] == board[2][2]
            or board[0][0] == board[1][1] == board[2][2]
            or board[0][2] == board[1][1] == board[2][0]
            or board[0][1] == board[1][1] == board[2][1]
        ):
            return True

        return False

    def check_draw(self, board):
        count = 0
        for i in board:
            count += i.count("⭕")
            count += i.count("❌")
        if count == 9:
            return True
        else:
            return False

    async def is_gaming(self, ctx):
        if ctx.author.id in self.gaming_list:
            embed = Embed.warn("주의", "게임을 진행중이셔서 해당 명령어를 실행할 수 없어요.")
            await ctx.send(embed=embed)
            return True

    @commands.command(name="asd")
    async def asd(self, ctx, a, b):
        return

    @commands.command(name="슬롯")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def slot(self, ctx, text):
        if await self.is_gaming(ctx):
            return

        user_money = await self.get_user_money(ctx.author.id)
        if user_money is None or int(user_money[1]) <= 0:
            embed = discord.Embed(
                title="⚠ 주의",
                description="돈이 없는것 같아요! `봇 돈받기`명령어를 사용하세요.",
                color=0xD8EF56,
            )
            await ctx.send(embed=embed)
            return

        user_money = int(user_money[1])
        if text == "올인":
            bet = user_money
        else:
            try:
                bet = int(text)
            except:
                raise commands.BadArgument()

        if bet > user_money:
            embed = discord.Embed(
                title="⚠ 주의",
                description="배팅값이 현재 돈보다 많습니다! 현재 당신의 돈은  **{}￦**입니다.".format(
                    user_money
                ),
                color=0xD8EF56,
            )
            await ctx.send(embed=embed)
            return

        if bet <= 0:
            embed = discord.Embed(
                title="⚠ 주의",
                description="올바르지 않은 베팅값입니다! 배팅값은 0보다 커야합니다.",
                color=0xD8EF56,
            )
            await ctx.send(embed=embed)
            return

        try:
            self.gaming_list.append(ctx.author.id)
            user_money -= bet
            embed = discord.Embed(
                title="🎰 슬롯 머신",
                description="7⃣ 7⃣ 7⃣ > 10x\n🔔 🔔 🔔 > 7x\n⭐ ⭐ ⭐ > 5x\n 🍒 🍒 🍒 > 2x\n 🍈 🍈 🍈 > 1x\n\n시작합니다!",
                color=0x1DC73A,
            )
            slot_list = (
                ["7⃣"] * 20 + ["🔔"] * 20 + ["⭐"] * 20 + ["🍒"] * 20 + ["🍈"] * 20
            )
            await ctx.send(embed=embed)
            if random.random() < 0.18:
                nowcheck = random.random()
                if nowcheck > 0 and nowcheck <= 0.4:
                    slot_list = ["🍈"]
                elif nowcheck > 0.4 and nowcheck <= 0.7:
                    slot_list = ["🍒"]
                elif nowcheck > 0.7 and nowcheck <= 0.9:
                    slot_list = ["⭐"]
                elif nowcheck > 0.9 and nowcheck <= 1.0:
                    slot_list = ["🔔"]
                else:
                    slot_list = ["7⃣"]
                tgmg = await ctx.send(random.choice(slot_list))
                await asyncio.sleep(0.5)
                await tgmg.edit(
                    content=tgmg.content + " " + random.choice(slot_list)
                )
                await asyncio.sleep(0.5)
                await tgmg.edit(
                    content=tgmg.content + " " + random.choice(slot_list)
                )

            else:

                tgmg = await ctx.send(random.choice(slot_list))
                await asyncio.sleep(0.5)
                await tgmg.edit(
                    content=tgmg.content + " " + random.choice(slot_list)
                )
                await asyncio.sleep(0.5)
                await tgmg.edit(
                    content=tgmg.content + " " + random.choice(slot_list)
                )

            check = tgmg.content.split()
            if check[0] == check[1] == check[2]:
                betting = self.betting[check[0]]

                user_money += bet * betting
                embed = discord.Embed(
                    title="🎰 슬롯 머신",
                    description="축하드려요! {}배 성공! 이제 {}의 돈은 **{}￦**입니다.".format(
                        str(betting), ctx.author.mention, str(user_money)
                    ),
                    color=0x1DC73A,
                )
                await ctx.send(embed=embed)
            ###
            else:
                embed = discord.Embed(
                    title="🎰 슬롯 머신",
                    description="실패했네요... 이제 {}의 돈은 **{}￦**입니다.".format(
                        ctx.author.mention, str(user_money)
                    ),
                    color=0x1DC73A,
                )
                await ctx.send(embed=embed)

            await self.update_user_money(ctx.author.id, user_money)
            self.gaming_list.remove(ctx.author.id)

        except Exception as error:
            self.gaming_list.remove(ctx.author.id)
            embed = discord.Embed(
                title="⚠ 주의",
                description="게임 중 오류가 발생하여 게임이 정지하였습니다.\n%s" % (error),
                color=0xD8EF56,
            )
            await ctx.send(embed=embed)

    @commands.command(name="틱택토")
    async def tictactoee(self, ctx):
        if await self.is_gaming(ctx):
            return

        self.gaming_list.append(ctx.author.id)
        embed = discord.Embed(
            title="⏳ 틱택토 플레이어 기다리는 중",
            description="%s님과 플레이하고 싶으신 분은 ✅ 이모지를 달아주세요!\n매칭을 취소하시려면 ❌ 이모지를 달아주세요!"
            % (ctx.author.mention),
            color=0x1DC73A,
        )
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

        def wait_player(reaction, user):
            # if msg != reaction.message:
            #     return False
            if user.id == ctx.author.id and str(reaction) == "❌":
                return True
            return (
                user != ctx.author
                and str(reaction.emoji) == "✅"
                and user.id != self.bot.user.id
                and reaction.message.id == msg.id
                and not user.id in self.gaming_list
            )

        try:
            reaction, user = await self.bot.wait_for(
                "reaction_add", timeout=60.0, check=wait_player
            )
            if str(reaction) == "❌":
                self.gaming_list.remove(ctx.author.id)
                embed = discord.Embed(
                    title="✅ 매칭 취소", description="매칭이 취소되었어요!", color=0x1DC73A
                )
                await ctx.send(embed=embed)
                return

            elif str(reaction) == "✅":
                self.gaming_list.append(user.id)
                playlist = [ctx.author.id, user.id]
                playlist = random.sample(playlist, 2)
                init_list = [
                    ["1⃣", "2⃣", "3⃣"],
                    ["4⃣", "5⃣", "6⃣"],
                    ["7⃣", "8⃣", "9⃣"],
                ]
                self.tictactoe[playlist[0]] = init_list
                now_board = self.get_playlist(self.tictactoe[playlist[0]])
                pae = {playlist[0]: "⭕", playlist[1]: "❌"}
                available = list(range(1, 10))
                embed = discord.Embed(
                    title="🎮 게임 중...",
                    description="%s\n\n===\n<@%s> - ⭕\n<@%s> - ❌"
                    % (now_board, playlist[0], playlist[1]),
                    color=0x1DC73A,
                )

                first_board = await ctx.send(embed=embed)
                game = True
                count = 0
                while game:

                    for c in playlist:
                        count += 1
                        now_board = self.get_playlist(
                            self.tictactoe[playlist[0]]
                        )
                        embed = discord.Embed(
                            title="🎮 게임 중...",
                            description="<@%s>님 턴!\n\n  %s\n\n===\n<@%s> - ⭕\n<@%s> - ❌"
                            % (c, now_board, playlist[0], playlist[1]),
                            color=0x1DC73A,
                        )
                        await first_board.edit(embed=embed)
                        try:

                            def check_msg(m):
                                try:
                                    content = int(m.content)
                                except:
                                    return False
                                return (
                                    m.channel == ctx.channel
                                    and m.author.id == c
                                    and content in available
                                )

                            msg = await self.bot.wait_for(
                                "message", check=check_msg, timeout=30
                            )
                            try:
                                await msg.delete()
                            except:
                                pass
                            available.remove(int(msg.content))
                            self.tictactoe[playlist[0]] = self.change_board(
                                pae[c],
                                self.tictactoe[playlist[0]],
                                int(msg.content),
                            )

                            if self.check_win(self.tictactoe[playlist[0]]):
                                now_board = self.get_playlist(
                                    self.tictactoe[playlist[0]]
                                )
                                embed = discord.Embed(
                                    title="🎮 게임 종료!",
                                    description="<@%s>님 승!\n\n  %s\n\n===\n<@%s> - ⭕\n<@%s> - ❌"
                                    % (c, now_board, playlist[0], playlist[1]),
                                    color=0x1DC73A,
                                )
                                await first_board.edit(embed=embed)

                                embed = discord.Embed(
                                    title="✅ 승리!",
                                    description="<@%s>님이 승리했어요!" % (c),
                                    color=0x1DC73A,
                                )
                                await ctx.send(embed=embed)
                                game = False
                                break
                            if self.check_draw(self.tictactoe[playlist[0]]):
                                now_board = self.get_playlist(
                                    self.tictactoe[playlist[0]]
                                )
                                embed = discord.Embed(
                                    title="🎮 게임 종료!",
                                    description="무승부!\n\n  %s\n\n===\n<@%s> - ⭕\n<@%s> - ❌"
                                    % (now_board, playlist[0], playlist[1]),
                                    color=0x1DC73A,
                                )
                                await first_board.edit(embed=embed)

                                embed = discord.Embed(
                                    title="✅ 무승부!",
                                    description="무승부입니다!",
                                    color=0x1DC73A,
                                )
                                await ctx.send(embed=embed)
                                game = False
                                break
                            if count == 5:
                                embed = discord.Embed(
                                    title="🎮 게임 중...",
                                    description="%s\n\n===\n<@%s> - ⭕\n<@%s> - ❌"
                                    % (now_board, playlist[0], playlist[1]),
                                    color=0x1DC73A,
                                )
                                await first_board.delete()
                                first_board = await ctx.send(embed=embed)

                        except Exception as error:
                            embed = discord.Embed(
                                title="⚠ 주의",
                                description="타임아웃으로 <@%s>님이 패배하였습니다! %s"
                                % (c, error),
                                color=0xD8EF56,
                            )
                            await ctx.send(embed=embed)
                            game = False
                            break
                self.gaming_list.remove(ctx.author.id)
                self.gaming_list.remove(user.id)

                del self.tictactoe[playlist[0]]

        except Exception as error:
            self.gaming_list.remove(ctx.author.id)
            embed = discord.Embed(
                title="⚠ 주의",
                description="게임 중 오류가 발생하여 게임이 정지하였습니다.\n%s" % (error),
                color=0xD8EF56,
            )
            await ctx.send(embed=embed)

    @commands.command(name="돈받기", aliases=["돈내놔", "돈주세요", "돈줘", "출석"])
    async def give_money(self, ctx):
        async with self.conn_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """SELECT * FROM money WHERE id = %s""",
                    (str(ctx.author.id)),
                )
                row = await cur.fetchone()
                receivetime = datetime.datetime.now()
                random_money = random.choice(self.money_list)
                if not row is None:
                    last_receivetime = row[2]
                    if last_receivetime is None:
                        sd = 900
                    else:
                        sd = receivetime - last_receivetime
                        sd = sd.total_seconds()
                    if sd > 600:
                        money = row[1]
                        total = money + random_money
                        await cur.execute(
                            """UPDATE money SET money=%s, lastgive=%s WHERE id=%s""",
                            (total, receivetime, str(ctx.author.id)),
                        )
                        embed = discord.Embed(
                            title="✅ 돈 받기 성공!",
                            description="%s원을 받았습니다." % (random_money),
                            color=0x1DC73A,
                        )
                        embed.add_field(name="현재 당신의 돈", value="%s원" % (total))
                        embed.set_footer(
                            text="돈은 1000원에서 10000원까지 랜덤으로 부여됩니다. (차등 확률)"
                        )
                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            title="⚠ 주의",
                            description="돈 받기는 10분에 한번씩만 가능해요. %s초 남았어요."
                            % (str(600 - int(sd))),
                            color=0xD8EF56,
                        )
                        await ctx.send(embed=embed)

                else:
                    await cur.execute(
                        """INSERT INTO money (id, money, lastgive) VALUES (%s, %s, %s)""",
                        (str(ctx.author.id), random_money, receivetime),
                    )
                    embed = discord.Embed(
                        title="✅ 돈 받기 성공!",
                        description="%s원을 받았어요." % (random_money),
                        color=0x1DC73A,
                    )
                    embed.add_field(
                        name="현재 당신의 돈", value="%s원" % (random_money)
                    )
                    embed.set_footer(
                        text="돈은 1000원에서 10000원까지 랜덤으로 부여됩니다. (차등 확률)"
                    )

                    await ctx.send(embed=embed)

    @commands.command(name="게임유저")
    async def now_playing_user(self, ctx):
        embed = discord.Embed(
            title="🎮 게임 유저",
            description="현재 봇으로 게임을 플레이하고 있는 유저는 %s명이에요."
            % (str(len(self.gaming_list))),
            color=0xD8EF56,
        )
        await ctx.send(embed=embed)

    @commands.command(name="업다운")
    async def updown(self, ctx):
        if await self.is_gaming(ctx):
            return

        self.gaming_list.append(ctx.author.id)
        try:
            embed = discord.Embed(
                title="↕️ 업다운", description="난이도를 선택해주세요!", color=0x1DC73A
            )
            embed.add_field(
                name="쉬움",
                value="> **1~10**까지의 숫자에서 게임을 진행합니다.\n> 승리하면 500₩를 획득합니다.",
            )
            embed.add_field(
                name="보통",
                value="> **1~50**까지의 숫자에서 게임을 진행합니다. \n> 승리하면 2500₩를 획득합니다.",
            )
            embed.add_field(
                name="어려움",
                value="> **1~100**까지의 숫자에서 게임을 진행합니다.\n> 승리하면 5000₩를 획득합니다.",
            )
            await ctx.send(embed=embed)

            def check_diff(m):
                return (
                    m.channel == ctx.channel
                    and m.author == ctx.author
                    and m.content in ["쉬움", "보통", "어려움"]
                )

            msg = await self.bot.wait_for(
                "message", check=check_diff, timeout=30
            )
            if msg.content == "쉬움":
                difficult = "쉬움"
                until = 10
                winmoney = 500
            elif msg.content == "보통":
                difficult = "보통"
                until = 50
                winmoney = 2500
            elif msg.content == "어려움":
                difficult = "어려움"
                until = 100
                winmoney = 5000

            correct = random.randint(1, until)
            count = 5
            embed = discord.Embed(
                title="↕️ 업다운",
                description="5번의 기회만 주어집니다. 신중히 선택해주세요! \n**1~%s**안의 숫자를 입력해주세요."
                % (str(until)),
                color=0x1DC73A,
            )
            embed.set_footer(text="게임을 그만하시려면 '봇 취소'를 입력하세요.")
            await ctx.send(embed=embed)

            while count > 0:

                def check_updown_input(m):
                    try:
                        int(m.content)
                        return (
                            m.channel == ctx.channel
                            and m.author == ctx.author
                            and int(m.content) in list(range(1, until + 1))
                        )

                    except:
                        if (
                            m.channel == ctx.channel
                            and m.author == ctx.author
                            and m.content == "봇 취소"
                        ):
                            return True
                        else:
                            return False

                user_input = await self.bot.wait_for(
                    "message", check=check_updown_input, timeout=30
                )
                if user_input.content == "봇 취소":
                    embed = discord.Embed(
                        title="✅ 게임 취소",
                        description="게임이 취소되었습니다!",
                        color=0x1DC73A,
                    )
                    await ctx.send(embed=embed)
                    break

                else:
                    if int(user_input.content) == correct:
                        embed = discord.Embed(
                            title="✅ 승리!",
                            description="축하해요! 정답입니다! %s원이 추가됩니다."
                            % (str(winmoney)),
                            color=0x1DC73A,
                        )
                        await ctx.send(embed=embed)
                        await self.add_user_money(ctx.author.id, winmoney)
                        break

                    elif int(user_input.content) > correct:
                        count -= 1
                        embed = discord.Embed(
                            title="⬇ Down",
                            description="입력하신 숫자보다 정답이 낮아요! %s회 남았어요."
                            % (str(count)),
                            color=0x1DC73A,
                        )
                        await ctx.send(embed=embed)

                    elif int(user_input.content) < correct:
                        count -= 1
                        embed = discord.Embed(
                            title="⬆ Up",
                            description="입력하신 숫자보다 정답이 높아요! %s회 남았어요."
                            % (str(count)),
                            color=0x1DC73A,
                        )
                        await ctx.send(embed=embed)

                    if count == 0:
                        embed = discord.Embed(
                            title="⚠ 패배",
                            description="5번 안에 정답을 맞추시지 못했네요. 답은 %s였군요."
                            % (str(correct)),
                            color=0xD8EF56,
                        )
                        await ctx.send(embed=embed)

            self.gaming_list.remove(ctx.author.id)

        except Exception as error:
            self.gaming_list.remove(ctx.author.id)
            embed = discord.Embed(
                title="⚠ 주의",
                description="게임 중 오류가 발생하여 게임이 정지하였습니다.\n%s" % (error),
                color=0xD8EF56,
            )
            await ctx.send(embed=embed)

    @commands.command(name="돈보기", aliases=["내돈", "돈"])
    async def show_money(self, ctx):
        if ctx.message.mentions == []:
            _id = ctx.author.id
        else:
            _id = ctx.message.mentions[0].id
        row = await self.get_user_money(_id)
        if row is None:
            embed = discord.Embed(
                title="✅ 돈 보기",
                description="<@%s>님의 돈은 %s원이에요." % (_id, "0"),
                color=0x1DC73A,
            )
            embed.set_footer(text="`봇 돈받기` 명령어를 이용해 돈을 받아보세요!")
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                title="✅ 돈 보기",
                description="<@%s>님의 돈은 %s원이에요." % (_id, row[1]),
                color=0x1DC73A,
            )
            await ctx.send(embed=embed)

    @commands.command(name="돈랭", aliases=["돈랭크", "돈순위"])
    async def money_rank(self, ctx):
        async with self.conn_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """SELECT * FROM money ORDER BY money DESC LIMIT 10; """,
                )
                row = await cur.fetchall()
                rank = 1
                embed = discord.Embed(
                    title="✅ 돈 랭크",
                    description="돈이 가장 많은 유저 10명을 불러와요.",
                    color=0x1DC73A,
                )
                for i in row:
                    embed.add_field(
                        name="{}위".format(str(rank)),
                        value="<@%s> / %s￦" % (i[0], i[1]),
                    )
                    rank += 1
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Game(bot))
