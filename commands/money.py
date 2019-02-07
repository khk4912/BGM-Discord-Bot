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
이름 그대로, 돈기능이다.
'''


''' Function '''


''' Main '''


class money(Command):

    def __init__(self, *args, **kwargs):
        Command.__init__(self, *args, **kwargs)
        self.get = ["봇 돈내놔", "봇 돈받기", "봇 돈줘", "봇 돈받을래", "봇 출석"]
        self.money_list = [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000,
                           2000, 2000, 2000, 2000, 2000, 2000, 5000, 5000, 5000, 7000, 10000]

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
                            await cur.execute("""UPDATE money SET money=%s, lastgive=%s WHERE id=%s""", (total, receivetime, str(message.author.id)  ))
                            embed=discord.Embed(title="✅ 돈 받기 성공!", description="%s원을 받았습니다."%(random_money),color=0x1dc73a)
                            embed.add_field(name="현재 당신의 돈", value="%s원" %(total))
                            embed.set_footer(text="돈은 1000원에서 10000원까지 랜덤으로 부여됩니다.")
                            await message.channel.send(embed=embed)
                        else:
                            embed=discord.Embed(title="⚠ 주의", description="돈 받기는 10분에 한번씩만 가능합니다. %s초 남으셨습니다." %(str(600-int(sd.total_seconds()))), color=0xd8ef56)
                            await message.channel.send(embed=embed)

                    else:
                        await cur.execute("""INSERT INTO money (id, money, lastgive) VALUES (%s, %s, %s)""", (str(message.author.id), random_money, receivetime))
                        embed=discord.Embed(title="✅ 돈 받기 성공!", description="%s원을 받았습니다."%(random_money),color=0x1dc73a)
                        embed.add_field(name="현재 당신의 돈", value="%s원" %(random_money))
                        embed.set_footer(text="돈은 1000원에서 10000원까지 랜덤으로 부여됩니다.")

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
                embed=discord.Embed(title="✅ 돈 보기", description="<@%s>님의 돈은 %s원입니다."%(_id, "0"),color=0x1dc73a)
                embed.set_footer(text="봇 돈받기 명령어를 이용해 돈을 받아보세요!")
                await message.channel.send(embed=embed)


            else:
                embed=discord.Embed(title="✅ 돈 보기", description="<@%s>님의 돈은 %s원입니다."%(_id, row[1]),color=0x1dc73a)
                await message.channel.send(embed=embed)

         

        # if message.content.startswith("봇 슬롯")