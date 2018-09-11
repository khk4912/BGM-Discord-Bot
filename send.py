import discord
import TOKEN
import PW
import asyncio
import aiomysql
import pickle 

class CommandInto(type):

    def __init__(cls, name, bases, attrs):

        if not hasattr(cls, 'commands'): # commands 리스트가 없을때
            cls.commands = [] # 커맨드 리스트 생성!
        else: 
            cls.commands.append(cls)

class Command(object, metaclass=CommandInto):

    def __init__(self, bot):
        self.client = bot
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.set_db())


    async def set_db(self):
        self.conn_pool = await aiomysql.create_pool(host='127.0.0.1', user=PW.db_user, password=PW.db_pw, db='bot', autocommit=True, loop=self.loop,
        minsize=5, maxsize=10, charset="utf8mb4")

        

        
    async def _send(self, message):
        await self.on_message(message)

    async def on_message(self, message):
        pass
