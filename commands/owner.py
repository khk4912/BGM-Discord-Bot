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
import pickle
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

        self.noticelist = ["봇-공지","봇_공지", "봇공지", "공지", "bot-notice", "bot_notice", "botnotice",  "notice", "bot-announcement", "botannouncment", 'bot_announcement']

    def search_notice_channel(self):

        allserver = []
        self.noticechannels = []
        for i in self.client.guilds:
            allserver.append(i)
        for b in allserver:
            for i in b.channels:
                if "bot-announcement" in i.name or "bot_announcement" in i.name or "봇-공지" in i.name or "봇_공지" in i.name:
                    self.noticechannels.append(i)
      
        for c in self.noticechannels:
            try:
                allserver.remove(c.guild)
            except:
                pass

        for b in allserver:
            for i in b.channels:
                if "bot-notice" in i.name or "bot_notice" in i.name:
                    self.noticechannels.append(i)
        for c in self.noticechannels:
            try:
                allserver.remove(c.guild)
            except:
                pass

        for b in allserver:
            for i in b.channels:
                if "notice" in i.name or "공지" in i.name:
                    self.noticechannels.append(i)
        for c in self.noticechannels:
            try:
                allserver.remove(c.guild)
            except:
                pass

        self.noserver = []
        for b in allserver:
            for i in b.channels:
                if "announcement" in i.name or "annoucement" in i.name:
                    self.noticechannels.append(i)

        for c in self.noticechannels:
            try:
                allserver.remove(c.guild)
            except:
                pass
        for a in allserver:
            self.noserver.append(a.name)

                    



    async def on_message(self,message):

        if message.content.startswith("봇 경고보기"):
            if not message.mentions == []:
                user = message.mentions[0]
                async with self.conn_pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute("""SELECT * FROM warn WHERE id = %s""", (str(user.id) ))
                        row = await cur.fetchone()
                        
                        if row is None:
                            warns = 0
                            embed=discord.Embed(title="✅ 경고 조회", description="%s 님의 경고를 불러옵니다." %(user.mention) ,color=0x1dc73a )
                            embed.add_field(name="경고 수", value=str(warns) + "회" )
                            embed.set_footer(text="5회 이상 경고 발생시 제제 처리됩니다.")

                        else:
                            warns = row[1]
                            embed=discord.Embed(title="✅ 경고 조회", description="%s 님의 경고를 불러옵니다." %(user.mention) ,color=0x1dc73a )
                            embed.add_field(name="경고 수", value=str(warns) + "회" )
                            embed.set_footer(text="5회 이상 경고 발생시 제제 처리됩니다.")

                await message.channel.send(embed=embed)

            else:
                embed=discord.Embed(title="⚠ 주의", description="사용자가 선택되지 않았습니다. 멘션으로 사용자를 설정해주세요.",color=0xd8ef56)
                await message.channel.send(embed=embed)

        if not message.author.id == 289729741387202560:
            return


        if message.content == "봇 재시작":
            await message.channel.send("봇을 재시작합니다...")
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



        if message.content.startswith("봇 경고추가"):
            if not message.mentions == []:
                user = message.mentions[0]
                async with self.conn_pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute("""SELECT * FROM warn WHERE id = %s""", (str(user.id) ))
                        row = await cur.fetchone()
                        
                        if row is None:
                            warns = 1
                            await cur.execute("""INSERT INTO warn (id, times) VALUES (%s, %s)""", (str(user.id), 1 ))
                        else:
                            warns = row[1] + 1
                            await cur.execute("""UPDATE warn SET times=%s WHERE id = %s""", (warns, str(user.id)))

                embed=discord.Embed(title="✅ 경고 추가", description="%s 님의 경고를 성공했습니다." %(user.mention) ,color=0x1dc73a )
                embed.add_field(name="경고 수", value=str(warns) + "회" )
                embed.set_footer(text="5회 이상 경고 발생시 제제 처리됩니다.")
                await message.channel.send(embed=embed)

            else:
                embed=discord.Embed(title="⚠ 주의", description="선택되지 않은 사용자.",color=0xd8ef56)
                await message.channel.send(embed=embed)
                
        if message.content.startswith("봇 db"):
            try:
                query = message.content[4:].lstrip()
                async with self.conn_pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute(query)
                        row = await cur.fetchall()
                if row is None or row == []:
                    embed=discord.Embed(title="✅ 성공", description="결과값이 없습니다.",color=0x1dc73a )
                else:
                    embed=discord.Embed(title="✅ 성공", description="%s" %(str(row)),color=0x1dc73a )
                await message.channel.send(embed=embed)
            except Exception as error:
                embed=discord.Embed(title="⚠ 주의", description="오류 발생!\n```%s```" %(error),color=0xd8ef56)
                await message.channel.send(embed=embed)
                
      
            
        if message.content.startswith("봇 공지"):
            contents = message.content[4:].lstrip()
            if contents == "" or contents is None:
                await message.channel.send("내용을 입력하세요. 전송에 실패하였습니다.")
            else:
                await message.channel.send("정말 전송합니까? (y/n)")
                def usercheck(a):
                    return a.author == message.author

                answer = await self.client.wait_for('message', check=usercheck, timeout=30)
                answer = answer.content

                if answer == "y":
                    self.search_notice_channel()
                    for i in self.noticechannels:
                        try:
                            await i.send(contents)
                        except:
                            pass
                    
                    await message.channel.send("전송 완료! 전송 하지 못한 서버들 : %s" %(self.noserver))
                else:
                    await message.channel.send("전송을 취소합니다.")


