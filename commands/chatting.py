import discord
from discord.ext import commands
import os
from bs4 import BeautifulSoup
import lxml
import datetime
import asyncio
import aiohttp
import random
import TOKEN
import json

def htmltotext(html):
    soup = BeautifulSoup(html)
    text_parts = soup.findAll(text=True)
    return ''.join(text_parts)

def right_check(a):
    try:
        if a is None or a == "":
            return "정보가 없습니다."

        else:
            return a

    except:
        return "정보를 찾을 수 없습니다."


def lxml_string(soup, tag):
    try:    
        find = soup.find(tag).string
        if find is None or find == "":
            return "정보가 존재하지 않음."
        else:
            return find
    except:
        return "정보 없음."


def checkpm10(n):
    try:
        n = int(n)
        if n >= 0 and n < 31:
            return "좋음"
        elif n >= 31 and n < 81:
            return "보통"
        elif n >= 80 and n < 151:
            return "`나쁨`"
        elif n >= 151:
            return "**`매우 나쁨`**" 

    except:
        return ""

def checkpm25(n):
    try:
        n = int(n)
        if n >= 0 and n < 16:
            return "좋음"
        elif n >= 16 and n < 36:
            return "보통"
        elif n >= 36 and n < 76:
            return "`나쁨`"
        elif n >= 76:
            return "**`매우 나쁨`**" 

    except:
        return ""


def earthquake(source):
    source = source.text.strip()
    if source:
        return source
    elif source == "" or source is None:
        return "정보가 없습니다."

async def nmt(source, target, string):
    headers = {"X-Naver-Client-Id" : TOKEN.papago_nmt_id, "X-Naver-Client-Secret" : TOKEN.papago_nmt_secret}
    data = {"source":source, "target":target, "text":string}
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post("https://openapi.naver.com/v1/papago/n2mt", data=data) as r:
                    if r.status == 200:
                        c = await r.json()
                        translated = c["message"]["result"]["translatedText"]
                        return translated
                    else:
                        return None
    except:
        return None                

async def smt(source, target, string):
    headers = {"X-Naver-Client-Id" : TOKEN.papago_smt_id, "X-Naver-Client-Secret" : TOKEN.papago_smt_secret}
    data = {"source":source, "target":target, "text":string}
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post("https://openapi.naver.com/v1/language/translate", data=data) as r:
                    if r.status == 200:
                        c = await r.json()
                        translated = c["message"]["result"]["translatedText"]
                        return translated
                    else:
                        return None
    except:
        return None                

