import discord
from discord.ext import commands
import os
import re
from bs4 import BeautifulSoup
import lxml
import datetime
import typing
import aiohttp
import random
import asyncio
import json
import TOKEN
from utils.embed import Embed
from EZPaginator import Paginator
from logs import Logs
import aiomysql
import PW


def htmltotext(html):
    soup = BeautifulSoup(html)
    text_parts = soup.findAll(text=True)
    return "".join(text_parts)


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
    headers = {
        "X-Naver-Client-Id": TOKEN.papago_nmt_id,
        "X-Naver-Client-Secret": TOKEN.papago_nmt_secret,
    }
    data = {"source": source, "target": target, "text": string}
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(
                "https://openapi.naver.com/v1/papago/n2mt", data=data
            ) as r:
                if r.status == 200:
                    c = await r.json()
                    translated = c["message"]["result"]["translatedText"]
                    return translated
                else:
                    return None
    except:
        return None


async def smt(source, target, string):
    headers = {
        "X-Naver-Client-Id": TOKEN.papago_smt_id,
        "X-Naver-Client-Secret": TOKEN.papago_smt_secret,
    }
    data = {"source": source, "target": target, "text": string}
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(
                "https://openapi.naver.com/v1/language/translate", data=data
            ) as r:
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
        self.logger = Logs.create_logger(self)
        self.conn_pool = ""

        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.set_db())

        with open("help.json", "r", encoding="utf-8") as f:
            self.help_data = json.load(f)

    async def set_db(self):
        self.conn_pool = await aiomysql.create_pool(
            host="127.0.0.1",
            user=PW.db_user,
            password=PW.db_pw,
            db="bot",
            autocommit=True,
            loop=self.loop,
            minsize=2,
            maxsize=3,
            charset="utf8mb4",
        )

    async def get_insignia(self, id):
        try:
            async with self.conn_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        """SELECT * FROM insignia where id=%s""", (str(id))
                    )
                    row = await cur.fetchone()

            if row is None:
                return None
            return row[1]

        except:
            return False

    @commands.command(
        name="안녕",
        aliases=[
            "ㅎㅇ",
            "gdgd",
            "gd",
            "안냥",
            "안녕하세요",
            "hello",
            "안뇽",
            "안뇨옹",
            "잘가",
            "byebye",
        ],
    )
    async def hello(self, ctx):
        bot_profile = self.bot.user.avatar_url
        embed = discord.Embed(
            title="👋 안녕하세요!",
            description="**봇을 사용해 주셔서 고마워요!**\n봇 / BOT은 BGM#0970이 개발중인 디스코드 봇이에요.\n\n자세한 내용은 `봇 도움` 명령어를 사용해서 볼 수 있어요.",
            color=0x237CCD,
        )
        embed.set_thumbnail(url=bot_profile)
        await ctx.send(embed=embed)

    @commands.command(name="라타어", rest_is_raw=True, aliases=["절리어"])
    async def jolly(self, ctx, *, args):
        args = args.lstrip()
        database = [
            "절",
            "절절",
            "리",
            "가루",
            "브금",
            " ",
            "동묘",
            "와이",
            "라마",
            "나무",
            "절절" "형",
            "pb",
            "ㅎㅌ",
            "순수",
            "순순",
            "순",
            "y",
            "",
            "띵큐",
            "잠수",
            "잠수",
            "나무",
            "루비",
            "루",
            "라미",
            "폭",
            "라타",
            "호준",
        ]

        target_list = list(args)
        translated_list = [
            sum([int(j) for j in str(ord(x))]) for x in target_list
        ]
        new = [
            database[x]
            if x < len(database) - 1
            else database[(x % len(database))]
            for x in translated_list
        ]
        embed = Embed.check(title="라타어 번역", description="".join(new))
        await ctx.send(embed=embed)

    @commands.command(
        name="코로나",
        ailases=["코로나바이러스", "우한", "우한폐렴", "우한", "신종코로나", "신종코로나바이러스", "코로나19"],
    )
    async def ncov2019(self, ctx):
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(
                "http://ncov.mohw.go.kr/index_main.jsp"
            ) as r:
                soup = BeautifulSoup(await r.text(), "html.parser")
                boardList = soup.select("ul.liveNum > li > span")
                newstNews = soup.select(".m_news > ul > li > a")[0]
            # async with session.get(
            #     "http://ncov.mohw.go.kr/static/js/co_main_chart.js"
            # ) as r:
            #     r = await r.text()
            #     rg = re.compile("/static/image/main_chart/week_\d*.png")
            #     pic = rg.search(r).group()

        boardList = [x.text for x in boardList]
        embed = discord.Embed(
            title="🦠 코로나바이러스감염증-19 국내 현황",
            description="[예방수칙](http://www.cdc.go.kr/gallery.es?mid=a20503020000&bid=0003)",
            color=0xD8EF56,
        )
        embed.add_field(name="확진환자", value="\n".join(boardList[0:2]))
        embed.add_field(name="완치", value=" ".join(boardList[2:4]))
        embed.add_field(name="사망", value=" ".join(boardList[6:8]), inline=True)

        embed.add_field(
            name="질병관리본부 최신 브리핑",
            value="[{}](http://ncov.mohw.go.kr{})".format(
                newstNews.text, newstNews.get("href")
            ),
            inline=False,
        )
        embed.set_footer(text="질병관리본부")
        # embed.set_image(url="http://ncov.mohw.go.kr/" + pic)
        await ctx.send(embed=embed)

    @commands.command(name="유라마드", aliases=["lama", "라마"])
    async def you_lamaed(self, ctx):
        try:
            headers = {
                "X-Naver-Client-Id": TOKEN.search_id,
                "X-Naver-Client-Secret": TOKEN.search_secret,
            }
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(
                    "https://openapi.naver.com/v1/search/image?query={}&display=20".format(
                        "llama"
                    )
                ) as r:
                    c = await r.text()
                    c = json.loads(c)
                embed = discord.Embed(
                    title="🦙", description="**YOU LLAMAED**", color=0xFF0909
                )
                embed.set_image(url=random.choice(c["items"])["link"])

                await ctx.send(embed=embed)
        except:
            embed = Embed.error("오류 발생", "해당 검색어에 대한 내용을 찾을 수 없어요.",)
            await ctx.send(embed=embed)

    @commands.command(name="따라해", rest_is_raw=True)
    async def repeat(self, ctx, *, args):
        if args == "":
            embed = Embed.warn(
                title="주의", description="봇 따라해 `할말`로 입력해주세요!\n아무 값도 받지 못했어요.",
            )
            await ctx.channel.send(embed=embed)
            return

        if "@everyone" in args or "@here" in args:
            embed = Embed.error(
                title="경고",
                description="`@everyone`이나 `@here`은 다른 사용자에게 피해를 줄 수 있어요.\n사용을 제한할께요!",
            )
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
            embed = Embed.warn(
                title="주의", description="봇 거꾸로 `할말`로 입력해주세요!\n아무 값도 받지 못했어요.",
            )
            await ctx.channel.send(embed=embed)
            return

        args = "".join(reversed(args))
        if "@everyone" in args or "@here" in args:
            embed = Embed.error(
                title="경고",
                description="`@everyone`이나 `@here`은 다른 사용자에게 피해를 줄 수 있어요.\n사용을 제한할께요!",
            )
            embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed=embed)
        else:
            try:
                await ctx.delete()
            except:
                pass
            await ctx.channel.send(args)

    @commands.command(name="샤드")
    @commands.guild_only()
    async def guild_shard(self, ctx):
        embed = discord.Embed(
            title="🖥 샤드",
            description="현재 이 서버는 샤드 {}번에 있어요!".format(ctx.guild.shard_id),
            color=0x237CCD,
        )
        await ctx.send(embed=embed)

    @commands.command(name="도움", aliases=["도움말", "어떻게써", "help"])
    async def help(self, ctx):

        functions_list = ["기본", "기본2", "게임", "커스텀 명령어", "관리자"]
        embeds = []
        for i in functions_list:
            embed = discord.Embed(
                title="📰 도움말",
                description="**{} 커맨드** ({} / {})".format(
                    i, functions_list.index(i) + 1, len(functions_list),
                ),
                color=0x237CCD,
            )
            embed.set_footer(text="이모지를 이용하여 페이지를 넘기세요.")
            for k in self.help_data[i]:
                for j in k.items():
                    embed.add_field(name=j[0], value=j[1], inline=False)
            embeds.append(embed)

        msg = await ctx.send(embed=embeds[0])
        page = Paginator(self.bot, msg, embeds=embeds)
        await page.start()

    @commands.command(name="초대", aliases=["초대링크", "초대 링크"])
    async def invite(self, ctx):
        embed = discord.Embed(
            title="❔ 봇 초대",
            description="저를 초대하고 싶으신가요?\n[여기](https://discordapp.com/oauth2/authorize?client_id=351733476141170688&scope=bot&permissions=268463166)를 클릭해주세요!",
            color=0x1DC73A,
        )
        await ctx.send(embed=embed)

    @commands.command(name="시간계산", aliases=["시간 계산"], rest_is_raw=True)
    async def time_calc(self, ctx, args):
        try:
            answer = datetime.datetime.strptime(args, "%Y-%m-%d")
            now = datetimee.datetime.now()
            dap = answer - now

            days = dap.days
            hours, remainder = divmod(dap.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            seconds += dap.microseconds / 1e6
            embed = discord.Embed(
                title="⏲ 시간 계산",
                description=str(days)
                + "일 "
                + str(hours)
                + "시간 "
                + str(minutes)
                + "분 "
                + str(int(round(seconds, 0)))
                + "초 남았어요.",
                color=0x237CCD,
            )
            await ctx.send(embed=embed)
        except:
            embed = Embed.error("오류 발생", "`yyyy-mm-dd` 형식으로 입력하셨는지 확인해주세요.")
            await ctx.send(embed=embed)

    @commands.command(name="핑", aliases=["퐁"])
    async def ping(self, ctx):
        ping = str(int(self.bot.latency * 1000))
        embed = discord.Embed(
            title="🏓 퐁! " + ping + "ms",
            description="Discord WebSocket 프로토콜의 레이턴시에요!",
            color=0x237CCD,
        )
        await ctx.send(embed=embed)

    @commands.command(name="잠수", aliasees=["afk"])
    async def afk_define(self, ctx, *, reason="사유가 없어요."):
        reason = reason.strip()
        try:
            author_color = ctx.author.colour
        except:
            author_color = 0x237CCD
        afk_start_time = datetime.datetime.now()
        afk_start_utc_time = datetime.datetime.utcnow()
        # self.afk[ctx.author.id] = {
        #     "reason": reason,
        #     "starttime": afk_start_time,
        #     "utcstarttime": afk_start_utc_time,
        #     "color": author_color,
        # }
        embed = discord.Embed(
            title="💤 잠수",
            description="<@{0}>님이 잠수를 시전하셨습니다.\n".format(ctx.author.id),
            color=author_color,
        )
        embed.add_field(name="잠수 사유", value="{0}".format(reason), inline=False)
        embed.set_footer(text="{0}\n".format(afk_start_time))
        await ctx.send(embed=embed)

    @commands.command(name="문의", aliases=["건의", "기능건의", "기능문의"])
    async def qna(self, ctx, *, args):

        msg = await ctx.send(
            "정말로 전송할까요? 의미 없는 내용을 전송하시면 **블랙추가** 됨을 확인해주세요.\n전송을 원하시면 ✅ 를 눌러주세요."
        )
        await msg.add_reaction("✅")

        def posi_check(reaction, user):
            # if user.is_bot: return False
            return (
                user == ctx.author
                and str(reaction.emoji) == "✅"
                and msg.id == reaction.message.id
            )

        answer = await self.bot.wait_for(
            "reaction_add", check=posi_check, timeout=10
        )
        bgm = self.bot.get_user(289729741387202560)
        embed = discord.Embed(
            title="❔ 건의가 도착했어요!",
            description=args,
            color=0x1DC73A,
            timestamp=datetime.datetime.utcnow(),
        )
        embed.set_footer(
            icon_url=ctx.author.avatar_url,
            text="{} / {}".format(ctx.author, ctx.author.id),
        )
        await bgm.send(embed=embed)
        embed = Embed.check(title="성공", description="건의 전송을 성공했어요!")
        await ctx.send(embed=embed)

    @commands.command(name="리마인더", aliases=["알려줘"])
    async def reminder(self, ctx, seconds: typing.Union[int], *, reason=None):

        if not seconds >= 0:
            raise commands.BadArgument()

        if reason is not None:
            embed = Embed.check(
                title="리마인더",
                description="리마인더에 기록 완료했어요! %s초 있다가 `%s`하라고 알려드릴께요!"
                % (str(seconds), reason),
            )
        else:
            embed = Embed.check(
                title="리마인더",
                description="리마인더에 기록 완료했어요! %s초 있다가 알려드릴께요!" % (str(seconds)),
            )

        embed.set_footer(text="봇이 꺼지면 초기화됩니다!")
        await ctx.send(embed=embed)
        await asyncio.sleep(seconds)
        await ctx.send(ctx.author.mention)
        embed = discord.Embed(
            title="⏰ 알림", description="시간이 다 되었어요!", color=0x1DC73A
        )
        if reason is not None:
            embed.add_field(name="내용", value=reason)
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
            async with session.get(
                "https://m.kma.go.kr/m/eqk/eqk.jsp?type=korea"
            ) as r:

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
                    title="지진 정보", description=date, color=0x62BF42
                )
                try:
                    img = soup.find("div", {"class": "img-center"}).find("img")[
                        "src"
                    ]
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

    @commands.command(name="골라", aliases=["선택", "골라줘", "선택해줘"])
    async def choice(self, ctx, *, args):
        content = args.strip()

        if "@everyone" in content or "@here" in content:
            embed = discord.Embed(
                title="⚠ 경고",
                description="`@everyone`이나 `@here`은 다른 사용자에게 피해를 줄 수 있어요.\n사용을 제한할께요!",
                color=0xFF0909,
            )
            embed.set_footer(text=ctx.author)
            await ctx.send(embed=embed)
        else:

            a = content.split(",")
            if content.count("​") != 0:
                a = a[content.count("​") - 1]
                jujak = True
            else:
                a = random.choice(a)
                jujak = False

            embed = discord.Embed(
                title="❔ 봇의 선택", description=a, color=0x1DC73A
            )
            if jujak:
                embed.set_footer(text="이 선택은 조작되었습니다.")
            await ctx.send(embed=embed)

    @commands.command(name="전역일")
    async def outoutout(self, ctx):
        now = datetime.datetime.now()
        jun = datetime.datetime(2020, 12, 16)

        dap = jun - now
        days = dap.days
        hours, remainder = divmod(dap.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        # 초 (실험)
        seconds += dap.microseconds / 1e6
        embed = discord.Embed(
            title="🎖️ 전역일",
            description=str(days)
            + "일 "
            + str(hours)
            + "시간 "
            + str(minutes)
            + "분 "
            + str(int(round(seconds, 0)))
            + "초 남았어요.",
            color=0x237CCD,
        )
        embed.set_footer(text="`봇 조의` 명령어로 조의를 표하세요.")

        await ctx.send(embed=embed)

    @commands.command(name="뽑기", aliases=["추첨"])
    async def choose_user(self, ctx):

        embed = Embed.check(
            title="뽑기 성공",
            description="{}님이 뽑혔어요!".format(
                random.choice(ctx.guild.members).mention
            ),
        )
        await ctx.send(embed=embed)

    @commands.command(name="미세먼지", aliases=["초미세먼지"], rest_is_raw=True)
    async def fine_dust(self, ctx, *, args):

        async with aiohttp.ClientSession() as session:
            async with session.get(
                "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureLIst?serviceKey="
                + TOKEN.misae
                + "&numOfRows=1&pageSize=1&pageNo=1&startPage=1&itemCode=PM10&dataGubun=HOUR"
            ) as r:
                c = await r.text()

                soup = BeautifulSoup(c, "lxml-xml")
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
                misae_sido = {
                    "서울": seoul,
                    "부산": busan,
                    "대구": daegu,
                    "인천": incheon,
                    "광주": gwangju,
                    "대전": daejon,
                    "울산": ulsan,
                    "경기": gyeonggi,
                    "강원": gangwon,
                    "충북": chungbuk,
                    "충남": chungnam,
                    "전북": jeonbuk,
                    "전남": jeonnam,
                    "경북": gyeongbuk,
                    "경남": gyeongnam,
                    "제주": jeju,
                    "세종": sejong,
                }

        async with aiohttp.ClientSession() as session:
            async with session.get(
                "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureLIst?serviceKey="
                + TOKEN.misae
                + "&numOfRows=1&pageSize=1&pageNo=1&startPage=1&itemCode=PM25&dataGubun=HOUR"
            ) as r:
                c = await r.text()

                soup = BeautifulSoup(c, "lxml-xml")
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
                chomisae_sido = {
                    "서울": seoul,
                    "부산": busan,
                    "대구": daegu,
                    "인천": incheon,
                    "광주": gwangju,
                    "대전": daejon,
                    "울산": ulsan,
                    "경기": gyeonggi,
                    "강원": gangwon,
                    "충북": chungbuk,
                    "충남": chungnam,
                    "전북": jeonbuk,
                    "전남": jeonnam,
                    "경북": gyeongbuk,
                    "경남": gyeongnam,
                    "제주": jeju,
                    "세종": sejong,
                }

                embed = discord.Embed(
                    title="💨 PM10 미세먼지 / PM2.5 초미세먼지 농도",
                    description="<미세먼지 농도>\n<초미세먼지 농도>  로 나타나요.",
                    color=0x1DC73A,
                )
                embed.set_footer(text="에어코리아 / {} 기준".format(misae_datatime))
                name = args.lstrip()
                if name == "":
                    for i in misae_sido.keys():
                        embed.add_field(
                            name=i,
                            value="{}㎍/m³ |  {}\n{}㎍/m³ |  {}".format(
                                misae_sido[i],
                                checkpm10(misae_sido[i]),
                                chomisae_sido[i],
                                checkpm25(chomisae_sido[i]),
                            ),
                            inline=True,
                        )
                    await ctx.send(embed=embed)
                else:
                    if name in misae_sido.keys():
                        embed.add_field(
                            name=name,
                            value="{}㎍/m³ |  {}\n{}㎍/m³ |  {}".format(
                                misae_sido[name],
                                checkpm10(misae_sido[name]),
                                chomisae_sido[name],
                                checkpm25(chomisae_sido[name]),
                            ),
                            inline=True,
                        )
                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            title="⚠ 주의",
                            description="지역 이름이 없어요. 시·도별기준으로 불러오며, 도는 줄인 이름으로, 광역시는 `광역시` 글자를 제거해주세요.\n\n```ex) 경북, 경기, 서울, 광주...```",
                            color=0xD8EF56,
                        )
                        await ctx.send(embed=embed)

    @commands.command(name="프사", aliases=["프로필", "프로필사진"], rest_is_raw=True)
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
                embed = discord.Embed(
                    title="🖼️ 프로필 사진", description="", color=0x62BF42
                )

                embed.set_image(url=a)
                await ctx.send(embed=embed)

            else:
                memberid = int(memberid)

                member = self.bot.get_user(memberid)
                a = member.avatar_url
                if a == "":
                    a = member.default_avatar_url
                embed = discord.Embed(
                    title="🖼️ 프로필 사진", description="", color=0x62BF42
                )

                embed.set_image(url=a)
                await ctx.send(embed=embed)

        except:
            embed = Embed.warn(
                "주의", "`봇 프사 <멘션 or ID>` 로 사용해주세요. 유저를 불러오지 못했어요."
            )
            await ctx.send(embed=embed)

    @commands.command(name="환율")
    async def currencyy(
        self, ctx, origin, target, how: typing.Optional[int] = 1
    ):

        origin = origin.upper()
        target = target.upper()
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://free.currconv.com/api/v7/convert?q={}_{}&compact=ultra&apiKey=6bc5cad1b80bf7f58aa5".format(
                    origin, target
                )
            ) as r:
                data = await r.json()

        if data == {}:
            embed = Embed.error(
                title="오류", description="잘못된 화폐 단위를 입력하였는지 확인해주세요."
            )
            await ctx.send(embed=embed)
        else:
            per = data["{}_{}".format(origin, target)]
            embed = discord.Embed(
                title="💰 {} {}".format(format(how, ","), origin),
                description="= {} {}".format(format(how * per, ","), target),
                color=0x1DC73A,
            )
            await ctx.send(embed=embed)

    @commands.command(name="가사검색")
    async def search_lyrics(self, ctx, *, args):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "http://music.naver.com/search/search.nhn?query="
                + args
                + "&target=track"
            ) as r:

                c = await r.text()
                soup = BeautifulSoup(c, "html.parser")
                f = soup.find_all("a", {"title": "가사"})[0]["class"][1]
                f = f.split(",")
                # print(f)
                f = f[2]
                f = f[2:]
                load = "http://music.naver.com/lyric/index.nhn?trackId=" + f

            async with session.get(load) as r:
                c = await r.text()
                soup = BeautifulSoup(c, "html.parser")
                f = soup.find("div", {"id": "lyricText"})
                f = f.get_text(separator="\n")
                title = soup.find("span", {"class": "ico_play"}).get_text()
                f = f[:100]

        embed = discord.Embed(
            title="🎵 " + title + "의 가사",
            description="\n" + f + "...",
            color=0x237CCD,
        )
        embed.add_field(name="자세히 보기", value=load, inline=False)
        embed.set_footer(text="네이버 뮤직")
        await ctx.send(embed=embed)

    @commands.command(name="한강")
    async def han_river(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("http://hangang.dkserver.wo.tc/") as r:

                ondo = await r.text()
                ondo = json.loads(ondo)
                if ondo["result"] == "true":
                    temp = ondo["temp"]
                    h = ondo["time"]
                    embed = discord.Embed(
                        title="🌡 한강 현재수온",
                        description=temp + "°C\n",
                        color=0x62BF42,
                    )
                    embed.add_field(name="🕐 기준시각", value=h, inline=True)
                    embed.set_footer(text="퐁당!")
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="❌ 오류 발생",
                        description="API에서 정보를 제공하지 않습니다.",
                        color=0xFF0909,
                    )
                    await ctx.send(embed=embed)

    @commands.command(name="영한번역", aliases=["영어한글번역", "en ko"])
    async def en_to_ko(self, ctx, *, args):
        a = args.lstrip()
        trans = await nmt("en", "ko", a)
        if trans is None:
            embed = discord.Embed(
                title="❌ 오류 발생", description="번역에 오류가 발생하였어요.", color=0xFF0909
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="✅ 한글 번역", description=trans, color=0x1DC73A
            )
            await ctx.send(embed=embed)

    @commands.command(name="한영번역", aliases=["한글영어번역", "ko en"])
    async def ko_to_en(self, ctx, *, args):
        a = args.lstrip()
        trans = await nmt("ko", "en", a)
        if trans is None:
            embed = discord.Embed(
                title="❌ 오류 발생", description="번역에 오류가 발생하였어요.", color=0xFF0909
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="✅ 영어 번역", description=trans, color=0x1DC73A
            )
            await ctx.send(embed=embed)

    @commands.command(name="한일번역", aliases=["한글일어번역", "ko ja"])
    async def ko_to_ja(self, ctx, *, args):
        a = args.lstrip()
        trans = await nmt("ko", "ja", a)
        if trans is None:
            embed = discord.Embed(
                title="❌ 오류 발생", description="번역에 오류가 발생하였어요.", color=0xFF0909
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="✅ 일본어 번역", description=trans, color=0x1DC73A
            )
            await ctx.send(embed=embed)

    @commands.command(
        name="일한번역", aliases=["일어한글번역", "ja ko"], rest_is_raw=True
    )
    async def ja_to_ko(self, ctx, *, args):
        a = args.lstrip()
        trans = await nmt("ja", "ko", a)
        if trans is None:
            embed = discord.Embed(
                title="❌ 오류 발생", description="번역에 오류가 발생하였어요.", color=0xFF0909
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="✅ 한글 번역", description=trans, color=0x1DC73A
            )
            await ctx.send(embed=embed)

    @commands.command(name="자동번역", aliases=["번역"])
    async def auto_translate(self, ctx, *, args):
        a = args.lstrip()
        headers = {
            "X-Naver-Client-Id": TOKEN.papago_detect_id,
            "X-Naver-Client-Secret": TOKEN.papago_detect_secret,
        }
        data = {"query": a}
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.post(
                    "https://openapi.naver.com/v1/papago/detectLangs", data=data
                ) as r:
                    if r.status == 200:
                        c = await r.json()
                        langcode = c["langCode"]
                        langcode = langcode.replace("zh-cn", "zh-CN")
                        langcode = langcode.replace("zh-tw", "zh-TW")

                        if langcode == "ko":
                            trans = await nmt("ko", "en", a)

                        else:
                            trans = await nmt(langcode, "ko", a)
                            if trans is None:
                                embed = discord.Embed(
                                    title="❌ 오류 발생",
                                    description="번역에 오류가 발생하였어요.",
                                    color=0xFF0909,
                                )
                                await ctx.send(embed=embed)
                            else:
                                embed = discord.Embed(
                                    title="✅ 자동 번역",
                                    description=trans,
                                    color=0x1DC73A,
                                )
                                await ctx.send(embed=embed)

                    else:
                        embed = discord.Embed(
                            title="❌ 오류 발생",
                            description="번역에 오류가 발생하였어요.",
                            color=0xFF0909,
                        )
                        await ctx.send(embed=embed)
        except:
            embed = discord.Embed(
                title="❌ 오류 발생",
                description="언어 감지에 오류가 발생하였어요.",
                color=0xFF0909,
            )
            await ctx.send(embed=embed)

    @commands.command(name="백과사전", aliases=["사전"])
    async def diction(self, ctx, *, args):
        try:
            a = args.strip()
            headers = {
                "X-Naver-Client-Id": TOKEN.search_id,
                "X-Naver-Client-Secret": TOKEN.search_secret,
            }
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(
                    "https://openapi.naver.com/v1/search/encyc.json?query=" + a
                ) as r:
                    c = await r.text()
                    c = json.loads(c)
                    a = c["items"][0]
                    title = a["title"]
                    title = htmltotext(title)
                    link = a["link"]
                    thumbnail = a["thumbnail"]
                    description = a["description"]
                    description = htmltotext(description)
                    embed = discord.Embed(
                        title="🔖 백과사전",
                        description="**" + title + "**에 대한 검색결과에요.",
                        color=0x237CCD,
                    )
                    embed.add_field(name="내용", value=description, inline=False)
                    embed.add_field(name="자세히 읽기", value=link, inline=False)
                    embed.set_image(url=thumbnail)

                    await ctx.send(embed=embed)

        except:
            embed = discord.Embed(
                title="❌ 오류 발생",
                description="해당 검색어에 대한 내용을 찾을 수 없어요.",
                color=0xFF0909,
            )
            await ctx.send(embed=embed)

    @commands.command(name="나무위키", aliases=["꺼무위키"])
    async def namu_wiki(self, ctx, *, args):
        a = args.lstrip()
        title = a
        a = "http://namu.wiki/w/" + a.replace(" ", "%20")
        async with aiohttp.ClientSession() as session:
            async with session.get(a) as r:
                if r.status == 404:
                    embed = discord.Embed(
                        title="", description="없는 문서에요.", color=0x1DC73A
                    )
                    embed.set_author(
                        name="문서를 찾을 수 없어요.",
                        icon_url="https://i.imgur.com/FLN2B5H.png",
                    )
                    await ctx.send(embed=embed)
                else:
                    data = await r.text()
                    soup = BeautifulSoup(data, "html.parser")
                    d = soup.select(".wiki-heading-content")[0].text
                    content = htmltotext(d)[:150]
                    embed = discord.Embed(
                        title="", description=content + "...", color=0x1DC73A
                    )
                    embed.add_field(
                        name="바로가기", value="[여기](%s)를 클릭하세요. " % (a)
                    )
                    embed.set_author(
                        name=title, icon_url="https://i.imgur.com/FLN2B5H.png"
                    )
                    await ctx.send(embed=embed)

    @commands.command(name="서버정보", aliases=["이 서버는?", "이 서버", "서버"])
    async def server_info(self, ctx):
        number = 0
        date = "%s (UTC)" % ctx.guild.created_at
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

        embed = discord.Embed(
            title="ℹ️ 서버 정보",
            description="이 서버에 대한 정보를 불러왔어요.\n\n",
            color=0x1DC73A,
        )
        embed.add_field(name="이름", value=ctx.guild.name, inline=False)
        embed.add_field(name="서버 ID", value=ctx.guild.id, inline=True)
        embed.add_field(name="서버 인원", value=number, inline=True)
        embed.add_field(name="순수 서버 인원 (봇 제외)", value=sunsunumber, inline=False)

        embed.add_field(name="서버 생성일", value=date, inline=True)
        embed.add_field(name="서버 오너", value=ctx.guild.owner, inline=False)
        embed.add_field(name="시스템 채널", value="#" + welcome, inline=False)
        embed.add_field(name="서버 위치", value=ctx.guild.region, inline=True)

        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command(
        name="유저정보", rest_is_raw=True, aliases=["유저", "이유저", "이 유저"]
    )
    @commands.guild_only()
    async def user_info(self, ctx, *, args):
        try:
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
            date = "%s (UTC)" % ctx.guild.get_member(a).created_at
            try:
                game = ctx.guild.get_member(a).activity
                if game.type == discord.ActivityType.listening:
                    game = game.title + " - " + ", ".join(game.artists)
                else:
                    game = game.name
            except:
                game = "플레이 중인 게임이 없습니다."
            if game is None:
                game = "플레이 중인 게임이 없습니다."
            member = ctx.guild.get_member(a)
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

            embed = discord.Embed(
                title="ℹ️ 유저 정보",
                description="선택하신 유저에 대한 정보를 불러왔습니다.\n\n",
                color=0x1DC73A,
            )
            embed.add_field(
                name="이름", value=ctx.guild.get_member(a).name, inline=False
            )
            embed.add_field(
                name="유저 ID", value=ctx.guild.get_member(a).id, inline=True
            )
            embed.add_field(name="계정 생성일", value=date, inline=True)
            embed.add_field(
                name="서버 가입일", value=joined + " (UTC)", inline=False
            )

            embed.add_field(name="플레이 중", value=game, inline=True)
            embed.add_field(name="상태", value=status, inline=False)

            insignia = await self.get_insignia(a)
            embed.set_thumbnail(url=asdf)
            await ctx.send(embed=embed)
            if insignia is not None:
                embed1 = discord.Embed(title=" ")
                embed1.set_thumbnail(url=insignia)
                await ctx.send(embed=embed1)  # <:mut:664836978520621076>
        except:
            embed = Embed.warn(
                "주의", "`봇 유저정보 <멘션 or ID>` 로 사용해주세요. 유저를 불러오지 못했어요."
            )
            embed.set_footer(text="이 서버에 있는 유저가 아니면 불러올 수 없어요!")
            await ctx.send(embed=embed)

    @commands.command(name="질문")
    async def question(self, ctx):
        response = [
            "아니요?",
            "아뇨?",
            "어...음...네",
            "흐음...아뇨?",
            "모르겠어요",
            "네",
            "맞아요",
            "흐음...몰라요",
        ]
        a = random.choice(response)
        await ctx.send(a)

    @commands.command(name="확률")
    async def percent(self, ctx, *, args):
        a = args.lstrip()
        per = random.randint(0, 100)
        await ctx.send("`%s` 은 `%s%%`입니다." % (a, per))

    @commands.command(name="날씨")
    async def weather(self, ctx, *, city):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "http://api.openweathermap.org/data/2.5/weather?q="
                + city
                + "&APPID="
                + TOKEN.weather
                + "&units=metric"
            ) as r:
                if r.status == 200:
                    c = await r.json()
                    embed = discord.Embed(
                        title="⛅ %s 날씨" % (c["name"]),
                        description="%s (구름 %s%%)"
                        % (c["weather"][0]["main"], c["clouds"]["all"]),
                        color=0x1DC73A,
                    )
                    embed.add_field(
                        name="온도", value="%s °C" % (c["main"]["temp"])
                    )
                    embed.add_field(
                        name="바람",
                        value="%sm/s (%s°)"
                        % (c["wind"]["speed"], c["wind"]["deg"]),
                        inline=False,
                    )
                    embed.add_field(
                        name="기타",
                        value="기압 : %shPa\n습도 : %s%%"
                        % (c["main"]["pressure"], c["main"]["humidity"]),
                    )
                    embed.set_thumbnail(
                        url="http://openweathermap.org/img/w/%s.png"
                        % (c["weather"][0]["icon"])
                    )
                    embed.set_footer(text="OpenWeatherMap.org")
                    await ctx.send(embed=embed)
                elif r.status == 404:
                    embed = discord.Embed(
                        title="⚠ 주의",
                        description="선택하신 도시를 찾지 못했어요. 다음을 시도해보세요:\n\n1. 지역명 뒤에 시, 광역시 붙이기 (`봇 날씨 부산광역시`)\n2. 주변에 있는 주요 도시로 재시도\n3. 영어로 해보기 (`봇 날씨 tokyo`)",
                        color=0xD8EF56,
                    )
                    await ctx.send(embed=embed)


def setup(bot):
    bot.remove_command("help")
    bot.add_cog(Chatting(bot))
