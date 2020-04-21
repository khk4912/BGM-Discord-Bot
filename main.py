import discord
from discord.ext import commands
import asyncio
import sys
import traceback
import aiomysql
import PW
import TOKEN
import logging
import json
import pickle
import datetime
from utils.embed import Embed
from utils.background import change_activity
from logs import Logs
from colorama import init, Fore, Back, Style


class Main(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=["봇 ", "봇"], shard_count=2)
        self.logger = Logs.create_logger(self)
        self.main_logger = Logs.main_logger()

        self.loop = asyncio.get_event_loop()
        self.loop.create_task(change_activity(self))
        self.loop.create_task(self.set_db())

        self.afk = {}
        self.blacklist = []
        additional_commands = [
            self.add_to_black,
            self.rest_black,
            self.show_black,
        ]

        with open("blacklist.pickle", "rb") as f:
            self.blacklist = pickle.load(f)

        with open("argument_help.json", "r", encoding="utf-8") as f:
            self.argument_data = json.load(f)

        for i in TOKEN.initial_extensions:
            self.load_extension(i)

        for cmd in additional_commands:
            self.add_command(cmd)

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

    async def on_ready(self):
        self.logger.info("Bot Ready.")

    async def check_cc(self, message):

        command = message.content[2:]
        async with self.conn_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """SELECT * FROM cc WHERE server = %s AND command = %s""",
                    (str(message.guild.id), command),
                )
                row = await cur.fetchone()
                # print(row)
                if not row is None:
                    await message.channel.send(row[2])

    async def on_message(self, message):
        if message.author.bot or str(message.author.id) in self.blacklist:
            return

        await self.process_commands(message)


        if message.content.startswith("봇 "):
            try:
                await self.check_cc(message)
            except:
                pass

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            return

        if isinstance(error, commands.errors.CommandNotFound):
            return

        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="⚠ 쿨타임 중!",
                description="{}초 뒤에 재시도하세요.".format(int(error.retry_after)),
                color=0xD8EF56,
            )
            return await ctx.send(embed=embed)

        if isinstance(error, commands.CommandInvokeError):
            original = error.original
            if isinstance(original, discord.Forbidden):
                embed = Embed.warn(
                    "주의",
                    "봇의 권한이 부족하여 {} 명령어를 수행할 수 없어요.".format(ctx.command.name),
                )
                return await ctx.send(embed=embed)

        if (
            isinstance(error, commands.BadArgument)
            or isinstance(error, commands.BadUnionArgument)
            or isinstance(error, commands.MissingRequiredArgument)
        ):
            name = str(ctx.command)
            try:
                embed = Embed.warn(
                    "주의",
                    "잘못된 형식으로 명령어를 사용했어요. \n올바른 사용 : `봇 {} {}`".format(
                        name, self.argument_data[name]
                    ),
                )
                return await ctx.send(embed=embed)
            except KeyError:
                embed = Embed.warn("주의", "잘못된 형식으로 명령어를 사용했어요.")
                return await ctx.send(embed=embed)
        embed = Embed.error(
            "이런!",
            "{} 명령어 수행 중 핸들링 되지 않은 오류가 발생했어요!\n```{}```\n지속적인 문제 발생 시 `봇 문의` 명령어로 문의해주세요.".format(
                ctx.command.name, error
            ),
        )
        await ctx.send(embed=embed)
        print(
            "Ignoring exception in command {}".format(ctx.command),
            file=sys.stderr,
        )
        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr
        )
        self.logger.warning(
            "Error {} occured in command {}".format(
                type(error), ctx.command.name
            )
        )

    async def on_member_join(self, member):

        async with self.conn_pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(
                        """SELECT id, welcome, welcome_message FROM welcome WHERE id = %s""",
                        (member.guild.id),
                    )
                    row = await cur.fetchone()
                    if not row:
                        return
                except:
                    return
                if row[1] == 1:
                    try:
                        tg = row[2]
                        tg = tg.replace("{멘션}", member.mention)
                        tg = tg.replace("{서버이름}", member.guild.name)
                        await member.guild.system_channel.send(tg)
                    except:
                        pass



bot = Main()
bot.run(TOKEN.bot_token)