class Chatting(commands.Cog):
    def __init__(self, bot):
        super()
        self.bot = bot
        self.bot_start_time = datetime.datetime.utcnow()

    @commands.command(name="안녕", aliases=['ㅎㅇ', 'gdgd', 'gd', '안냥', '안녕하세요', 'hello', '안뇽', '안뇨옹'])
    async def hello(self, ctx):
        bot_profile = self.bot.user.avatar_url
        embed = discord.Embed(
            title="👋 안녕하세요!", description="**봇을 사용해 주셔서 고마워요!**\n봇 / BOT은 BGM#0970이 개발중인 디스코드 봇이에요.\n\n자세한 내용은 `봇 도움` 명령어를 사용해서 볼 수 있어요.", color=0x237ccd)
        embed.set_thumbnail(url=bot_profile)
        await ctx.send(embed=embed)

    # @commands.command(name='connect', aliases=['컴','야 들어와'])

    @commands.command(name="온도", ailases=["서버온도"])
    async def server_temp(self, ctx):
        try:
            a = os.popen("vcgencmd measure_temp").read()
            a = a.replace("temp=", "")
            a = a.replace("'C", "")
            a = a.replace("\n", "")
            a = float(a)
            if a < 45:
                embed = discord.Embed(
                    title="✅ 서버 온도", description="현재 서버 온도는 %s°C 이에요." % (str(a)), color=0x1dc73a)
                embed.set_footer(text="온도가 좋아요.")

            if 45 <= a and a < 50:
                embed = discord.Embed(
                    title="⚠ 서버 온도", description="현재 서버 온도는 %s°C 이에요." % (str(a)), color=0xd8ef56)
                embed.set_footer(text="온도가 보통이에요.")
            if 50 <= a:
                embed = discord.Embed(
                    title="❌ 서버 온도", description="현재 서버 온도는 %s°C 이에요." % (str(a)), color=0xff0909)
                embed.set_footer(text="온도가 높네요.")
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(
                title="⚠ 오류", description="시스템에서 온도를 불러오는데에 실패했어요.", color=0xff0909)
            await ctx.send(embed=embed)

    @commands.command(name="따라해", rest_is_raw=True)
    async def repeat(self, ctx, *, args):
        if args == "":
            embed = discord.Embed(
                title="⚠ 주의", description="봇 따라해 `할말`로 입력해주세요!\n아무 값도 받지 못했어요.", color=0xd8ef56)
            await ctx.channel.send(embed=embed)
            return

        if "@everyone" in args or "@here" in args:
            embed = discord.Embed(
                title="⚠ 경고", description="`@everyone`이나 `@here`은 다른 사용자에게 피해를 줄 수 있어요.\n사용을 제한할께요!", color=0xff0909)
            embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed=embed)
        else:
            try:
                await ctx.delete()
            except:
                pass
            await ctx.channel.send(args)

    @commands.command(name="거꾸로", rest_is_raw=True)
    async def reverse(self, ctx, *, args):
        if args == "":
            embed = discord.Embed(
                title="⚠ 주의", description="봇 거꾸로 `할말`로 입력해주세요!\n아무 값도 받지 못했어요.", color=0xd8ef56)
            await ctx.channel.send(embed=embed)
            return

        args = ''.join(reversed(args))
        if "@everyone" in args or "@here" in args:
            embed = discord.Embed(
                title="⚠ 경고", description="`@everyone`이나 `@here`은 다른 사용자에게 피해를 줄 수 있어요.\n사용을 제한할께요!", color=0xff0909)
            embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed=embed)
        else:
            try:
                await ctx.delete()
            except:
                pass
            await ctx.channel.send(args)

    @commands.command(name="서버랭크", aliases=["서버랭", "서버 랭크", "서버 랭"])
    async def server_rank(self, ctx):
        rank = {}
        allguild = self.bot.guilds
        for i in allguild:
            rank[i] = int(i.member_count)
        rank = sorted(rank, key=lambda k: rank[k], reverse=True)
        number = 0
        totalserver = str(len(allguild))
        totalperson = 0
        embed = discord.Embed(
            title="🥇 서버 랭크", description="(서버 이름 / 인원수)로 보여줘요! ", color=0x237ccd)

        for i in rank:
            number += 1
            totalperson += int(i.member_count)
            embed.add_field(name=str(number)+"위", value="%s / %s명" %
                            (i.name, i.member_count), inline=False)

            if number == 10:
                break
        embed.set_footer(text="전체 서버 개수는 %s개입니다." %
                         (str(len(self.bot.guilds))))
        await ctx.send(embed=embed)

    @commands.command(name='샤드')
    async def which_shard(self, ctx):
        if ctx.guild is None:
            pass

        else:
            embed = discord.Embed(
                title="🖥 샤드", description="현재 이 서버는 샤드 {}번에 있어요!".format(ctx.guild.shard_id), color=0x237ccd)
            await ctx.send(embed=embed)

    @commands.command(name="도움", rest_is_raw=True)
    async def help(self, ctx, *, args):
        a = args.lstrip()
        if a == "" or a is None:
            embed = discord.Embed(
                title="📜 도움말", description="봇의 사용을 도와줄 도움말이에요. 다음 명령어 그룹들을 참고하세요.", color=0x237ccd)
            # embed.add_field(name="봇 도움 기타", value="기타 도움말입니다. 자세한 명령어는 '봇 도움 기타'을 참고하세요.", inline=False)
            # embed.add_field(name="봇 도움 게임", value="봇에 있는 게임 기능에 관련된 도움말입니다. 자세한 명령어는 '봇 도움 게임'을 참고하세요.", inline=True)
            embed.add_field(
                name="봇 도움 기능", value="봇에 있는 기능에 대해 알려드려요.", inline=True)
            embed.add_field(
                name="봇 도움 어드민", value="어드민이 서버 관리를 위해 사용 가능한 기능입니다. 자세한 명령어는 '봇 도움 어드민'을 참고하세요.", inline=True)
            embed.add_field(name="더 많은 기능은?",
                            value="문의는 BGM#0970으로 친추 후 DM해주세요!", inline=False)

            embed.set_footer(text="도움 명령어에 없는 명령어가 있을 수 있을 수 있어요.")
            try:
                await ctx.author.send(embed=embed)
                await ctx.send("DM으로 메시지를 보냈습니다. 확인하세요.")
            except:
                embed = discord.Embed(
                    title="⚠ 주의", description="DM 보내기에 실패했어요. 계정에서 DM 설정을 확인해주세요.", color=0xd8ef56)
                await ctx.send(embed=embed)
        # elif a == "게임":
        #     embed=discord.Embed(title=" ", description="봇에 있는 채팅 기능을 설명합니다.", color=0x237ccd)
        #     embed.add_field(name="봇 끝말잇기", value="봇과 끝말잇기를 할 수 있습니다. 제한시간은 10초입니다.", inline=False)
        #     embed.add_field(name="봇 숫자게임", value="1~10까지 중 랜덤으로 뽑은 숫자에서, 봇보다 숫자가 크면 승리입니다.", inline=True)
        #     embed.add_field(name="봇 카드게임", value="A ~ K 까지의 카드에서 높은 숫자가 나오면 승리합니다.", inline=True)
        #     embed.add_field(name="봇 컵게임", value="3개의 컵중에 동전이 들어간 컵을 찾는 게임입니다.", inline=True)
        #     embed.add_field(name="봇 도박 컵 <배팅금액> <배수>", value="컵게임과 같은 방식입니다. 단, 배수가 늘어날수록 컵의 개수도 그만큼 늘어납니다.", inline=True)

        #     embed.set_footer(text="도움 명령어에 없는 명령어가 있을 수 있습니다.")
        #     try:
        #         await message.author.send(embed=embed)
        #     except:
        #         embed=discord.Embed(title="⚠ 주의", description="DM 보내기에 실패하였습니다. 계정에서 DM 설정을 확인해주세요.",color=0xd8ef56)
        #         await ctx.send(embed=embed)

        elif a == "기능":
            embed = discord.Embed(
                title=" ", description="봇에 있는 편리한 기능을 설명합니다.", color=0x237ccd)
            embed.add_field(
                name="봇 프사 @상대", value="멘션한 상대의 프로필 사진을 가져와요. 상대를 지정하지 않으면 자신의 프로필 사진을 가져와요.", inline=False)
            embed.add_field(name="봇 백과사전 <검색어>",
                            value="백과사전에서 검색어를 검색해줍니다.", inline=False)
            embed.add_field(
                name="봇 나무위키 <검색어>", value="해당 나무위키 검색어로 바로가는 나무위키 링크를 표시하고, 문서를 일부분 미리 볼 수 있습니다.")
            # embed.add_field(name="봇 도서검색 <검색어>", value="도서를 검색해줍니다.", inline=False)
            embed.add_field(name="봇 afk/잠수 <사유>",
                            value="나중에 다시 오시면 알려드려요.", inline=False)
            embed.add_field(name="봇 자동번역 <번역할 문장>",
                            value="언어를 자동으로 인식한 후 한국어로 번역합니다.")
            embed.add_field(name="봇 한글영어번역(영어한글번역, 일어한글번역, 한글일어번역) <번역할 문장>",
                            value="선택한 언어에서 선택한 언어로 번역해줍니다.", inline=False)
            embed.add_field(name="봇 초대", value="봇의 초대링크를 전송해요.", inline=False)

            # embed.add_field(name="봇 죽창 <개수>", value="죽창을 표시합니다. 60개가 최대입니다.",inline=False)
            embed.add_field(name="봇 지진", value="지진 정보를 표시합니다.", inline=False)
            # embed.add_field(name="봇 별명변경 <바꿀별명>", value="입력한 별명으로 별명을 변경합니다.", inline=False)
            embed.add_field(
                name="봇 조의 표해", value="봇이 조의를 표해줍니다.", inline=False)
            embed.add_field(name="봇 고양이/냥이",
                            value="랜덤으로 고양이짤을 보여준다냐!", inline=False)
            embed.add_field(
                name="봇 강아지", value="랜덤으로 강아지짤을 보여준다멍.", inline=False)
            embed.add_field(name="봇 리마인더 <시간(초)> <사유(선택)>",
                            value="선택한 초 있다가 알려드려요.", inline=False)
            embed.add_field(
                name="봇 링크축약 [축약할 주소]", value="네이버 서비스를 이용하여 긴 주소를 짧게 만들어 드립니다.", inline=False)

            embed.add_field(
                name="봇 기상특보", value="기상특보 정보를 표시합니다.", inline=False)
            embed.add_field(
                name="봇 미세먼지", value="미세먼지 정보를 표시합니다.", inline=False)
            # embed.add_field(name="봇 11번가 검색 <검색어>", value="11번가에서 검색해, 정보를 불러옵니다.", inline=False)
            embed.add_field(
                name="봇 초미세먼지", value="초미세먼지 정보를 표시합니다.", inline=False)
            # embed.add_field(name="봇 멜론차트", value="멜론 TOP10을 보여줍니다.", inline=False)
            embed.add_field(
                name="봇 가사검색", value="선택한 노래의 가사를 검색해줍니다. 가끔 다른 노래 가사가 들어갈수도 있으니 자세히 보기로 확인해보시는것도 좋아요!", inline=False)
            embed.add_field(
                name="봇 날씨 [도시]", value="선택한 도시의 현재 날씨를 보여줍니다.", inline=False)

            embed.add_field(name="더 많은 기능은?",
                            value="문의는 BGM#0970으로 친추 후 DM해주세요!", inline=False)

            # embed.add_field(name="봇 명언은?", value="명언을 표시합니다. (명언인지 확인안됨)", inline=False)
            # embed.add_field(name="봇 서버 인원은?", value="채팅한 서버의 인원을 표시합니다.", inline=False)

            embed.set_footer(text="도움 명령어에 없는 명령어가 있을 수 있어요.")
            try:
                await ctx.author.send(embed=embed)
            except:
                embed = discord.Embed(
                    title="⚠ 주의", description="DM 보내기에 실패했어요. 계정에서 DM 설정을 확인해주세요.", color=0xd8ef56)
                await ctx.send(embed=embed)
        elif a == "어드민":
            embed = discord.Embed(
                title=" ", description="봇에 있는 서버의 관리자가 사용할때 유용한 기능입니다.", color=0x237ccd)
            embed.add_field(
                name="봇 킥 @유저", value="선택한 유저를 킥합니다.", inline=False)
            embed.add_field(
                name="봇 밴 @유저", value="선택한 유저를 밴합니다.", inline=False)
            embed.add_field(name="봇 언밴 @유저 또는 유저 ID ",
                            value="선택한 유저를 언밴합니다. 유저 ID는 데스크톱 버전에서 오른쪽키 > ID복사로 얻으실 수 있습니다.", inline=False)
            embed.add_field(name="봇 뮤트 @유저",
                            value="유저를 해당 채널에서 뮤트시킵니다.", inline=False)
            embed.add_field(
                name="봇 전체뮤트", value="명령어를 사용한 채널을 관리자 제외 모든 유저가 사용할 수 없도록 합니다.", inline=False)
            embed.add_field(name="봇 언뮤트 @유저",
                            value="유저를 해당 채널에서 언뮤트시킵니다.", inline=False)
            embed.add_field(name="봇 전체언뮤트", value="전체뮤트를 해제합니다.", inline=False)
            embed.add_field(name="봇 커스텀 추가 <명령어>/<봇의 대답>",
                            value="해당 서버만 사용되는 커스텀 명령어를 추가합니다. 명령어와 봇의 대답 구분에는 꼭 /가 필요합니다.", inline=False)
            embed.add_field(name="봇 커스텀 수정 <수정할 명령어>/<봇의 대답>",
                            value="이미 추가된 커스텀 명령어를 수정합니다. 명령어와 봇의 대답 구분에는 꼭 /가 필요합니다.", inline=False)
            embed.add_field(name="봇 커스텀 보기",
                            value="해당 서버의 모든 커스텀 명령어를 출력합니다.", inline=False)
            embed.add_field(
                name="봇 커스텀 삭제 [삭제할 커스텀 명령어]", value="해당 서버의 커스텀 명령어중 입력한 명령어를 삭제합니다.", inline=False)
            embed.add_field(name="봇 커스텀 초기화",
                            value="해당 서버의 모든 커스텀 명령어를 삭제합니다.", inline=False)
            embed.add_field(name="봇 웰컴설정/환영설정",
                            value="서버에 새로운 사람이 오면 보낼 메시지를 설정합니다.", inline=False)
            embed.add_field(name="더 많은 기능은?",
                            value="문의는 BGM#0970으로 친추 후 DM해주세요!", inline=False)

            embed.set_footer(text="도움 명령어에 없는 명령어가 있을 수 있습니다.")

            try:
                await ctx.author.send(embed=embed)
            except:
                embed = discord.Embed(
                    title="⚠ 주의", description="DM 보내기에 실패했어요. 계정에서 DM 설정을 확인해주세요.", color=0xd8ef56)
                await ctx.send(embed=embed)
        # elif a == "기타":
        #     embed=discord.Embed(title=" ", description="봇에 있는 다른 잡다한 기능들을 소개합니다.", color=0x237ccd)
        #     embed.add_field(name="봇 철컹철컹", value="??? : 철컹", inline=False)
        #     try:
        #         await message.author.send(embed=embed)
        #     except:
        #         embed=discord.Embed(title="⚠ 주의", description="DM 보내기에 실패하였습니다. 계정에서 DM 설정을 확인해주세요.",color=0xd8ef56)
        #         await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                title="⚠ 주의", description="해당 도움 그룹이 없어요. 존재하는 도움 그룹은 \n```기능, 어드민``` 입니다.", color=0xd8ef56)
            await ctx.send(embed=embed)

    @commands.command(name="초대", aliases=["초대링크", "초대 링크"])
    async def invite(self, ctx):
        embed = discord.Embed(
            title="✅ 봇 초대", description="초대하시려면 [여기](https://discordapp.com/oauth2/authorize?client_id=351733476141170688&scope=bot&permissions=2146958847)를 클릭해주세요!", color=0x1dc73a)
        await ctx.send(embed=embed)

    @commands.command(name="시간계산", aliases=["시간 계산"], rest_is_raw=True)
    async def time_calc(self, ctx, *, args):
        try:
            if args.lstrip() == "":
                embed = discord.Embed(
                    title="⏲ 시간 계산", description="yyyy-mm-dd 형식으로 입력해주세요.", color=0x237ccd)
                await ctx.send(embed=embed)

                def usercheck(a):
                    return a.author == ctx.author and a.channel == ctx.channel

                answer = await self.bot.wait_for('message', check=usercheck)
                answer = answer.content
                now = datetime.datetime.now()
                answer = datetime.datetime.strptime(answer, "%Y-%m-%d")
                dap = answer - now
                print(dap)
                days = dap.days
                hours, remainder = divmod(dap.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                # 초 (실험)
                seconds += dap.microseconds / 1e6
                embed = discord.Embed(title="⏲ 시간 계산", description=str(days) + "일 " + str(hours) + "시간 " + str(
                    minutes) + "분 " + str(int(round(seconds, 0))) + "초 남았어요.", color=0x237ccd)
                embed.set_footer(text="과거 시간은 계산값이 정확하지 않아요.")

                await ctx.send(embed=embed)

            else:
                answer = args.lstrip()

        except Exception as error:
            embed = discord.Embed(
                title="❌ 오류 발생", description="형식을 제대로 입력하셨는지 학인하시거나, 값 한도를 초과했는지 확인해주세요.. \n\n0001-01-01 ~ 9999-12-31 %s" % (error), color=0xff0909)
            await ctx.send(embed=embed)
    @commands.command(name="별명변경", rest_is_raw=True)
    async def nickname(self, ctx, *, args):
        try:
            b = args.lstrip()
            memberid = ctx.author.id
            member = ctx.guild.get_member(memberid)

            await member.edit(nick=b)
            embed=discord.Embed(title="✅ 별명 변경", description="별명 변경에 성공하였습니다.",color=0x1dc73a )

            await ctx.send(embed=embed)
        except:
            embed=discord.Embed(title="❌ 오류 발생", description="봇의 권한이 부족하거나 사용자의 권한이 봇보다 높습니다.",color=0xff0909)
            await ctx.send(embed=embed)


    @commands.command(name="핑", aliases=["퐁"])
    async def ping(self, ctx):
        ping = str(int(self.bot.latency*1000))
        embed = discord.Embed(title="🏓 퐁! " + ping + "ms",
                              description="Discord WebSocket 프로토콜의 레이턴시에요!", color=0x237ccd)
        # embed.set_footer(text="이 수치는 봇이 메시지에 반응하는 속도입니다.")
        await ctx.send(embed=embed)

    @commands.command(name="문의", aliases=["건의", "기능건의", "기능문의"])
    async def qna(self, ctx):
        embed=discord.Embed(title="❔ 건의", description="건의하실 내용을 입력해주세요. 개발자에게 직접 전송됩니다.",color=0x1dc73a )
        await ctx.send(embed=embed)
        def qnacheck(qna):
            return qna.author == ctx.author and qna.channel == ctx.channel
        answer = await self.bot.wait_for('message', check=qnacheck)
        bgm = self.bot.get_user(289729741387202560)
        embed=discord.Embed(title="❔ 건의가 도착했어요!", description=answer.content,color=0x1dc73a, timestamp=datetime.datetime.utcnow() )
        embed.set_footer(icon_url=ctx.author.avatar_url, text="{} / {}".format(ctx.author, ctx.author.id))
        await bgm.send(embed=embed)
        embed=discord.Embed(title="✅ 성공", description="건의 전송을 성공했어요!",color=0x1dc73a)
        await ctx.send(embed=embed)
    

    @commands.command(name="리마인더", aliases=["알려줘"], rest_is_raw=True)
    async def reminder(self, ctx, *, args):
        a = args
        a = a.lstrip().split()
        try:
            set_time = int(a[0])
            try:
                del a[0]
                reason = ""
                for i in a:
                    reason = reason + i + " "
                if not reason == "":
                    embed = discord.Embed(title="✅ 리마인더", description="리마인더에 기록 완료했어요! %s초 있다가 `%s`하라고 알려드릴께요!" % (
                        str(set_time), reason), color=0x1dc73a)
                else:
                    embed = discord.Embed(title="✅ 리마인더", description="리마인더에 기록 완료했어요! %s초 있다가 알려드릴께요!" % (
                        str(set_time)), color=0x1dc73a)

            except IndexError as error:
                await ctx.send(error)
            embed.set_footer(text="봇이 꺼지면 초기화됩니다!")
            await ctx.send(embed=embed)
            await asyncio.sleep(set_time)
            await ctx.send(ctx.author.mention)
            embed = discord.Embed(
                title="⏰ 알림", description="시간이 다 되었어요!", color=0x1dc73a)
            if not reason == "":
                embed.add_field(name="내용", value=reason)
            await ctx.send(embed=embed)

        except Exception as error:
            embed = discord.Embed(
                title="❌ 오류 발생", description="봇 리마인더 <시간(초)> <사유(선택)> 형식으로 사용해주세요. \n```%s```     " % (error), color=0xff0909)
            await ctx.send(embed=embed)

    @commands.command(name="조의 표해", aliases=["조의 표헤", "joy", "조의"])
    async def joy(self, ctx):
        await ctx.message.add_reaction("❌")
        await ctx.message.add_reaction("✖")
        await ctx.message.add_reaction("🇽")
        await ctx.message.add_reaction("🇯")
        await ctx.message.add_reaction("🇴")
        await ctx.message.add_reaction("🇾")

    @commands.command(name="지진", aliases=["지진희", "강진"])
    async def get_earthquake(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://m.kma.go.kr/m/eqk/eqk.jsp?type=korea") as r:

                c = await r.text()
                soup = BeautifulSoup(c, "html.parser")
                table = soup.find("table", {"class": "table02 style01"})
                td = table.find_all("td")

                date = earthquake(td[1])
                gyumo = earthquake(td[3])
                jindo = earthquake(td[5])
                location = earthquake(td[7])
                depth = earthquake(td[9])
                detail = earthquake(td[10])

                embed = discord.Embed(
                    title="지진 정보", description=date, color=0x62bf42)
                try:
                    img = soup.find(
                        "div", {"class": "img-center"}).find("img")['src']
                    img = "http://m.kma.go.kr" + img
                    if img is None:
                        pass
                    else:
                        embed.set_image(url=img)

                except:
                    pass

                embed.add_field(name="규모", value=gyumo, inline=True)
                embed.add_field(name="발생위치", value=location, inline=True)
                embed.add_field(name="발생깊이", value=depth, inline=True)
                embed.add_field(name="진도", value=jindo, inline=True)
                embed.add_field(name="참고사항", value=detail, inline=True)
                embed.set_footer(text="기상청")

                await ctx.send(embed=embed)

    @commands.command(name="골라", aliases=["선택", "골라줘", "선택해줘"], rest_is_raw=True)
    async def choice(self, ctx, *, args):
        content = args.lstrip()
        if content == "":
            embed=discord.Embed(title="❔ 봇의 선택", description="항목을 받지 못했어요! 명령어 사용법은 \n```봇 골라 <항목1>, <항목2>...```\n형식이에요!",color=0x1dc73a )
            await ctx.send(embed=embed)
            return

        if "@everyone" in content or "@here" in content:
            embed=discord.Embed(title="⚠ 경고", description="`@everyone`이나 `@here`은 다른 사용자에게 피해를 줄 수 있어요.\n사용을 제한할께요!" ,color=0xff0909 )
            embed.set_footer(text=ctx.author)
            await ctx.send(embed=embed)
        else:
            
            a = content.split(",")
            a = random.choice(a)
            embed=discord.Embed(title="❔ 봇의 선택", description=a,color=0x1dc73a )
            await ctx.send(embed=embed)

    @commands.command(name="기상특보", aliases=["기상 특보", "기상"])
    async def weather_warn(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('http://newsky2.kma.go.kr/service/WetherSpcnwsInfoService/SpecialNewsStatus?serviceKey=' + TOKEN.weather_warn) as r:
                c = await r.text()
                soup = BeautifulSoup(c,"lxml-xml")
                title = lxml_string(soup, "t1")
                area = lxml_string(soup, "t2")
                content = lxml_string(soup, "t4")
                now = lxml_string(soup, "t6")
                will = lxml_string(soup, "t7")
                cham = lxml_string(soup, "other")

                embed=discord.Embed(title="🌥 기상특보", description="현재 기준 기상특보를 불러왔어요.",color=0x62bf42)
                
                embed.add_field(name="현재 특보 제목", value=title)
                embed.add_field(name="발효 지역", value=area)
                embed.add_field(name="내용", value=content)
                embed.add_field(name="특보 현황 내용", value=now)


                embed.add_field(name="예비특보", value=will)
                embed.set_footer(text="기상청")

                await ctx.send(embed=embed)
    
    @commands.command(name="뽑기", aliases=["추첨"])
    async def choose_user(self, ctx):
        # embed=discord.Embed(title="🔄 유저 불러오는 중", description="서버의 모든 유저를 불러오는 중이에요...",color=0x1dc73a )
        # await ctx.send(embed=embed, delete_after=1)
        
        embed=discord.Embed(title="✅ 뽑기 성공", description="{}님이 뽑혔어요!".format(random.choice(ctx.guild.members).mention ) ,color=0x1dc73a )
        await ctx.send(embed=embed)

    @commands.command(name="미세먼지", aliases=["초미세먼지"], rest_is_raw=True)
    async def fine_dust(self, ctx, *, args):

        async with aiohttp.ClientSession() as session:
            async with session.get('http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureLIst?serviceKey=' + TOKEN.misae +  '&numOfRows=1&pageSize=1&pageNo=1&startPage=1&itemCode=PM10&dataGubun=HOUR') as r:
                c = await r.text()
                
                soup = BeautifulSoup(c,"lxml-xml")
                misae_datatime = lxml_string(soup, "dataTime")
                seoul = lxml_string(soup, "seoul")
                busan = lxml_string(soup, "busan")
                daegu = lxml_string(soup, "daegu")
                incheon = lxml_string(soup, "incheon")
                gwangju = lxml_string(soup, "gwangju")
                daejon = lxml_string(soup, "daejeon")
                ulsan = lxml_string(soup, "ulsan")
                gyeonggi = lxml_string(soup, "gyeonggi")
                gangwon = lxml_string(soup, "gangwon")
                chungbuk = lxml_string(soup, "chungbuk")
                chungnam = lxml_string(soup, "chungnam")
                jeonbuk = lxml_string(soup, "jeonbuk")
                jeonnam = lxml_string(soup, "jeonnam")
                gyeongbuk = lxml_string(soup, "gyeongbuk")
                gyeongnam = lxml_string(soup, "gyeongnam")
                jeju = lxml_string(soup, "jeju")
                sejong = lxml_string(soup, "sejong")
                misae_sido = {"서울" : seoul, "부산" : busan, "대구":daegu, "인천":incheon, "광주":gwangju, "대전":daejon, "울산":ulsan, "경기":gyeonggi, "강원": gangwon, "충북": chungbuk, "충남":chungnam, "전북":jeonbuk, "전남" : jeonnam, "경북" : gyeongbuk, "경남" : gyeongnam, "제주":jeju, "세종": sejong}
                
        async with aiohttp.ClientSession() as session:
            async with session.get('http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureLIst?serviceKey=' + TOKEN.misae + '&numOfRows=1&pageSize=1&pageNo=1&startPage=1&itemCode=PM25&dataGubun=HOUR') as r:
                c = await r.text()
                
                soup = BeautifulSoup(c,"lxml-xml")
                chomisae_datatime = lxml_string(soup, "dataTime")
                seoul = lxml_string(soup, "seoul")
                busan = lxml_string(soup, "busan")
                daegu = lxml_string(soup, "daegu")
                incheon = lxml_string(soup, "incheon")
                gwangju = lxml_string(soup, "gwangju")
                daejon = lxml_string(soup, "daejeon")
                ulsan = lxml_string(soup, "ulsan")
                gyeonggi = lxml_string(soup, "gyeonggi")
                gangwon = lxml_string(soup, "gangwon")
                chungbuk = lxml_string(soup, "chungbuk")
                chungnam = lxml_string(soup, "chungnam")
                jeonbuk = lxml_string(soup, "jeonbuk")
                jeonnam = lxml_string(soup, "jeonnam")
                gyeongbuk = lxml_string(soup, "gyeongbuk")
                gyeongnam = lxml_string(soup, "gyeongnam")
                jeju = lxml_string(soup, "jeju")
                sejong = lxml_string(soup, "sejong")
                chomisae_sido = {"서울" : seoul, "부산" : busan, "대구":daegu, "인천":incheon, "광주":gwangju, "대전":daejon, "울산":ulsan, "경기":gyeonggi, "강원": gangwon, "충북": chungbuk, "충남":chungnam, "전북":jeonbuk, "전남" : jeonnam, "경북" : gyeongbuk, "경남" : gyeongnam, "제주":jeju, "세종": sejong}
                
                
                

                embed=discord.Embed(title="💨 PM10 미세먼지 / PM2.5 초미세먼지 농도", description="<미세먼지 농도>\n<초미세먼지 농도>  로 나타나요.", color=0x1dc73a )
                embed.set_footer(text="에어코리아 / {} 기준".format(misae_datatime))
                name = args.lstrip()
                if name == "":
                    for i in misae_sido.keys():
                        embed.add_field(name=i, value="{}㎍/m³ |  {}\n{}㎍/m³ |  {}" .format(misae_sido[i], checkpm10(misae_sido[i]), chomisae_sido[i], checkpm25(chomisae_sido[i]) ), inline=True)
                    await ctx.send(embed=embed)
                else:
                    if name in misae_sido.keys():
                        embed.add_field(name=name, value="{}㎍/m³ |  {}\n{}㎍/m³ |  {}" .format(misae_sido[name], checkpm10(misae_sido[name]), chomisae_sido[name], checkpm25(chomisae_sido[name]) ), inline=True)
                        await ctx.send(embed=embed)
                    else:
                        embed=discord.Embed(title="⚠ 주의", description="지역 이름이 없어요. 시·도별기준으로 불러오며, 도는 줄인 이름으로, 광역시는 `광역시` 글자를 제거해주세요.\n\n```ex) 경북, 경기, 서울, 광주...```",color=0xd8ef56)
                        await ctx.send(embed=embed)


    @commands.command(name="프사",aliases=["프로필", "프로필사진"], rest_is_raw=True)
    async def profile_emoji(self, ctx, *, args):
        try:
            memberid = args.lstrip()
            memberid = memberid.replace("<@", "")
            memberid = memberid.replace("!", "")
            memberid = memberid.replace(">", "")
            if memberid == "":
                memberid = ctx.author.id
                member = self.bot.get_user(memberid)
                a = member.avatar_url
                if a == "":
                    a = member.default_avatar_url
                embed=discord.Embed(title="🖼️ 프로필 사진", description="",color=0x62bf42)

                embed.set_image(url=a)
                await ctx.send(embed=embed)
                
            else:
                memberid = int(memberid)

                member = self.bot.get_user(memberid)
                a = member.avatar_url
                if a == "":
                    a = member.default_avatar_url
                embed=discord.Embed(title="🖼️ 프로필 사진", description="",color=0x62bf42)

                embed.set_image(url=a)
                await ctx.send(embed=embed)

        except:
            embed=discord.Embed(title="❌ 오류", description="오류가 발생했어요.",color=0xff0909)
            await ctx.send(embed=embed)


    @commands.command(name="가사검색", rest_is_raw=True)
    async def search_lyrics(self, ctx, *, args):
        try:
            a = args.lstrip()
            if a == "":
                embed=discord.Embed(title="⚠ 주의", description="검색어가 없어요!",color=0xd8ef56)
                await ctx.send(embed=embed)
            else:     
                async with aiohttp.ClientSession() as session:
                    async with session.get("http://music.naver.com/search/search.nhn?query=" + a + "&target=track") as r:

                        c = await r.text()
                        soup = BeautifulSoup(c,"html.parser")
                        f = soup.find_all("a",{"title":"가사"})[0]['class'][1]
                        f = f.split(",")
                        # print(f)
                        f = f[2]
                        f = f[2:]
                        load = "http://music.naver.com/lyric/index.nhn?trackId=" + f
                async with aiohttp.ClientSession() as session:
                    async with session.get(load) as r:
                        c = await r.text()
                        soup = BeautifulSoup(c,"html.parser")
                        f = soup.find("div",{"id":"lyricText"})
                        f = f.get_text(separator="\n")
                        title = soup.find("span",{"class":"ico_play"}).get_text()
                        f = f[:100]
                        embed=discord.Embed(title="🎵 " + title + "의 가사", description="\n" + f +"...", color=0x237ccd)
                        embed.add_field(name="자세히 보기", value=load, inline=False)
                        embed.set_footer(text="네이버 뮤직")
                        await ctx.send(embed=embed)

        except Exception as error:
            embed=discord.Embed(title="❌ 오류", description="오류가 발생했어요.\n%s" %(error),color=0xff0909)
            await ctx.channel.send(embed=embed)


    @commands.command(name="한강")
    async def han_river(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("http://hangang.dkserver.wo.tc/") as r:

                ondo = await r.text()
                ondo = json.loads(ondo)
                if ondo['result'] == "true":
                    temp = ondo['temp']
                    h = ondo['time']
                    embed=discord.Embed(title="🌡 한강 현재수온", description= temp + "°C\n",color=0x62bf42)
                    embed.add_field(name="🕐 기준시각", value=h, inline=True)
                    embed.set_footer(text="퐁당!")
                    await ctx.send(embed=embed)
                else:
                    embed=discord.Embed(title="❌ 오류 발생", description="API에서 정보를 제공하지 않습니다.",color=0xff0909)
                    await ctx.send(embed=embed)

    @commands.command(name="영어한글번역", aliases=["영한번역", "en ko"], rest_is_raw=True)
    async def en_to_ko(self, ctx, * , args):
        a = args.lstrip()
        trans = await nmt("en", "ko", a)
        if trans is None:
            embed=discord.Embed(title="❌ 오류 발생", description="번역에 오류가 발생하였어요.",color=0xff0909)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="✅ 한글 번역", description=trans,color=0x1dc73a )
            await ctx.send(embed=embed)

    @commands.command(name="한글영어번역", aliases=["한영번역", "ko en"], rest_is_raw=True)
    async def ko_to_en(self, ctx, *, args):
        a = args.lstrip()
        trans = await nmt("ko", "en", a)
        if trans is None:
            embed=discord.Embed(title="❌ 오류 발생", description="번역에 오류가 발생하였어요.",color=0xff0909)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="✅ 영어 번역", description=trans,color=0x1dc73a )
            await ctx.send(embed=embed)

    @commands.command(name="자동번역", aliases=["번역"], rest_is_raw=True)
    async def auto_translate(self, ctx , *, args):
        a = args.lstrip()
        headers = {"X-Naver-Client-Id" : TOKEN.papago_detect_id, "X-Naver-Client-Secret" : TOKEN.papago_detect_secret}
        data = {"query":a}
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.post("https://openapi.naver.com/v1/papago/detectLangs", data=data) as r:
                        if r.status == 200:
                            c = await r.json()
                            langcode = c["langCode"]
                            langcode = langcode.replace("zh-cn","zh-CN")           
                            langcode = langcode.replace("zh-tw","zh-TW")           

                            if langcode == "ko":
                                embed=discord.Embed(title="⚠ 주의", description="언어가 한국어로 감지되었어요. 한국어가 많이 섞여있다면 한국어를 삭제해보시고 다시 시도해주세요." ,color=0xd8ef56)
                                await ctx.send(embed=embed)



                            else:
                                trans = await nmt(langcode, "ko", a)
                                if trans is None:
                                    embed=discord.Embed(title="❌ 오류 발생", description="번역에 오류가 발생하였어요.",color=0xff0909)
                                    await ctx.send(embed=embed)
                                else:
                                    embed=discord.Embed(title="✅ 자동 번역", description=trans,color=0x1dc73a )
                                    embed.set_footer(text=langcode + " >> ko")
                                    await ctx.send(embed=embed)

                        else:
                            embed=discord.Embed(title="❌ 오류 발생", description="번역에 오류가 발생하였어요.",color=0xff0909)
                            await ctx.send(embed=embed)
        except:
            embed=discord.Embed(title="❌ 오류 발생", description="언어 감지에 오류가 발생하였어요.",color=0xff0909)
            await ctx.send(embed=embed)


    @commands.command(name="백과사전", aliases=["사전"], rest_is_raw=True)
    async def diction(self, ctx, *, args):
        try:
            a = args.lstrip()
            if a == "":
                embed=discord.Embed(title="⚠ 주의", description="검색어가 없어요! `봇 백과사전 <검색어>` 로 사용해주세요.",color=0xd8ef56)
                await ctx.send(embed=embed)
            else:

                headers = {"X-Naver-Client-Id" : TOKEN.search_id, "X-Naver-Client-Secret" : TOKEN.search_secret}
                async with aiohttp.ClientSession(headers=headers) as session:
                    async with session.get("https://openapi.naver.com/v1/search/encyc.json?query=" + a) as r:
                        c = await r.text()
                        c = json.loads(c)
                        a = c['items'][0]     
                        
                        title = a['title']
                        title = htmltotext(title)
                        link = a['link']
                        thumbnail = a['thumbnail']
                        description = a['description']
                        description = htmltotext(description)
                        embed=discord.Embed(title="🔖 백과사전", description="**" + title+ "**에 대한 검색결과에요.", color=0x237ccd)
                        embed.add_field(name="내용", value=description, inline=False)
                        embed.add_field(name="자세히 읽기", value=link, inline=False)
                        embed.set_image(url=thumbnail)

                        await ctx.send(embed=embed)

        except:
            embed=discord.Embed(title="❌ 오류 발생", description="해당 검색어에 대한 내용을 찾을 수 없어요.",color=0xff0909)
            await ctx.send(embed=embed)

    @commands.command(name="링크축약", aliases=["링크단축", "url축약", "url단축"], rest_is_raw=True)
    async def short_url(self, ctx, *, args):
        if args.lstrip() == "":
            embed=discord.Embed(title="⚠ 주의", description="축약할 링크가 오지 않았어요. `봇 링크축약 <ulr주소>`로 진행해주세요.",color=0xd8ef56)
            await ctx.send(embed=embed)
            return
        link = args.lstrip()
        headers = {"X-Naver-Client-Id" : TOKEN.url_id, "X-Naver-Client-Secret" : TOKEN.url_secret}
        data = {"url":link}
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.post("https://openapi.naver.com/v1/util/shorturl", data=data) as r:
                        if r.status == 200:
                            c = await r.json()
                            url = c["result"]["url"]
                            embed=discord.Embed(title="✅ 링크 축약", description="링크 축약을 성공하였어요.",color=0x1dc73a )
                            embed.add_field(name="처음 URL", value=link)
                            embed.add_field(name="단축된 URL", value=url)
                            await ctx.send(embed=embed)
                        else:
                            embed=discord.Embed(title="❌ 오류 발생", description="정상적인 값이 출력되지 않았습니다. 나중에 다시 시도해주세요.\nHTTP CODE : %s" %(r.status),color=0xff0909)
                            await ctx.send(embed=embed)

        except:
            embed=discord.Embed(title="❌ 오류 발생", description="단축에 오류가 발생하였어요.",color=0xff0909)
            await ctx.send(embed=embed)

    @commands.command(name="나무위키", aliases=["꺼무위키"], rest_is_raw=True)
    async def namu_wiki(self, ctx, *, args):
        a = args.lstrip()
        title = a
        a = "http://namu.wiki/w/" + a.replace(" ","%20")
        async with aiohttp.ClientSession() as session:
            async with session.get(a) as r:
                if r.status == 404:
                    embed=discord.Embed(title="", description="없는 문서에요.", color=0x1dc73a)
                    embed.set_author(name="문서를 찾을 수 없어요.", icon_url="https://i.imgur.com/FLN2B5H.png")
                    await ctx.send(embed=embed)
                else:
                    data = await r.text()
                    soup = BeautifulSoup(data,"html.parser")
                    d = soup.find("div", {"class":"wiki-inner-content"}).get_text()
                    content = htmltotext(d)[:150]
                    embed=discord.Embed(title="", description=content+"...", color=0x1dc73a)
                    embed.add_field(name="바로가기", value="[여기](%s)를 클릭하세요. " %(a))
                    embed.set_author(name=title, icon_url="https://i.imgur.com/FLN2B5H.png")
                    await ctx.send(embed=embed)

    @commands.command(name="고양이", aliases=["냥이", "냥냥이", "냐"])
    async def get_cat(self, ctx):
        while True:
            async with aiohttp.ClientSession() as session:
                async with session.get("http://aws.random.cat/meow") as r:
                    try:
                        data = await r.text()
                        data = json.loads(data)
                        break
                    except:
                        pass
        file = data["file"]
        embed=discord.Embed(title=" ",color=0xf2e820)
        embed.set_image(url=file)
        embed.set_footer(text="http://random.cat")
        await ctx.send(embed=embed)


    @commands.command(name="강아지", aliases=["멍멍이", "댕댕이", "개", "멍"])
    async def get_dog(self, ctx):
        async with aiohttp.ClientSession() as session:
                async with session.get("http://random.dog/woof.json") as r:
                    data = await r.json()
        file = data["url"]
        embed=discord.Embed(title=" ",color=0xf2e820)
        embed.set_image(url=file)
        embed.set_footer(text="http://random.dog")
        await ctx.send(embed=embed)
    
    @commands.command(name="서버정보", aliases=["이 서버는?", "이 서버", "서버"])
    async def server_info(self, ctx):
        number = 0
        date = "%s (UTC)"% ctx.guild.created_at
        for i in ctx.guild.members:
            number = number + 1
        sunsunumber = 0
        for i in ctx.guild.members:
            if i.bot == False:
                sunsunumber = sunsunumber + 1
        try:
            welcome = ctx.guild.system_channel.name
            if welcome == "" or welcome is None:
                welcome = "존재하지 않아요."
        except:
            welcome = "존재하지 않아요."
            
        embed=discord.Embed(title="ℹ️ 서버 정보", description="이 서버에 대한 정보를 불러왔어요.\n\n" , color=0x1dc73a)
        embed.add_field(name="이름", value=ctx.guild.name, inline=False)
        embed.add_field(name="서버 ID", value=ctx.guild.id, inline=True)
        embed.add_field(name="서버 인원", value=number, inline=True)
        embed.add_field(name="순수 서버 인원 (봇 제외)", value=sunsunumber, inline=False)

        embed.add_field(name="서버 생성일", value=date, inline=True)
        embed.add_field(name="서버 오너", value=ctx.guild.owner, inline=False)
        embed.add_field(name="웰컴 채널", value="#" + welcome, inline=False)
        embed.add_field(name="서버 위치", value=ctx.guild.region, inline=True)

        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)


    @commands.command(name="유저정보", rest_is_raw=True)
    async def user_info(self, ctx, *, args):
        a = args.lstrip()       
        if a == "":
            a = ctx.author.id
        try:
            a = a.replace("<", "")
            a = a.replace("@", "")
            a = a.replace("!", "")
            a = a.replace(">", "") 
            a = int(a)
        except:
            pass
        date = "%s (UTC)"% ctx.guild.get_member(a).created_at
        try:
            game = ctx.guild.get_member(a).activity.name
        except:
            game = "플레이 중인 게임이 없습니다."
        if game is None:
            game = "플레이 중인 게임이 없습니다."
        member =ctx.guild.get_member(a)
        status = ctx.guild.get_member(a).status
        joined = str(ctx.guild.get_member(a).joined_at)
        if status == discord.Status.online:
            status = "온라인"
        elif status == discord.Status.idle:
            status = "자리비움"
        elif status == discord.Status.dnd:
            status = "다른 용무 중"
        elif status == discord.Status.offline:
            status = "오프라인"
        else:
            status = "알 수 없음."

        asdf = member.avatar_url
        if asdf == "":
            asdf = member.default_avatar_url

        embed=discord.Embed(title="ℹ️ 유저 정보", description="선택하신 유저에 대한 정보를 불러왔습니다.\n\n" , color=0x1dc73a)
        embed.add_field(name="이름", value=ctx.guild.get_member(a).name, inline=False)
        embed.add_field(name="유저 ID", value=ctx.guild.get_member(a).id, inline=True)
        embed.add_field(name="계정 생성일", value=date, inline=True)
        embed.add_field(name="서버 가입일", value=joined + " (UTC)", inline=False)
        
        embed.add_field(name="플레이 중", value=game, inline=True)
        embed.add_field(name="상태", value=status, inline=False)

        embed.set_thumbnail(url=asdf)
        await ctx.send(embed=embed)

    @commands.command(name="질문")
    async def question(self, ctx):
        response = ['아니요?','아뇨?','어...음...네','흐음...아뇨?','모르겠어요','네','맞아요','흐음...몰라요']
        a = random.choice(response)
        await ctx.send(a)


    @commands.command(name="확률", rest_is_raw=True)
    async def percent(self, ctx, *, args):
        a = args.lstrip()
        per = random.randint(0,100)
        await ctx.send("`%s` 은 `%s%%`입니다." %(a, per))

    @commands.command(name="날씨", rest_is_raw=True)
    async def weather(self, ctx, *, args):
        city = args.lstrip()
        if city == "":
            embed=discord.Embed(title="⚠ 주의", description="도시가 정의되지 않았어요.",color=0xd8ef56)
            await ctx.send(embed=embed)

        else:
            async with aiohttp.ClientSession() as session:
                async with session.get("http://api.openweathermap.org/data/2.5/weather?q=" + city + "&APPID=" + TOKEN.weather + "&units=metric") as r:
                        if r.status == 200:
                            c = await r.json()
                            embed=discord.Embed(title="⛅ %s 날씨" %(c["name"]), description="%s (구름 %s%%)" %(c["weather"][0]["main"], c["clouds"]["all"]) ,color=0x1dc73a )
                            embed.add_field(name="온도", value="%s °C" %(c["main"]["temp"]) )
                            embed.add_field(name="바람", value="%sm/s (%s°)" %(c["wind"]["speed"], c["wind"]["deg"]), inline=False)
                            embed.add_field(name="기타", value="기압 : %shPa\n습도 : %s%%" %(c["main"]["pressure"], c["main"]["humidity"]))
                            embed.set_thumbnail(url="http://openweathermap.org/img/w/%s.png" %(c["weather"][0]["icon"]))
                            embed.set_footer(text="OpenWeatherMap.org")
                            await ctx.send(embed=embed)
                        elif r.status == 404:
                            embed=discord.Embed(title="⚠ 주의", description="선택하신 도시를 찾지 못했어요. 다음을 시도해보세요:\n\n1. 지역명 뒤에 시, 광역시 붙이기 (`봇 날씨 부산광역시`)\n2. 주변에 있는 주요 도시로 재시도\n3. 영어로 해보기 (`봇 날씨 tokyo`)"
                            ,color=0xd8ef56)
                            await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Chatting(bot))
