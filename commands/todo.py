from discord.ext import commands
import asyncio
import aiohttp
import aiomysql
import PW


class Todo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.set_db())

    async def set_db(self):
        self.conn_pool = await aiomysql.create_pool(host='127.0.0.1', user=PW.db_user, password=PW.db_pw, db='bot', autocommit=True, loop=self.loop,
                                                    minsize=2, maxsize=3, charset="utf8mb4")

    @commands.command(name="할일등록", aliases=["일등록"])
    async def register_todo(self, ctx):
        async with self.conn_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""SELECT * FROM money WHERE id = %s""", (str(ctx.author.id)))
                row = await cur.fetchone()

        if row is None:
            


def setup(bot):
    bot.add_cog(Todo(bot))
