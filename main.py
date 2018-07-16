import discord
import asyncio
import TOKEN

import importer
from send import Command
from commands.background import * 

loop = asyncio.get_event_loop()

class Bot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_command = []
        self.get_all_commands()
        # self.bg_task = self.loop.create_task(on_thirty_second(self)) Background Task
        print(self.load_command)
    
    def get_all_commands(self):
        for i in Command.commands:
            self.load_command.append(i(self))



    async def on_ready(self):
        print(self.user.name + "으로 봇이 로그인함.")
        print("=======")
        print("작동 시작!")
        print("\n\n")
        for s in client.guilds:
            print(" >> %s [%s, %s]" % (s.name, s.id,s.get_member(self.user.id).guild_permissions.administrator))

    
    async def on_message(self, message):
        if message.author.bot:
            return
        
        for i in self.load_command:
            self.loop.create_task(i._send(message))


client = Bot()
client.run(TOKEN.bot_token)