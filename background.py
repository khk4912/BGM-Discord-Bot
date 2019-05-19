import discord
import asyncio

'''
봇이 작동중에 사용할 백그라운드 태스크를 사용합니다.
'''

async def change_activity(self):
    await self.wait_until_ready()
    while not self.is_closed():

        try:
            number = len(self.guilds)
            user = len(self.users)

            await self.change_presence(activity=discord.Game(name="%s개의 서버 / %s Servers"%(number,number)))
            await asyncio.sleep(30)
            await self.change_presence(activity=discord.Game(name="%s명의 유저 / %s Users"%(user, user)))
            await asyncio.sleep(30)
            await self.change_presence(activity=discord.Game(name="`봇 도움` 명령어를 사용해보세요!"))
            await asyncio.sleep(30)

        except:
            pass