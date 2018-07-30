import discord
import asyncio
import aiomysql
import PW
import datetime

from send import Command

'''
커스텀 커맨드 관련 명령어를 수록합니다.
'''

''' Function '''

''' Main '''

class cc(Command):
    
    def __init__(self, *args, **kwargs):
        Command.__init__(self, *args, **kwargs)
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.set_db())

    async def set_db(self):
        self.conn = await aiomysql.connect(host='127.0.0.1', user=PW.db_user, password=PW.db_pw, db='bot', autocommit=True, loop=self.loop)


    async def on_message(self,message):

        ''' 일반 유저 가능 ''' 
        if message.content.startswith("봇 "):
            command = message.content[2:]
            async with self.conn.cursor() as cur:
                await cur.execute("""SELECT answer FROM cc WHERE server = %s AND command = %s""", (str(message.guild.id), command))
                row = await cur.fetchone()
                if not row is None:
                    await message.channel.send(row[0])

        if message.content.startswith('봇 커스텀 보기') or message.content.startswith("봇 커스텀보기"):
            try:
                async with self.conn.cursor() as cur:
                    await cur.execute("""SELECT command FROM cc WHERE server = %s""", (str(message.guild.id)) )
                    row = await cur.fetchall()
                    if not row is ():
                        text = "| "
                        for i in row:
                            text += i[0] + " | "

                        embed=discord.Embed(title="✅ 커스텀 보기", description="%s" %(text ),color=0x1dc73a )
                        await message.channel.send(embed=embed)
                    else:
                        embed=discord.Embed(title="✅ 커스텀 보기", description="커스텀 명령어가 없습니다.",color=0x1dc73a )
                        await message.channel.send(embed=embed)
                
            except Exception as error:
                embed=discord.Embed(title="❌ 오류 발생", description="오류로 커스텀 명령어 불러오기에 실패하였습니다. 지속적으로 문제가 발생한다면 BGM#0970 DM 바랍니다. %s" %(error) ,color=0xff0909 )
                await message.channel.send(embed=embed)



        ''' 어드민, 오너 사용 가능 '''

        if message.content.startswith('봇 커스텀 추가'):
            if message.author.guild_permissions.administrator == True or message.author.id == 289729741387202560:
                a = message.content[8:].lstrip()
                if a == "":
                    embed=discord.Embed(title="⚠ 주의", description="`봇 커스텀 추가 [명령어]/[봇의 대답]` 형식으로 작성해주세요.",color=0xd8ef56)
                    await message.channel.send(embed=embed)
                else:
                    answer = ""
                    contents = a.split("/")
                    command = contents[0]


                    if len(a) >= 2:
                        for i in contents[1:]:
                            answer += i
                        answer = answer.lstrip()
                        async with self.conn.cursor() as cur:
                            await cur.execute("""SELECT command FROM cc WHERE server = %s AND command = %s""", (str(message.guild.id), command))
                            row = await cur.fetchone()
                        if not row is None:
                            embed=discord.Embed(title="⚠ 주의", description="이미 존재하는 명령어입니다. 수정하시려면 `봇 커스텀 수정 [명령어]/[봇의 대답]` 을 사용해주세요.",color=0xd8ef56)
                            await message.channel.send(embed=embed)
                        else:
                            async with self.conn.cursor() as cur:
                                await cur.execute("""INSERT INTO cc (server, command, answer, who, datetime) VALUES (%s, %s, %s, %s, %s)""", ( str(message.guild.id), command, answer, str(message.author.id), str(datetime.datetime.now())     ))
                                embed=discord.Embed(title="✅ 커스텀 추가", description="커스텀 추가를 성공했습니다.",color=0x1dc73a )
                                embed.add_field(name="명령어", value=command)
                                embed.add_field(name="봇의 대답", value=answer)
                                await message.channel.send(embed=embed)


                    else:
                        embed=discord.Embed(title="⚠ 주의", description="`봇 커스텀 추가 [명령어]/[봇의 대답]` 형식으로 작성해주세요.",color=0xd8ef56)
                        await message.channel.send(embed=embed)


            else:
                embed=discord.Embed(title="⚠ 주의", description="관리자 권한 또는 봇 오너여야 사용 가능한 명령어입니다.",color=0xd8ef56)
                await message.channel.send(embed=embed)

        if message.content.startswith('봇 커스텀 수정'):
            if message.author.guild_permissions.administrator == True or message.author.id == 289729741387202560:
                a = message.content[8:].lstrip()
                if a == "":
                    embed=discord.Embed(title="⚠ 주의", description="`봇 커스텀 수정 [명령어]/[봇의 대답]` 형식으로 작성해주세요.",color=0xd8ef56)
                    await message.channel.send(embed=embed)
                else:
                    answer = ""
                    contents = a.split("/")
                    command = contents[0]


                    if len(a) >= 2:
                        for i in contents[1:]:
                            answer += i
                        answer = answer.lstrip()
                        async with self.conn.cursor() as cur:
                            await cur.execute("""SELECT command FROM cc WHERE server = %s AND command = %s""", (str(message.guild.id), command))
                            row = await cur.fetchone()
                        if not row is None:
                            async with self.conn.cursor() as cur:
                                await cur.execute("""UPDATE cc SET answer=%s, who=%s, datetime=%s WHERE server=%s AND command=%s  """, ( answer, str(message.author.id), str(datetime.datetime.now()), str(message.guild.id), str(command)  ))
                                embed=discord.Embed(title="✅ 커스텀 수정", description="커스텀 수정을 성공했습니다.",color=0x1dc73a )
                                embed.add_field(name="명령어", value=command)
                                embed.add_field(name="수정된 봇의 대답", value=answer)
                                await message.channel.send(embed=embed)

                        else:
                            embed=discord.Embed(title="⚠ 주의", description="음.. 해당 명령어가 존재 하지 않아요. `봇 커스텀 추가 [명령어]/[봇의 대답]` 으로 추가를 해보세요!",color=0xd8ef56)
                            await message.channel.send(embed=embed)


                    else:
                        embed=discord.Embed(title="⚠ 주의", description="`봇 커스텀 수정 [명령어]/[봇의 대답]` 형식으로 작성해주세요.",color=0xd8ef56)
                        await message.channel.send(embed=embed)


            else:
                embed=discord.Embed(title="⚠ 주의", description="관리자 권한 또는 봇 오너여야 사용 가능한 명령어입니다.",color=0xd8ef56)
                await message.channel.send(embed=embed)




        if message.content.startswith('봇 커스텀 삭제'):
            if message.author.guild_permissions.administrator == True or message.author.id == 289729741387202560:
                a = message.content[8:].lstrip()
                if a == "":
                    embed=discord.Embed(title="⚠ 주의", description="`봇 커스텀 삭제 [삭제할 명령어]` 형식으로 작성해주세요.",color=0xd8ef56)
                    await message.channel.send(embed=embed)
                else:

                    command = a.lstrip()
                    async with self.conn.cursor() as cur:
                        await cur.execute("""SELECT command FROM cc WHERE server = %s AND command = %s""", (str(message.guild.id), command))
                        row = await cur.fetchone()
                        if not row is None:
                            async with self.conn.cursor() as cur:
                                await cur.execute("""DELETE FROM cc WHERE server = %s AND command = %s""", (str(message.guild.id), command) )
                                embed=discord.Embed(title="✅ 커스텀 삭제", description="커스텀 삭제를 성공했습니다.",color=0x1dc73a )
                                embed.add_field(name="삭제한 명령어", value=command)
                                await message.channel.send(embed=embed)

                        else:
                            embed=discord.Embed(title="⚠ 주의", description="음.. 해당 명령어가 존재 하지 않아요. `봇 커스텀 추가 [명령어]/[봇의 대답]` 으로 추가를 해보세요!",color=0xd8ef56)
                            await message.channel.send(embed=embed)


            else:
                embed=discord.Embed(title="⚠ 주의", description="관리자 권한 또는 봇 오너여야 사용 가능한 명령어입니다.",color=0xd8ef56)
                await message.channel.send(embed=embed)
