import discord
from discord.ext import commands
import PW
import asyncio
import aiomysql


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.set_db())

    async def set_db(self):
        self.conn_pool = await aiomysql.create_pool(host='127.0.0.1', user=PW.db_user, password=PW.db_pw, db='bot', autocommit=True, loop=self.loop,
                                                    minsize=2, maxsize=5, charset="utf8mb4")
    async def cog_check(self, ctx):
        if ctx.guild is None:
            return False
        if ctx.author.guild_permissions.administrator or ctx.author.id == 289729741387202560:
            return True
        else:
            embed=discord.Embed(title="⚠ 주의", description="이 명령어를 사용하려면 서버에 관리자 권한이 있어야 해요.",color=0xd8ef56)
            await ctx.send(embed=embed)


    @commands.command(name="뮤트")
    @commands.guild_only()
    async def mute(self, ctx):
        try:
            
            if not ctx.message.mentions == []:
                member = ctx.message.mentions[0]
                overwrite = discord.PermissionOverwrite()
                overwrite.send_messages = False
                await ctx.channel.set_permissions(member, overwrite=overwrite)
                embed=discord.Embed(title="✅ 유저 뮤트", description="뮤트를 성공했습니다.",color=0x1dc73a)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title="⚠ 주의", description="`봇 뮤트 @유저` 형식으로 명령어를 사용해주세요. 선택된 사용자가 없어요.",color=0xd8ef56)
                await ctx.send(embed=embed)
                
        except:
            embed=discord.Embed(title="❌ 오류 발생", description="뮤트를 실패하였습니다. 권한을 확인해 주세요. "  ,color=0xff0909)    
            await ctx.send(embed=embed)

    @commands.command(name="언뮤트", aliases=["뮤트해제"])
    @commands.guild_only()
    async def unmute(self, ctx):
        try:
            if not ctx.message.mentions == []:
                member = ctx.message.mentions[0]
                overwrite = discord.PermissionOverwrite()
                overwrite.send_messages = None
                await ctx.channel.set_permissions(member, overwrite=overwrite)
                embed=discord.Embed(title="✅ 유저 언뮤트", description="언뮤트를 성공했습니다.",color=0x1dc73a )
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title="⚠ 주의", description="`봇 언뮤트 @유저` 형식으로 명령어를 사용해주세요. 선택된 사용자가 없어요.",color=0xd8ef56)
                await ctx.send(embed=embed)
                
        except:
            embed=discord.Embed(title="❌ 오류 발생", description="뮤트를 실패하였습니다. 권한을 확인해 주세요." ,color=0xff0909)    
            await ctx.send(embed=embed)


    @commands.command(name="전체뮤트", aliases=["채널뮤트"])
    @commands.guild_only()
    async def channel_mute(self, ctx):
        try:
            role = discord.utils.get(ctx.guild.roles, name='@everyone')
            await ctx.channel.set_permissions(role, send_messages=False)
            embed=discord.Embed(title="✅ 전체 뮤트", description="관리자를 제외한 모든 유저의 뮤트를 성공했어요.",color=0x1dc73a )
            embed.set_footer(text="명령어를 사용한 채널에서만 적용돼요.")
            await ctx.send(embed=embed)
        except:
            embed=discord.Embed(title="❌ 오류 발생", description="뮤트를 실패하였습니다. 권한을 확인해 주세요." ,color=0xff0909)    
            await ctx.send(embed=embed)

    @commands.command(name="전체언뮤트", aliases=["전체뮤트해제", "전체뮤트 해제", "채널뮤트해제"])
    @commands.guild_only()
    async def channel_unmute(self, ctx):
        try:
            role = discord.utils.get(ctx.guild.roles, name='@everyone')
            await ctx.channel.set_permissions(role, send_messages=None)
            embed=discord.Embed(title="✅ 전체 언뮤트", description="전체뮤트의 해제를 성공했어요.",color=0x1dc73a )
            embed.set_footer(text="명령어를 사용한 채널에서만 적용돼요.")
            await ctx.send(embed=embed)

        except: 
            embed=discord.Embed(title="❌ 오류 발생", description="언뮤트를 실패하였습니다. 권한을 확인해 주세요." ,color=0xff0909)    
            await ctx.send(embed=embed)

    @commands.command(name="밴", aliases=["차단"])
    @commands.guild_only()
    async def ban(self, ctx):
        try:
            if not ctx.message.mentions == []:
                member = ctx.message.mentions[0]
                await ctx.guild.ban(member,reason=str(ctx.author) + "님의 명령어 사용으로 인해 밴 당하셨습니다.", delete_message_days=7)
                embed=discord.Embed(title="✅ 유저 밴", description="유저의 밴을 완료했습니다.",color=0x1dc73a )
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title="⚠ 주의", description="`봇 밴 @유저` 형식으로 명령어를 사용해주세요. 선택된 사용자가 없어요.",color=0xd8ef56)
                await ctx.send(embed=embed)
        except:
            embed=discord.Embed(title="❌ 오류 발생", description="밴을 실패하였습니다. 권한을 확인해보세요." ,color=0xff0909)    
            await ctx.send(embed=embed)

    @commands.command(name="언밴", alliases=["차단해제"], rest_is_raw=True)
    @commands.guild_only()
    async def unban(self, ctx, *, args):
        try:    
            memberid = args.lstrip()
            memberid = memberid.replace("<", "")
            memberid = memberid.replace("@", "")
            memberid = memberid.replace("!", "")
            memberid = memberid.replace(">", "")
            memberid = int(memberid)
            if not memberid == "":
                await ctx.guild.unban(self.bot.get_user(memberid))
                embed=discord.Embed(title="✅ 유저 언밴", description="유저의 언밴을 완료했어요.",color=0x1dc73a )
                await ctx.send(embed=embed)
        
            else:
                embed=discord.Embed(title="⚠ 주의", description="`봇 언밴 [유저ID]` 형식으로 명령어를 사용해주세요. 선택된 사용자가 없어요.",color=0xd8ef56)
                await ctx.send(embed=embed)
        
        except Exception as error:
            embed=discord.Embed(title="❌ 오류 발생", description="언밴을 실패하였습니다. 권한을 확인해보세요.{}".format(error) ,color=0xff0909)    
            await ctx.send(embed=embed)

    @commands.command(name="킥", aliases=["강제퇴장", "강퇴"])
    async def kick(self, ctx):
        try:
            if not ctx.message.mentions == []:
                member = ctx.message.mentions[0]
                await ctx.guild.kick(member,reason=str(ctx.author) + "님의 명령어 사용으로 인해 킥 당하셨습니다.")
                embed=discord.Embed(title="✅ 멤버 킥", description="킥을 날렸어요.",color=0x1dc73a)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title="⚠ 주의", description="`봇 킥 @유저` 형식으로 명령어를 사용해주세요. 선택된 사용자가 없어요.",color=0xd8ef56)
                await ctx.send(embed=embed)
                
        except:
            embed=discord.Embed(title="❌ 오류 발생", description="킥을 실패하였습니다. 권한을 확인해 주세요." ,color=0xff0909)    
            await ctx.send(embed=embed)

    @commands.command(name="지우기", aliases=["삭제"])
    async def delete_message(self, ctx, amount:int):
        if amount > 0 and amount <= 100:
            deleted_message = await ctx.channel.purge(limit=amount )
            embed=discord.Embed(title="✅ 메시지 삭제", description="%s개의 메시지를 지웠어요." %len(deleted_message),color=0x1dc73a )
            await ctx.send(embed=embed, delete_after=3)
        else:
            embed=discord.Embed(title="⚠ 오류 발생", description="지우는 개수는 1개~100개여야 해요.",color=0xff0909 )
            await ctx.send(embed=embed, delete_after=3)

    @delete_message.error
    async def delete_message_error(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="⚠ 오류 발생", description="`봇 지우기 <지울 메시지의 숫자>`로 사용해주세요!", color=0xff0909 )
            await ctx.send(embed=embed)
    

    @commands.command(name="웰컴설정", aliases=["환영설정"])
    async def set_welcome_message(self, ctx):
        async with self.conn_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""SELECT id, welcome, welcome_message FROM welcome WHERE id=%s""", (ctx.guild.id))
                row = await cur.fetchone()
        
        if row is None or row[1] == 0:
            embed=discord.Embed(title="📝 웰컴 설정", description="현재 웰컴 메시지가 설정되어 있지 않아요. 추가하시려면 ✅ 이모티콘을 눌러주세요.")
            msg = await ctx.send(embed=embed)
            await msg.add_reaction("✅")

            def posi_check(reaction, user):
                # if user.is_bot: return False
                return user == ctx.author and str(reaction.emoji) == '✅' and msg.id == reaction.message.id

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=posi_check)
                if str(reaction) == "✅":
                    edit = True
                else:
                    return
            except:
                await ctx.send("타임아웃으로 취소되었어요.")
                return

        else:
            embed=discord.Embed(title="📝 웰컴 설정", description="현재 웰컴 메시지는 다음과 같습니다.\n```%s```\n\n 수정하시려면 ✅ 이모티콘을, 제거하시려면 ❌ 이모티콘을 클릭해주세요. " %(row[2]))
            embed.set_footer(text="메시지는 `서버 설정 > NEW MEMEBR MESSAGES CHANNEL`에 보내집니다.")        
            msg = await ctx.send(embed=embed)
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")


            def posi_check2(reaction, user):
                # # if user.is_bot: return False
                # print(user, ctx.author, msg.id, reaction.message.id)
                return user == ctx.author and ( str(reaction.emoji) == '✅' or str(reaction.emoji)  == "❌" ) and msg.id == reaction.message.id

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=posi_check2)
                if str(reaction) == "✅":
                    edit = True
                    print(edit)
                else:
                    edit = False
            except:
                await ctx.send("타임아웃으로 취소되었어요.")
                return

        
        if edit:
            embed=discord.Embed(title="📝 웰컴 설정", description="유저가 들어올때 봇이 보낼 메시지를 설정해주세요. 취소하시려면 `봇 취소` 를 입력하세요.\n\n{멘션} > 유저를 언급합니다.\n{서버이름} > 서버 이름을 표시합니다.")            
            await ctx.send(embed=embed)

            def check_msg(m):
                return m.channel == ctx.channel and m.author == ctx.author

            msg = await self.bot.wait_for('message', check=check_msg)
            if msg.content == "봇 취소":
                await ctx.send("취소되었습니다.")
            else:
                async with self.conn_pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute("""INSERT INTO welcome (id, welcome, welcome_message) VALUES (%s, %s, %s)  ON DUPLICATE KEY UPDATE welcome=%s, welcome_message=%s;""", (ctx.guild.id, 1, msg.content, 1, msg.content))
                embed=discord.Embed(title="✅ 웰컴 메시지", description="```%s```\n로 웰컴 메시지가 설정되었습니다." %(msg.content),color=0x1dc73a )
                embed.set_footer(text="메시지는 `서버 설정 > NEW MEMEBR MESSAGES CHANNEL`에 보내집니다.")        

                await ctx.send(embed=embed)
                
        else:
            async with self.conn_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("""INSERT INTO welcome (id, welcome, welcome_message) VALUES (%s, %s, %s)  ON DUPLICATE KEY UPDATE welcome='%s';""", (ctx.guild.id, 0, None, 0))
                embed=discord.Embed(title="✅ 웰컴 메시지", description="웰컴 메시지 사용이 중지되었습니다.",color=0x1dc73a )
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Admin(bot))