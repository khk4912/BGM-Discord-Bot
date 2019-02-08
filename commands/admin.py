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
import aiomysql
import PW
import time

from send import Command

'''
서버 어드민들이 사용 가능한 봇의 명령어를 수록합니다.
(단, 100줄 이상의 명령어는 따로 분리처리)
'''


''' Function '''

''' Main ''' 
class admin(Command):
    
    def __init__(self, *args, **kwargs):
        Command.__init__(self, *args, **kwargs)
        
    
    async def on_member_join(self,member):
        async with self.conn_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""SELECT * FROM server WHERE id = %s""", (member.guild.id))
                row = await cur.fetchone()

                if row[1] == 1:
                    tg = row[2]
                    tg = tg.replace("{멘션}", member.mention)
                    tg = tg.replace("{서버이름}", member.guild.name)
                    await member.guild.system_channel.send(tg)


    async def on_message(self, message):


        if not message.author.id == 289729741387202560:
            if not message.author.guild_permissions.administrator == True:
                return
        

    

        if message.content.startswith('봇 뮤트'):
            if message.author.guild_permissions.administrator == True:
                try:
                    if not message.mentions == []:
                        member = message.mentions[0]

                        overwrite = discord.PermissionOverwrite()
                        overwrite.send_messages = False
                        await message.channel.set_permissions(member, overwrite=overwrite)
                        embed=discord.Embed(title="✅ 유저 뮤트", description="뮤트를 성공했습니다.",color=0x1dc73a)
                        await message.channel.send(embed=embed)
                    else:
                        embed=discord.Embed(title="⚠ 주의", description="`봇 뮤트 @유저` 형식으로 명령어를 사용해주세요. 선택된 사용자가 없습니다.",color=0xd8ef56)
                        await message.channel.send(embed=embed)
                        
                except:
                    embed=discord.Embed(title="❌ 오류 발생", description="뮤트를 실패하였습니다. 권한을 확인해 주세요. "  ,color=0xff0909)    
                    await message.channel.send(embed=embed)

            else:
                embed=discord.Embed(title="⚠ 주의", description="관리자 권한이 있어야 사용 가능한 명령어입니다.",color=0xd8ef56)
                await message.channel.send(embed=embed)


        if message.content.startswith('봇 언뮤트'):
            if message.author.guild_permissions.administrator == True:
                try:
                    if not message.mentions == []:
                        member = message.mentions[0]
                        overwrite = discord.PermissionOverwrite()
                        overwrite.send_messages = True
                        await message.channel.set_permissions(member, overwrite=overwrite)
                        embed=discord.Embed(title="✅ 유저 언뮤트", description="언뮤트를 성공했습니다.",color=0x1dc73a )
                        await message.channel.send(embed=embed)
                    else:
                        embed=discord.Embed(title="⚠ 주의", description="`봇 언뮤트 @유저` 형식으로 명령어를 사용해주세요. 선택된 사용자가 없습니다.",color=0xd8ef56)
                        await message.channel.send(embed=embed)
                        
                except:
                    embed=discord.Embed(title="❌ 오류 발생", description="뮤트를 실패하였습니다. 권한을 확인해 주세요." ,color=0xff0909)    
                    await message.channel.send(embed=embed)
            else:
                embed=discord.Embed(title="⚠ 주의", description="관리자 권한이 있어야 사용 가능한 명령어입니다.",color=0xd8ef56)
                await message.channel.send(embed=embed)


        if message.content.startswith('봇 전체뮤트'):
            if message.author.guild_permissions.administrator == True:
                try:
                    role = discord.utils.get(message.guild.roles, name='@everyone')
                    await message.channel.set_permissions(role, send_messages=False)
                    embed=discord.Embed(title="✅ 전체 뮤트", description="관리자를 제외한 모든 유저의 뮤트를 성공했습니다.",color=0x1dc73a )
                    await message.channel.send(embed=embed)
                except:
                    embed=discord.Embed(title="❌ 오류 발생", description="뮤트를 실패하였습니다. 권한을 확인해 주세요." ,color=0xff0909)    
                    await message.channel.send(embed=embed)

            else:
                embed=discord.Embed(title="⚠ 주의", description="관리자 권한이 있어야 사용 가능한 명령어입니다.",color=0xd8ef56)
                await message.channel.send(embed=embed)


        if message.content.startswith('봇 전체언뮤트'):
            if message.author.guild_permissions.administrator == True:
                try:
                    role = discord.utils.get(message.guild.roles, name='@everyone')
                    await message.channel.set_permissions(role, send_messages=True)
                    embed=discord.Embed(title="✅ 전체 언뮤트", description="모든 유저의 언뮤트를 성공했습니다.",color=0x1dc73a )
                    await message.channel.send(embed=embed)

                except: 
                    embed=discord.Embed(title="❌ 오류 발생", description="뮤트를 실패하였습니다. 권한을 확인해 주세요." ,color=0xff0909)    
                    await message.channel.send(embed=embed)

            else:
                embed=discord.Embed(title="⚠ 주의", description="관리자 권한이 있어야 사용 가능한 명령어입니다.",color=0xd8ef56)
                await message.channel.send(embed=embed)

        if message.content.startswith('봇 밴') :
            if message.author.guild_permissions.administrator == True:
                try:
                    if not message.mentions == []:
                        member = message.mentions[0]
                        await message.guild.ban(member,reason=str(message.author) + "님의 명령어 사용으로 인해 밴 당하셨습니다.", delete_message_days=7)
                        embed=discord.Embed(title="✅ 유저 밴", description="유저의 밴을 완료했습니다.",color=0x1dc73a )
                        await message.channel.send(embed=embed)
                    else:
                        embed=discord.Embed(title="⚠ 주의", description="`봇 밴 @유저` 형식으로 명령어를 사용해주세요. 선택된 사용자가 없습니다.",color=0xd8ef56)
                        await message.channel.send(embed=embed)

                except:
                    embed=discord.Embed(title="❌ 오류 발생", description="밴을 실패하였습니다. 권한을 확인해보세요." ,color=0xff0909)    
                    await message.channel.send(embed=embed)
            else:
                embed=discord.Embed(title="⚠ 주의", description="관리자 권한이 있어야 사용 가능한 명령어입니다.",color=0xd8ef56)
                await message.channel.send(embed=embed)



        if message.content.startswith('봇 언밴'):
            if message.author.guild_permissions.administrator == True:
                try:    
                    memberid = message.content.replace("봇 언밴 ", "")
                    memberid = memberid.replace("<", "")
                    memberid = memberid.replace("@", "")
                    memberid = memberid.replace("!", "")
                    memberid = memberid.replace(">", "")
                    
                    if not memberid == "":
                        embed=discord.Embed(title="✅ 유저 언밴", description="유저의 언밴을 완료했습니다.",color=0x1dc73a )
                        await message.channel.send(embed=embed)
                
                    else:
                        embed=discord.Embed(title="⚠ 주의", description="`봇 언밴 [유저ID]` 형식으로 명령어를 사용해주세요. 선택된 사용자가 없습니다.",color=0xd8ef56)
                        await message.channel.send(embed=embed)
             
                except:
                    embed=discord.Embed(title="❌ 오류 발생", description="언밴을 실패하였습니다. 권한을 확인해보세요." ,color=0xff0909)    
                    await message.channel.send(embed=embed)

            else:
                embed=discord.Embed(title="⚠ 주의", description="관리자 권한이 있어야 사용 가능한 명령어입니다.",color=0xd8ef56)
                await message.channel.send(embed=embed)




        if message.content.startswith('봇 킥') :
            if message.author.guild_permissions.administrator == True:
                try:
                    if not message.mentions == []:

                        member = message.mentions[0]
                        await message.guild.kick(member,reason=str(message.author) + "님의 명령어 사용으로 인해 킥 당하셨습니다.")
                        embed=discord.Embed(title="✅ 멤버 킥", description="킥을 날려버렸습니다.",color=0x1dc73a)
                        await message.channel.send(embed=embed)
                    else:
                        embed=discord.Embed(title="⚠ 주의", description="`봇 킥 @유저` 형식으로 명령어를 사용해주세요. 선택된 사용자가 없습니다.",color=0xd8ef56)
                        await message.channel.send(embed=embed)
                       
                except:
                    embed=discord.Embed(title="❌ 오류 발생", description="킥을 실패하였습니다. 권한을 확인해 주세요." ,color=0xff0909)    
                    await message.channel.send(embed=embed)
            else:
                embed=discord.Embed(title="⚠ 주의", description="관리자 권한이 있어야 사용 가능한 명령어입니다.",color=0xd8ef56)
                await message.channel.send(embed=embed)


        if message.content.startswith('봇 지우기'):
            if message.author.guild_permissions.administrator == True:
                a = message.content[6:]
                if a.startswith("<@"):
                    mgs = []
                    tgmgs = []
                    a = a.replace("<@", "")
                    a = a.replace(">","")
                    member = message.guild.get_member(int(a))                        
                    async for x in message.channel.history(limit = 100):
                        mgs.append(x)
                    for i in mgs:
                        if i.author == member:
                            tgmgs.append(i)
                    try:
                        await message.channel.delete_messages(tgmgs)
                        await message.delete()
                        embed=discord.Embed(title="✅ 메시지 삭제", description="%s개의 메시지를 지웠습니다." %len(tgmgs),color=0x1dc73a )
                        deletemessage = await message.channel.send(embed=embed)
                        await asyncio.sleep(1)
                        await deletemessage.delete()
                    except discord.errors.NotFound:
                        embed=discord.Embed(title="⚠ 오류 발생", description="일정 메시지의 삭제에 문제가 발생하였습니다.",color=0xff0909 )
                        await message.channel.send(embed=embed)

                        deletemessage =  await message.channel.send(embed=embed)
                        await asyncio.sleep(5)
                        await deletemessage.delete()
                        
                        
                else:
                    try:
                        a = a.replace ("봇 지우기", "")
                        a = a.split()

                        a = [int (i) for i in a]
                        b = a[0]
                        mgs = []
                        number = b
                            
                
                        async for x in message.channel.history(limit = number):
                            mgs.append(x)

                        await message.channel.delete_messages(mgs)
                        embed=discord.Embed(title="✅ 메시지 삭제", description="%s개의 메시지를 지웠습니다." %number,color=0x1dc73a )
                        deletemessage = await message.channel.send(embed=embed)
                        await asyncio.sleep(1)
                        await deletemessage.delete()
                    except Exception as error:
                        embed=discord.Embed(title="⚠ 오류 발생", description="메시지의 삭제에 문제가 발생하였습니다." ,color=0xff0909 )
                        deletemessage =  await message.channel.send(embed=embed)
                        await asyncio.sleep(5)
                        await deletemessage.delete()

            else:
                embed=discord.Embed(title="⚠ 주의", description="관리자 권한이 있어야 사용 가능한 명령어입니다.",color=0xd8ef56)
                await message.channel.send(embed=embed)

        if message.content.startswith("봇 웰컴설정") or message.content.startswith("봇 환영설정"):
            async with self.conn_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("""SELECT * FROM server WHERE id=%s""", (message.guild.id))
                    row = await cur.fetchone()
            
            if row is None or row[1] == 0:
                embed=discord.Embed(title="📝 웰컴 설정", description="현재 웰컴 메시지가 설정되어 있지 않습니다. 추가하시려면 ✅ 이모티콘을 눌러주세요.")
                msg = await message.channel.send(embed=embed)
                await msg.add_reaction("✅")

                def posi_check(reaction, user):
                    return user == message.author and str(reaction.emoji) == '✅'

                try:
                    reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=posi_check)
                    if str(reaction) == "✅":
                        edit = True
                    else:
                        return
                except:
                    await message.channel.send("타임아웃으로 취소되었습니다.")
                    return

            else:
                embed=discord.Embed(title="📝 웰컴 설정", description=f"현재 웰컴 메시지는 다음과 같습니다.\n```{row[2]}```\n\n 수정하시려면 ✅ 이모티콘을, 제거하시려면 ❌ 이모티콘을 클릭해주세요. ")            
                msg = await message.channel.send(embed=embed)
                await msg.add_reaction("✅")
                await msg.add_reaction("❌")


                def posi_check2(reaction, user):
                    return user == message.author and ( str(reaction.emoji) == '✅' or str(reaction.emoji)  == "❌" )

                try:
                    reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=posi_check2)
                    if str(reaction) == "✅":
                        edit = True
                        print(edit)
                    else:
                        edit = False
                except:
                    await message.channels.send("타임아웃으로 취소되었습니다.")
                    return

            
            if edit:
                embed=discord.Embed(title="📝 웰컴 설정", description="유저가 들어올때 봇이 보낼 메시지를 설정해주세요. 취소하시려면 `봇 취소` 를 입력하세요.\n\n{멘션} > 유저를 언급합니다.\n{서버이름} > 서버 이름을 표시합니다.")            
                await message.channel.send(embed=embed)

                def check_msg(m):
                    return m.channel == message.channel and m.author == message.author

                msg = await self.client.wait_for('message', check=check_msg)
                if msg == "봇 취소":
                    await message.channel.send("취소되었습니다.")
                else:
                    async with self.conn_pool.acquire() as conn:
                        async with conn.cursor() as cur:
                            await cur.execute("""INSERT INTO server (id, welcome, welcome_message) VALUES (%s, %s, %s)  ON DUPLICATE KEY UPDATE welcome=%s, welcome_message=%s;""", (message.guild.id, 1, msg.content, 1, msg.content))
                    embed=discord.Embed(title="✅ 웰컴 메시지", description=f"```{msg.content}```\n로 웰컴 메시지가 설정되었습니다.",color=0x1dc73a )
                    await message.channel.send(embed=embed)
                    
            else:
                async with self.conn_pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute("""INSERT INTO server (id, welcome, welcome_message) VALUES (%s, %s, %s)  ON DUPLICATE KEY UPDATE welcome='%s';""", (message.guild.id, 0, None, 0))
                    embed=discord.Embed(title="✅ 웰컴 메시지", description="웰컴 메시지 사용이 중지되었습니다.",color=0x1dc73a )
                    await message.channel.send(embed=embed)
                  



