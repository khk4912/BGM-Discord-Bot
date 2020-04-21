import discord
import asyncio


async def change_activity(self):
    await self.wait_until_ready()
    while not self.is_closed():
        try:
            number = len(self.guilds)
            user = len(self.users)

            await self.change_presence(
                activity=discord.Game(
                    name="{} Guilds / {} Users".format(number, user)
                )
            )
            await asyncio.sleep(20)

            await self.change_presence(
                activity=discord.Game(name="'봇 도움' 명령어를 사용해보세요!")
            )

            await asyncio.sleep(20)
        except:
            pass
