import discord
from discord.ext import commands
import asyncio
import aiomysql
import PW
import datetime

async def check_admin(ctx):
    if (ctx.author.guild_permissions.administrator or 
        ctx.author.id == 289729741387202560):
        return True
    else:
        embed=discord.Embed(title="⚠ 주의", description="관리자 권한이 있어야 사용이 가능해요.",color=0xd8ef56)
        await ctx.send(embed=embed)

class CC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.set_db())

    async def set_db(self):
        self.conn_pool = await aiomysql.create_pool(host='127.0.0.1', user=PW.db_user, password=PW.db_pw, db='bot', autocommit=True, loop=self.loop,
                                                    minsize=2, maxsize=3, charset="utf8mb4")



    @commands.command(name="커스텀", aliases=["커스텀보기", "커스텀목록", "커보"], rest_is_raw=True)
    async def cc(self, ctx, *, args):
        message = ctx.message
        if (message.content.startswith('봇 커스텀 보기') or message.content.startswith("봇 커스텀보기") or message.content.startswith("봇 커스텀 목록") 
        or message.content.startswith("봇 커스텀목록") or message.content.startswith("봇 커보")):

            try:
                async with self.conn_pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute("""SELECT command FROM cc WHERE server = %s""", (str(ctx.guild.id)) )
                        row = await cur.fetchall()
                        if not row is ():
                            text = " | ".join(_[0] for _ in row)
                            embed=discord.Embed(title="✅ 커스텀 보기", description="%s" %(text ),color=0x1dc73a )
                            embed.set_footer(text="총 CC개수는 {}개입니다.".format(len(row)))
                            await ctx.send(embed=embed)
                        else:
                            embed=discord.Embed(title="✅ 커스텀 보기", description="이 서버엔 커스텀 명령어가 없어요! `봇 커스텀 추가 <명령어>/<대답>`으로 추가를 진행해보세요.",color=0x1dc73a )
                            await ctx.send(embed=embed)
                
            except Exception as error:
                embed=discord.Embed(title="❌ 오류 발생", description="오류로 커스텀 명령어 불러오기에 실패하였습니다. 지속적으로 문제가 발생한다면 BGM#0970 DM 바랍니다. \n```%s```" %(error) ,color=0xff0909 )
                await ctx.send(embed=embed)

        if message.content.startswith('봇 커스텀 추가'):
            if await check_admin(ctx):

                a = message.content[8:].lstrip()
                if a == "":
                    embed=discord.Embed(title="⚠ 주의", description="`봇 커스텀 추가 [명령어]/[봇의 대답]` 형식으로 작성해주세요.",color=0xd8ef56)
                    await ctx.send(embed=embed)
                else:
                    answer = ""
                    contents = a.split("/", 1)
                    command = contents[0]
                    if not command:
                        embed=discord.Embed(title="⚠ 주의", description="명령어가 정의되지 않았어요.\n`봇 커스텀 추가 [명령어]/[봇의 대답]` 형식으로 작성해주세요.",color=0xd8ef56)
                        await ctx.send(embed=embed)
                        return


                    if len(contents) >= 2:
                        for i in contents[1:]:
                            answer += i
                        answer = answer.lstrip()
                        if not answer:
                            embed=discord.Embed(title="⚠ 주의", description="대답이 정의되지 않았어요.\n`봇 커스텀 추가 [명령어]/[봇의 대답]` 형식으로 작성해주세요.",color=0xd8ef56)
                            await ctx.send(embed=embed)
                        else:
                            async with self.conn_pool.acquire() as conn:
                                async with conn.cursor() as cur:
                                    await cur.execute("""SELECT command FROM cc WHERE server = %s AND command = %s""", (str(ctx.guild.id), command))
                                    row = await cur.fetchone()

                            if not row is None:
                                embed=discord.Embed(title="⚠ 주의", description="이미 존재하는 명령어에요. 수정하시려면 `봇 커스텀 수정 [명령어]/[봇의 대답]` 을 사용해주세요.",color=0xd8ef56)
                                await ctx.send(embed=embed)
                            else:
                                async with self.conn_pool.acquire() as conn:
                                    async with conn.cursor() as cur:
                                        await cur.execute("""INSERT INTO cc (server, command, answer, who, datetime) VALUES (%s, %s, %s, %s, %s)""", ( str(ctx.guild.id), command, answer, str(ctx.author.id), str(datetime.datetime.now())     ))
                                        embed=discord.Embed(title="✅ 커스텀 추가", description="커스텀 추가를 성공했어요.",color=0x1dc73a )
                                        embed.add_field(name="명령어", value=command)
                                        embed.add_field(name="봇의 대답", value=answer)
                                        await ctx.send(embed=embed)


                    else:
                        embed=discord.Embed(title="⚠ 주의", description="`봇 커스텀 추가 [명령어]/[봇의 대답]` 형식으로 작성해주세요.",color=0xd8ef56)
                        await ctx.send(embed=embed)
    
        if message.content.startswith('봇 커스텀 수정'):
            if await check_admin(ctx):

                a = message.content[8:].lstrip()
                if a == "":
                    embed=discord.Embed(title="⚠ 주의", description="`봇 커스텀 수정 [명령어]/[봇의 대답]` 형식으로 작성해주세요.",color=0xd8ef56)
                    await ctx.send(embed=embed)
                else:
                    answer = ""
                    contents = a.split("/", 1)
                    command = contents[0]
                    if not command:
                        embed=discord.Embed(title="⚠ 주의", description="명령어가 정의되지 않았어요.\n`봇 커스텀 추가 [명령어]/[봇의 대답]` 형식으로 작성해주세요.",color=0xd8ef56)
                        await ctx.send(embed=embed)
                        return


                    if len(contents) >= 2:
                        for i in contents[1:]:
                            answer += i
                        answer = answer.lstrip()
                        async with self.conn_pool.acquire() as conn:
                            async with conn.cursor() as cur:
                                await cur.execute("""SELECT command FROM cc WHERE server = %s AND command = %s""", (str(ctx.guild.id), command))
                                row = await cur.fetchone()

                        if not answer:
                            embed=discord.Embed(title="⚠ 주의", description="대답이 정의되지 않았어요.\n`봇 커스텀 수정 [명령어]/[봇의 대답]` 형식으로 작성해주세요.",color=0xd8ef56)
                            await ctx.send(embed=embed)
                        else:

                            if not row is None:
                                async with self.conn_pool.acquire() as conn:
                                    async with conn.cursor() as cur:
                                        await cur.execute("""UPDATE cc SET answer=%s, who=%s, datetime=%s WHERE server=%s AND command=%s  """, ( answer, str(ctx.author.id), str(datetime.datetime.now()), str(ctx.guild.id), str(command)  ))
                                        embed=discord.Embed(title="✅ 커스텀 수정", description="커스텀 수정을 성공했습니다.",color=0x1dc73a )
                                        embed.add_field(name="명령어", value=command)
                                        embed.add_field(name="수정된 봇의 대답", value=answer)
                                        await ctx.send(embed=embed)

                            else:
                                embed=discord.Embed(title="⚠ 주의", description="선택하신 명령어가 존재하지 않아요. `봇 커스텀 추가 [명령어]/[봇의 대답]` 으로 추가를 해보세요!",color=0xd8ef56)
                                await ctx.send(embed=embed)


                    else:
                        embed=discord.Embed(title="⚠ 주의", description="`봇 커스텀 수정 [명령어]/[봇의 대답]` 형식으로 작성해주세요.",color=0xd8ef56)
                        await ctx.send(embed=embed)

        if message.content.startswith("봇 커스텀 삭제"):
            a = message.content[8:].lstrip()
            if await check_admin(ctx):

                if a == "":
                    embed=discord.Embed(title="⚠ 주의", description="`봇 커스텀 삭제 [삭제할 명령어]` 형식으로 작성해주세요.",color=0xd8ef56)
                    await ctx.send(embed=embed)
                else:

                    command = a.lstrip()
                    async with self.conn_pool.acquire() as conn:
                        async with conn.cursor() as cur:
                            await cur.execute("""SELECT command FROM cc WHERE server = %s AND command = %s""", (str(message.guild.id), command))
                            row = await cur.fetchone()
                    if not row is None:
                        async with self.conn_pool.acquire() as conn:
                            async with conn.cursor() as cur:
                                await cur.execute("""DELETE FROM cc WHERE server = %s AND command = %s""", (str(message.guild.id), command) )
                                embed=discord.Embed(title="✅ 커스텀 삭제", description="커스텀 삭제를 성공했어요.",color=0x1dc73a )
                                embed.add_field(name="삭제한 명령어", value=command)
                                await ctx.send(embed=embed)

                    else:
                        embed=discord.Embed(title="⚠ 주의", description="해당 명령어가 존재 하지 않아요. `봇 커스텀 추가 [명령어]/[봇의 대답]` 으로 추가를 해보세요!",color=0xd8ef56)
                        await ctx.send(embed=embed)


        if message.content == ('봇 커스텀 초기화') or message.content == ("봇 커스텀초기화"):
            if await check_admin(ctx):
                    async with self.conn_pool.acquire() as conn:
                        async with conn.cursor() as cur:
                            await cur.execute("""SELECT command FROM cc WHERE server = %s""", (str(message.guild.id)))
                            row = await cur.fetchone()
                        # print(row)
                    if row is None:
                        embed=discord.Embed(title="⚠ 주의", description="현재 이 서버에 커스텀 명령어가 존재하지 않아요.",color=0xd8ef56)
                        await ctx.send(embed=embed)
                    else:
                        embed=discord.Embed(title="⚠ 주의", description="정말로 삭제하시겠어요? (y/n)",color=0xd8ef56)
                        await ctx.send(embed=embed)
                        def usercheck(a):
                            return a.author == message.author

                        answer = await self.bot.wait_for('message', check=usercheck, timeout=30)
                        answer = answer.content
                        
                        if answer == "y":
                            async with self.conn_pool.acquire() as conn:
                                async with conn.cursor() as cur:
                                    await cur.execute("DELETE FROM cc WHERE server = %s", (str(message.guild.id)))
                                    embed=discord.Embed(title="✅ 커스텀 초기화", description="커스텀 초기화를 성공적으로 진행했어요.",color=0x1dc73a )
                                    await ctx.send(embed=embed)

                        elif answer == "n":
                            embed=discord.Embed(title="⚠ 주의", description="진행이 취소되었습니다.",color=0xd8ef56)
                            await ctx.send(embed=embed)

                        else:
                            embed=discord.Embed(title="⚠ 주의", description="잘못된 선택으로 취소되었습니다.",color=0xd8ef56)
                            await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(CC(bot))