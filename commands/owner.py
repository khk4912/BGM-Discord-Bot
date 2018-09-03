import discord
import asyncio
import random 
import sys
import os
import PW 
import aiomysql 

from send import Command

'''
봇 주인만 사용 가능한 비밀 명령어를 수록합니다.
'''


''' Function '''
def restart_bot():
    python = sys.executable
    os.execl(python, python, * sys.argv)

''' Main ''' 
class owner(Command):

    def __init__(self, *args, **kwargs):
        Command.__init__(self, *args, **kwargs)


    async def on_message(self,message):

        if not message.author.id == 289729741387202560:
            return

        if message.content == "봇 재시작":
            restart_bot()


        if message.content == "봇 종료":
            await message.channel.send("봇을 종료합니다...")
            exit()

        if message.content.startswith("봇 강제초대"):
            a = message.content
            serverid = a[7:]
            invite = self.client.get_channel(int(serverid))
        
            link = await invite.create_invite(max_uses=1, reason="자동 초대")
            
            await message.channel.send(link)



        # if message.content.startswith("봇 경고추가"):
        #     if not message.mentions == []:
        #         user = message.mentions[0]
        #         async with self.conn.cursor() as cur:
        #             await cur.execute("""SELECT id FROM warn WHERE id = %s""", (str(message.author.id)) )




        #     else:
        #         embed=discord.Embed(title="⚠ 주의", description="선택되지 않은 사용자.",color=0xd8ef56)
        #         await message.channel.send(embed=embed)
                

