import discord


class CommandInto(type):

    def __init__(cls, name, bases, attrs):

        if not hasattr(cls, 'commands'): # commands 리스트가 없을때
            cls.commands = [] # 커맨드 리스트 생성!
        else: 
            cls.commands.append(cls)

class Command(object, metaclass=CommandInto):

    def __init__(self, bot):
        self.client = bot


    async def _send(self,message):
        await self.on_message(message)

    async def on_message(self,message):
        pass
