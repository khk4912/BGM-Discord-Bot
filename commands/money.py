'''
MIT License

Copyright (c) 2019 khk4912

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import discord
import asyncio
import random
import sys
import os
import PW
import aiomysql
from send import Command
import datetime


'''
돈 기능이 수록됩니다.
(기능 일원화를 막기 위해 게임 기능은 소스에서 제외됩니다.)
'''


''' Function '''


''' Main '''


class money(Command):

    def __init__(self, *args, **kwargs):
        Command.__init__(self, *args, **kwargs)
        self.get = ["봇 돈내놔", "봇 돈받기", "봇 돈줘", "봇 돈받을래", "봇 출석"]
        self.money_list = [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000,
                           2000, 2000, 2000, 2000, 2000, 2000, 5000, 5000, 5000, 7000, 10000]
        self.slot_list = ["7⃣"] * 10 + ["🔔"] * 10 + \
            ["⭐"] * 20 + ["🍒"] * 20 + ["🍈"] * 50
        self.betting = {"⃣": 50, "🔔": 25, "⭐": 10, "🍒": 5, "🍈": 2}
        self.gaming_list = []
        self.tictactoe = {}
        self.tictactoe_board = [["1⃣", "2⃣", "3⃣"],
                                ["4⃣", "5⃣", "6⃣"], ["7⃣", "8⃣", "9⃣"]]

    def get_playlist(self, board):
        now_board = ""
        for c in board:
            for i in c:
                now_board += i
            now_board += "\n"
        return now_board

    def change_board(self, ox, board, target):
        if target <= 3:
            board[0][target-1] = ox
            return board
        elif target <= 6:
            board[1][target-4] = ox
            return board
        elif target <= 9:
            board[2][target-7] = ox
            return board

    def check_win(self, board):
        for i in board:
            if i == ["⭕"] * 3 or i == ["❌"] * 3:
                return True

        if (board[0][0] == board[1][0] == board[2][0] or board[0][2] == board[1][2] == board[2][2] or
            board[0][0] == board[1][1] == board[2][2] or board[0][2] == board[1][1] == board[2][0]):
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

    async def on_message(self, message):

        if message.content in self.get:
            async with self.conn_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("""SELECT * FROM money WHERE id = %s""", (str(message.author.id)))
                    row = await cur.fetchone()
                    receivetime = datetime.datetime.now()
                    random_money = random.choice(self.money_list)
                    if not row is None:
                        last_receivetime = row[2]
                        sd = receivetime - last_receivetime
                        if sd.total_seconds() > 600:
                            money = row[1]
                            total = money + random_money
                            await cur.execute("""UPDATE money SET money=%s, lastgive=%s WHERE id=%s""", (total, receivetime, str(message.author.id)))
                            embed = discord.Embed(title="✅ 돈 받기 성공!", description="%s원을 받았습니다." % (
                                random_money), color=0x1dc73a)
                            embed.add_field(name="현재 당신의 돈",
                                            value="%s원" % (total))
                            embed.set_footer(
                                text="돈은 1000원에서 10000원까지 랜덤으로 부여됩니다. (차등 확률)")
                            await message.channel.send(embed=embed)
                        else:
                            embed = discord.Embed(title="⚠ 주의", description="돈 받기는 10분에 한번씩만 가능합니다. %s초 남으셨습니다." % (
                                str(600-int(sd.total_seconds()))), color=0xd8ef56)
                            await message.channel.send(embed=embed)

                    else:
                        await cur.execute("""INSERT INTO money (id, money, lastgive) VALUES (%s, %s, %s)""", (str(message.author.id), random_money, receivetime))
                        embed = discord.Embed(title="✅ 돈 받기 성공!", description="%s원을 받았습니다." % (
                            random_money), color=0x1dc73a)
                        embed.add_field(name="현재 당신의 돈",
                                        value="%s원" % (random_money))
                        embed.set_footer(
                            text="돈은 1000원에서 10000원까지 랜덤으로 부여됩니다. (차등 확률)")

                        await message.channel.send(embed=embed)

        if message.content.startswith("봇 돈보기"):
            if message.mentions == []:
                _id = message.author.id
            else:
                _id = message.mentions[0].id

            async with self.conn_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("""SELECT * FROM money WHERE id = %s""", (str(_id)))
                    row = await cur.fetchone()
            if row is None:
                embed = discord.Embed(
                    title="✅ 돈 보기", description="<@%s>님의 돈은 %s원입니다." % (_id, "0"), color=0x1dc73a)
                embed.set_footer(text="봇 돈받기 명령어를 이용해 돈을 받아보세요!")
                await message.channel.send(embed=embed)

            else:
                embed = discord.Embed(title="✅ 돈 보기", description="<@%s>님의 돈은 %s원입니다." % (
                    _id, row[1]), color=0x1dc73a)
                await message.channel.send(embed=embed)

        if message.content.startswith("봇 돈랭") or message.content.startswith("봇 돈순위") or message.content.startswith("봇 돈 순위"):
            async with self.conn_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("""SELECT * FROM money ORDER BY money DESC LIMIT 10; """, )
                    row = await cur.fetchall()
                    rank = 1
                    embed = discord.Embed(
                        title="✅ 돈 랭크", description="돈이 가장 많은 유저 10명을 불러옵니다!", color=0x1dc73a)
                    for i in row:
                        embed.add_field(name="{}위".format(
                            str(rank)), value="<@%s> / %s￦" % (i[0], i[1]))
                        rank += 1
            await message.channel.send(embed=embed)



