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
import datetime
import os
import random
from bs4 import BeautifulSoup
import sys 
import aiohttp
import asyncio
import requests 
import json 
import time


import TOKEN
from send import Command

'''
봇의 간단한 문답 기능을 수록합니다.
단, 간단하게 채팅으로 가능한 명령어는 이곳에 수록합니다. 
{100줄 이상 명령어 또는 특수 기능(게임 등)은 제외}
'''

# def restart_bot():
#     python = sys.executable
#     os.execl(python, python, * sys.argv)

''' Function '''
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


''' Main '''

class chatting(Command):
    
    def __init__(self, *args, **kwargs):
        Command.__init__(self, *args, **kwargs)
        self.bot_start_time = datetime.datetime.now()
        
    async def on_message(self, message):



        if message.content.startswith("봇 온도"):
            try:
                a = os.popen("vcgencmd measure_temp").read()
                a = a.replace("temp=","")
                a = a.replace("'C", "")
                a = a.replace("\n","")
                a = float(a)
                if a < 45:
                    embed=discord.Embed(title="✅ 서버 온도", description="현재 서버 온도는 %s°C 입니다." %(str(a)),color=0x1dc73a )
                    embed.set_footer(text="온도가 좋습니다.")

                if 45 <= a and a<50:
                    embed=discord.Embed(title="⚠ 서버 온도", description="현재 서버 온도는 %s°C 입니다." %(str(a)),color=0xd8ef56)
                    embed.set_footer(text="온도가 보통입니다.")
                if 50 <= a:
                    embed=discord.Embed(title="❌ 서버 온도", description="현재 서버 온도는 %s°C 입니다." %(str(a)),color=0xff0909)
                    embed.set_footer(text="온도가 높습니다.")
                await message.channel.send(embed=embed)
            except:
                embed=discord.Embed(title="⚠ 오류", description="시스템에서 온도를 불러오는데에 실패했습니다.",color=0xff0909)
                await message.channel.send(embed=embed)

        if message.content.startswith("봇 따라해"): 
            if "@everyone" in message.content or "@here" in message.content :
                embed=discord.Embed(title="⚠ 경고", description="`@everyone`이나 `@here`은 다른 사용자에게 피해를 줄 수 있습니다.\n사용이 제한됩니다." ,color=0xff0909 )
                embed.set_footer(text=message.author)
                await message.channel.send(embed=embed)
            else:
                try:
                    await message.delete()
                except:
                    pass
                await message.channel.send(message.content[6:])

        if message.content.startswith("봇 거꾸로"):
            try:
                await message.delete()
            except:
                pass
            
            a = message.content[6:]
            a = ''.join(reversed(a))
            if "@everyone" in a or "@here" in a:
                embed=discord.Embed(title="⚠ 경고", description="`@everyone`이나 `@here`은 다른 사용자에게 피해를 줄 수 있습니다.\n사용이 제한됩니다." ,color=0xff0909 )
                embed.set_footer(text=message.author)
                await message.channel.send(embed=embed)
            else:
                await message.channel.send(a)

        if message.content.startswith("봇 서버랭"):
            rank = {}
            allguild = self.client.guilds
            for i in allguild:
                rank[i] = int(i.member_count)
            rank = sorted(rank, key=lambda k : rank[k], reverse=True)
            number = 0
            totalserver = str(len(allguild))
            totalperson = 0
            embed=discord.Embed(title="서버 랭크", description="서버 이름 / 인원수" , color=0x237ccd)

            for i in rank:
                number += 1
                totalperson += int(i.member_count)
                embed.add_field(name=str(number)+"위", value="%s / %s명" %(i.name, i.member_count),inline=False)

                if number == 10:
                    break                                       
            await message.channel.send(embed=embed)

        if message.content.startswith("봇 업타임"):
            uptime = datetime.datetime.now() - self.bot_start_time
            # days = uptime.day
            # hours = uptime.hour
            # minitues = uptime.minute
            # seconds = uptime.second
            day = uptime.days
            day = str(day)

            uptime = str(uptime)
            uptime = uptime.split(":")

            hours = uptime[0]

            hours = hours.replace(" days,","일")
            hours = hours.replace(" day,","일")

            minitues = uptime[1]

            seconds = uptime[2]
            seconds = seconds.split(".")
            seconds = seconds[0]

            embed=discord.Embed(title="봇 업타임", description="봇이 동작한 시간은  %s시간 %s분 %s초 입니다." %(hours,minitues,seconds) , color=0x237ccd)

            await message.channel.send(embed=embed)


        if message.content.startswith('봇 도움'):
            a = message.content
            a = a[5:]
            if a == "":
                embed=discord.Embed(title="📜 도움말", description="봇의 사용을 도와줄 도움말입니다. 다음 명령어 그룹들을 참고하세요.", color=0x237ccd)
                # embed.add_field(name="봇 도움 기타", value="기타 도움말입니다. 자세한 명령어는 '봇 도움 기타'을 참고하세요.", inline=False)
                # embed.add_field(name="봇 도움 게임", value="봇에 있는 게임 기능에 관련된 도움말입니다. 자세한 명령어는 '봇 도움 게임'을 참고하세요.", inline=True)
                embed.add_field(name="봇 도움 기능", value="봇에 있는 기능에 대해 알려드립니다.", inline=True)
                embed.add_field(name="봇 도움 어드민", value="어드민이 서버 관리를 위해 사용 가능한 기능입니다. 자세한 명령어는 '봇 도움 어드민'을 참고하세요.", inline=True)

                
                embed.set_footer(text="도움 명령어에 없는 명령어가 있을 수 있습니다.")
                try:
                    await message.author.send(embed=embed)
                    await message.channel.send("DM으로 메시지를 보냈습니다. 확인하세요.")
                except:
                    embed=discord.Embed(title="⚠ 주의", description="DM 보내기에 실패하였습니다. 계정에서 DM 설정을 확인해주세요.",color=0xd8ef56)
                    await message.channel.send(embed=embed)
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
            #         await message.channel.send(embed=embed)

            elif a == "기능":
                embed=discord.Embed(title=" ", description="봇에 있는 편리한 기능을 설명합니다.", color=0x237ccd)
                embed.add_field(name="봇 프사 @상대", value="멘션한 상대의 프로필 사진을 가져옵니다. 상대를 지정하지 않으면 자신의 프로필 사진을 가져옵니다.", inline=False)
                embed.add_field(name="봇 백과사전 <검색어>", value="백과사전에서 검색어를 검색해줍니다.", inline=False)
                embed.add_field(name="봇 나무위키 <검색어>", value="해당 나무위키 검색어로 바로가는 나무위키 링크를 표시하고, 문서를 일부분 미리 볼 수 있습니다.")
                # embed.add_field(name="봇 도서검색 <검색어>", value="도서를 검색해줍니다.", inline=False)
                embed.add_field(name="봇 afk/잠수 <사유>", value="잠수를 선언합니다. 다시 돌아오면 환영해드립니다.", inline=False)
                embed.add_field(name="봇 자동번역 <번역할 문장>", value="언어를 자동으로 인식한 후 한국어로 번역합니다.")
                embed.add_field(name="봇 한글영어번역(영어한글번역, 일어한글번역, 한글일어번역) <번역할 문장>", value="선택한 언어에서 선택한 언어로 번역해줍니다.", inline=False)

                # embed.add_field(name="봇 죽창 <개수>", value="죽창을 표시합니다. 60개가 최대입니다.",inline=False)
                embed.add_field(name="봇 지진", value="지진 정보를 표시합니다.", inline=False)
                embed.add_field(name="봇 별명변경 <바꿀별명>", value="입력한 별명으로 별명을 변경합니다.", inline=False)
                embed.add_field(name="봇 조의 표해", value="봇이 조의를 표해줍니다.", inline=False)
                embed.add_field(name="봇 고양이/냥이", value="랜덤으로 고양이짤을 보여준다냐!", inline=False)
                embed.add_field(name="봇 강아지", value="랜덤으로 강아지짤을 보여준다멍.", inline=False)
                # embed.add_field(name="봇 원주율 구해", value="원주율을 1997자리 까지 구합니다.", inline=False)
                embed.add_field(name="봇 리마인더 <시간(초)> <사유(선택)>", value="선택한 초 있다가 알려드려요.", inline=False)

                embed.add_field(name="봇 기상특보", value="기상특보 정보를 표시합니다.", inline=False)
                embed.add_field(name="봇 미세먼지", value="미세먼지 정보를 표시합니다.", inline=False)
                # embed.add_field(name="봇 11번가 검색 <검색어>", value="11번가에서 검색해, 정보를 불러옵니다.", inline=False)
                embed.add_field(name="봇 초미세먼지", value="초미세먼지 정보를 표시합니다.", inline=False)
                embed.add_field(name="봇 멜론차트", value="멜론 TOP10을 보여줍니다.", inline=False)
                embed.add_field(name="봇 가사검색", value="선택한 노래의 가사를 검색해줍니다. 가끔 다른 노래 가사가 들어갈수도 있으니 자세히 보기로 확인해보시는것도 좋아요!", inline=False)
                embed.add_field(name="봇 날씨 [도시]", value="선택한 도시의 현재 날씨를 보여줍니다.", inline=False)

                embed.add_field(name="더 많은 기능은?", value="궁금증이나 도움 명령어에 수록되지 않은 명령어는 BGM#0970으로 친추후 DM해주세요!", inline=False)

                # embed.add_field(name="봇 명언은?", value="명언을 표시합니다. (명언인지 확인안됨)", inline=False)
                # embed.add_field(name="봇 서버 인원은?", value="채팅한 서버의 인원을 표시합니다.", inline=False)

                embed.set_footer(text="도움 명령어에 없는 명령어가 있을 수 있습니다.")
                try:
                    await message.author.send(embed=embed)
                except:
                    embed=discord.Embed(title="⚠ 주의", description="DM 보내기에 실패하였습니다. 계정에서 DM 설정을 확인해주세요.",color=0xd8ef56)
                    await message.channel.send(embed=embed)
            elif a == "어드민":
                embed=discord.Embed(title=" ", description="봇에 있는 서버의 관리자가 사용할때 유용한 기능입니다.", color=0x237ccd)
                embed.add_field(name="봇 킥 @유저", value="선택한 유저를 킥합니다.", inline=False)
                embed.add_field(name="봇 밴 @유저", value="선택한 유저를 밴합니다.", inline=False)
                embed.add_field(name="봇 언밴 @유저 또는 유저 ID ", value="선택한 유저를 언밴합니다. 유저 ID는 데스크톱 버전에서 오른쪽키 > ID복사로 얻으실 수 있습니다.", inline=False)
                embed.add_field(name="봇 뮤트 @유저", value="유저를 해당 채널에서 뮤트시킵니다.", inline=False)
                embed.add_field(name="봇 전체뮤트", value="명령어를 사용한 채널을 관리자 제외 모든 유저가 사용할 수 없도록 합니다.", inline=False)
                embed.add_field(name="봇 언뮤트 @유저", value="유저를 해당 채널에서 언뮤트시킵니다.", inline=False)
                embed.add_field(name="봇 전체언뮤트", value="전체뮤트를 해제합니다.", inline=False)
                embed.add_field(name="봇 커스텀 추가 <명령어>/<봇의 대답>", value="해당 서버만 사용되는 커스텀 명령어를 추가합니다. 명령어와 봇의 대답 구분에는 꼭 /가 필요합니다.", inline=False)
                embed.add_field(name="봇 커스텀 수정 <수정할 명령어>/<봇의 대답>", value="이미 추가된 커스텀 명령어를 수정합니다. 명령어와 봇의 대답 구분에는 꼭 /가 필요합니다.", inline=False)
                embed.add_field(name="봇 커스텀 보기", value="해당 서버의 모든 커스텀 명령어를 출력합니다.", inline=False)
                embed.add_field(name="봇 커스텀 삭제 [삭제할 커스텀 명령어]", value="해당 서버의 커스텀 명령어중 입력한 명령어를 삭제합니다.", inline=False)

                embed.add_field(name="봇 커스텀 초기화", value="해당 서버의 모든 커스텀 명령어를 삭제합니다.", inline=False)
                embed.add_field(name="더 많은 기능은?", value="궁금증이나 도움 명령어에 수록되지 않은 명령어는 BGM#0970으로 친추후 DM해주세요!", inline=False)

                embed.set_footer(text="도움 명령어에 없는 명령어가 있을 수 있습니다.")

                try:
                    await message.author.send(embed=embed)
                except:
                    embed=discord.Embed(title="⚠ 주의", description="DM 보내기에 실패하였습니다. 계정에서 DM 설정을 확인해주세요.",color=0xd8ef56)
                    await message.channel.send(embed=embed)
            # elif a == "기타":
            #     embed=discord.Embed(title=" ", description="봇에 있는 다른 잡다한 기능들을 소개합니다.", color=0x237ccd)
            #     embed.add_field(name="봇 철컹철컹", value="??? : 철컹", inline=False)
            #     try:
            #         await message.author.send(embed=embed)
            #     except:
            #         embed=discord.Embed(title="⚠ 주의", description="DM 보내기에 실패하였습니다. 계정에서 DM 설정을 확인해주세요.",color=0xd8ef56)
            #         await message.channel.send(embed=embed)
            
            else:
                embed=discord.Embed(title="⚠ 주의", description="해당 도움 그룹이 없습니다. 존재하는 도움 그룹은 \n``` 기능, 어드민``` 입니다.",color=0xd8ef56)
                await message.channel.send(embed=embed)

        if message.content.startswith('봇 안녕') or message.content.startswith('봇 안냥') or message.content.startswith("봇 ㅎㅇ") or message.content.startswith("봇 gd") or message.content.startswith("봇 hello"):
            a = self.client.user.id
            bot_profile = self.client.get_user(a).avatar_url

            embed = discord.Embed(title="👋 안녕하세요!", description="**봇을 사용해 주셔서 감사합니다!**\n봇 / BOT은 BGM#0970이 개발중인 디스코드 봇입니다.\n\n자세한 내용은 `봇 도움` 명령어를 사용해주세요." ,color=0x237ccd)
            embed.set_thumbnail(url=bot_profile)
            await message.channel.send(embed=embed)


        if message.content.startswith('봇 별명변경'):
            try:
                a = message.content
                a = a[6:]
                b = a.lstrip()
                memberid = message.author.id
                member = message.guild.get_member(memberid)

                await member.edit(nick=b)
                embed=discord.Embed(title="✅ 별명 변경", description="별명 변경에 성공하였습니다.",color=0x1dc73a )

                await message.channel.send(embed=embed)
            except:
                embed=discord.Embed(title="❌ 오류 발생", description="봇의 권한이 부족하거나 사용자의 권한이 봇보다 높습니다.",color=0xff0909)
                await message.channel.send(embed=embed)

        if message.content.startswith('봇 별명 초기화') or message.content.startswith("봇 별명초기화"):
            try:
                memberid = message.author.id
                member = message.guild.get_member(memberid)
                await member.edit(nick=None)
                embed=discord.Embed(title="✅ 별명 변경", description="별명 초기화에 성공하였습니다.",color=0x1dc73a )

                await message.channel.send(embed=embed)
            except:
                embed=discord.Embed(title="❌ 오류 발생", description="봇의 권한이 부족하거나 사용자의 권한이 봇보다 높습니다.",color=0xff0909)
                await message.channel.send(embed=embed)


        if message.content.startswith("봇 시간계산"):
            try:
                if not message.content[6:] == "":
                    answer = message.content[6:].lstrip()
                else:
                    embed=discord.Embed(title="봇 시간계산", description="yyyy-mm-dd 형식으로 입력해주세요.",color=0x237ccd)
                    await message.channel.send(embed=embed)
                    def usercheck(a):
                        return a.author == message.author

                    answer = await self.client.wait_for('message', check=usercheck)
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
                embed=discord.Embed(title="⏲ 시간 계산", description=str(days) + "일 " + str(hours) + "시간 " + str(minutes) + "분 " + str(int(round(seconds,0))) + "초 남았습니다.",color=0x237ccd)
                embed.set_footer(text="과거 시간은 계산값이 정확하지 않습니다.")
        
                await message.channel.send(embed=embed )
            except Exception as error:
                embed=discord.Embed(title="❌ 오류 발생", description="형식을 제대로 입력하셨는지 학인하시거나, 값 한도를 초과했는지 확인해주세요.. \n\n0001-01-01 ~ 9999-12-31 %s" %(error),color=0xff0909 )
                await message.channel.send(embed=embed)

        # if message.content.startswith("봇 해티는?"):
        #     embed=discord.Embed(title="이름", description="해티 (본명 : 김도훈)", color=0x4286f4)
        #     embed.set_author(name="기여운 해티의 정보입니다.")
        #     embed.add_field(name="성별", value="남", inline=False)
        #     embed.add_field(name="좋아하는 것", value="Python, <@289729741387202560> (BGM#0970), 디스코드", inline=True)
        #     embed.add_field(name="싫어하는 것", value="햇반, 갈아만든 배, Jollyed, 크콩", inline=True)
        #     await message.channel.send(embed=embed)

        if message.content.startswith("봇 핑"):
            nowasdf = datetime.datetime.now()
            await message.channel.trigger_typing()
            latertime = datetime.datetime.now()            
            ping = latertime - nowasdf

            asdf = str(int(ping.microseconds) / 1000)
            asdf = asdf.split(".")
            asdf = asdf[0]
            embed=discord.Embed(title="🏓 퐁! " + asdf+"ms", description=str(ping.microseconds) + "μs", color=0x237ccd)
            embed.set_footer(text="이 수치는 봇이 메시지에 반응하는 속도입니다.")
            await  message.channel.send(embed=embed)
            
        if message.content.startswith("봇 퐁"):
            nowasdf = datetime.datetime.now()
            await message.channel.trigger_typing()
            latertime = datetime.datetime.now()            
            ping = latertime - nowasdf

            asdf = str(int(ping.microseconds) / 1000)
            asdf = asdf.split(".")
            asdf = asdf[0]
            embed=discord.Embed(title="🏓 핑! " + asdf+"ms", description=str(ping.microseconds) + "μs", color=0x237ccd)
            embed.set_footer(text="이 수치는 봇이 메시지에 반응하는 속도입니다.")
            await message.channel.send(embed=embed)
            
        if message.content.startswith("봇 리마인더"):
            a = message.content[6:]
            a = a.lstrip()
            a = a.split()
            try:
                set_time = int(a[0])
                try:  
                    del a[0]
                    reason = ""
                    for i in a:
                        reason = reason + i + " "
                    if not reason == "":
                        embed=discord.Embed(title="✅ 리마인더", description="리마인더에 기록 완료했어요! %s초 있다가 `%s`하라고 알려드릴께요!" %(str(set_time), reason),color=0x1dc73a )
                    else:
                        embed=discord.Embed(title="✅ 리마인더", description="리마인더에 기록 완료했어요! %s초 있다가 알려드릴께요!" %(str(set_time)),color=0x1dc73a )
            
                except IndexError as error:
                    await message.channel.send(error)
                embed.set_footer(text="봇이 꺼지면 초기화됩니다. 유의하여 주십시오.")
                await message.channel.send(embed=embed)
                await asyncio.sleep(set_time)
                await message.channel.send(message.author.mention)
                embed=discord.Embed(title="⏰ 알림", description="시간이 다 되었어요!" ,color=0x1dc73a )
                if not reason == "":
                    embed.add_field(name="내용", value=reason)
                await message.channel.send(embed=embed)

                
            except Exception as error:
                embed=discord.Embed(title="❌ 오류 발생", description="봇 리마인더 <시간(초)> <사유(선택)> 형식으로 사용해주세요. \n```%s```     "%(error) ,color=0xff0909)    
                await message.channel.send(embed=embed)


        if message.content.startswith('봇 히오스는?'): 
            choice = ["hos.PNG", "hosjongnews.PNG", "hosmang.PNG", "wehatehos.PNG"]
            await message.channel.send(file=discord.File(random.choice(choice)))

        if message.content == ("봇 시공"):
            response = ["**싫음**","너나 해 이 악마야","`봇 시공은?` 계속 쳐봐!","시공이 재밌냐?","싫음.","시 공 시 렁"]
            response = random.choice(response)
            await message.channel.send(response)

        if message.content == ("봇 시공은?"):
            response = ["**싫음**","너나 해 이 악마야","`봇 히오스는?` 계속 쳐봐!","시공이 재밌냐?","싫음.","시 공 시 렁"]
            response = random.choice(response)
            await message.channel.send(response)

        if message.content.endswith("봇 조의 표해"):
            await message.add_reaction("❌")
            await message.add_reaction("✖")
            await message.add_reaction("🇽")
            await message.add_reaction("🇯")
            await message.add_reaction("🇴")
            await message.add_reaction("🇾")

        # if message.content == ("봇 지진"):
        #     async with aiohttp.ClientSession() as session:
        #         async with session.get("https://m.kma.go.kr/m/eqk/eqk.jsp?type=korea") as r:

        #             c = await r.text()
        #             soup = BeautifulSoup(c,"html.parser")
        #             table = soup.find("table",{"class":"table02"})
        #             tr = table.find_all("tr")

        #             embed=discord.Embed(title="지진 정보", description=a,color=0x62bf42)
        #             try:
        #                 img = all[0].find_all("img")[0]['src']
        #                 img = "http://m.kma.go.kr" + img
        #                 if img is None: pass
        #                 else: embed.set_image(url=img)



        #             except:
        #                 pass

        #             embed.add_field(name="규모", value=b, inline=True)
        #             embed.add_field(name="발생위치", value=c, inline=True)
        #             embed.add_field(name="발생깊이", value=d, inline=True)
        #             embed.add_field(name="진도", value=e, inline=True)
        #             embed.add_field(name="참고사항", value=f, inline=True)
        #             embed.set_footer(text="기상청")


        #             await message.channel.send(embed=embed)

        if message.content.startswith("봇 골라"):
            if "@everyone" in message.content or "@here" in message.content:
                embed=discord.Embed(title="⚠ 경고", description="`@everyone`이나 `@here`은 다른 사용자에게 피해를 줄 수 있습니다.\n사용이 제한됩니다." ,color=0xff0909 )
                embed.set_footer(text=message.author)
                await message.channel.send(embed=embed)
            else:
                a = message.content
                a = a[4:]
                a = a.lstrip().split(",")
                a = random.choice(a)
                embed=discord.Embed(title="❔봇의 선택", description=a,color=0x1dc73a )
                await message.channel.send(embed=embed)

        if message.content.startswith("봇 기상특보"):
            async with aiohttp.ClientSession() as session:
                async with session.get('http://newsky2.kma.go.kr/service/WetherSpcnwsInfoService/WeatherWarningItem?serviceKey=' + TOKEN.weather_warn) as r:
                    c = await r.text()
                    soup = BeautifulSoup(c,"lxml-xml")
                    title = lxml_string(soup, "t1")
                    area = lxml_string(soup, "t2")
                    content = lxml_string(soup, "t4")
                    now = lxml_string(soup, "t6")
                    will = lxml_string(soup, "t7")
                    cham = lxml_string(soup, "other")

                    embed=discord.Embed(title="🌥 기상특보", description="현재 기준 기상특보 입니다.",color=0x62bf42)
                    
                    embed.add_field(name="현재 특보 제목", value=title)
                    embed.add_field(name="발효 지역", value=area)
                    embed.add_field(name="내용", value=content)
                    embed.add_field(name="특보 현황 내용", value=now)


                    embed.add_field(name="예비특보", value=will)
                    embed.set_footer(text="기상청")

                    await message.channel.send(embed=embed)


        if message.content.startswith("봇 뽑기"):

            embed=discord.Embed(title="🔄 유저 불러오는 중", description="온라인 유저를 불러옵니다.",color=0x1dc73a )
            await message.channel.send(embed=embed)
            online = []
            for i in message.guild.members:
                if i.status == discord.Status.offline:
                    pass
                else:
                    online.append(i.id)

            embed=discord.Embed(title="✅ 뽑기 성공", description="<@%s>님 당첨!" %(str(random.choice(online))),color=0x1dc73a )

            await message.channel.send(embed=embed)


#💨

        if message.content.startswith("봇 미세먼지"):
            async with aiohttp.ClientSession() as session:
                async with session.get('http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureLIst?serviceKey=' + TOKEN.misae +  '&numOfRows=1&pageSize=1&pageNo=1&startPage=1&itemCode=PM10&dataGubun=HOUR') as r:
                    c = await r.text()
                    
                    soup = BeautifulSoup(c,"lxml-xml")
                    datatime = lxml_string(soup, "dataTime")
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
                    sido = {"서울" : seoul, "부산" : busan, "대구":daegu, "인천":incheon, "광주":gwangju, "대전":daejon, "울산":ulsan, "경기":gyeonggi, "강원": gangwon, "충북": chungbuk, "충남":chungnam, "전북":jeonbuk, "전남" : jeonnam, "경북" : gyeongbuk, "경남" : gyeongnam, "제주":jeju, "세종": sejong}
                    embed=discord.Embed(title="💨 PM10 미세먼지 농도", description=datatime + " 기준", color=0x1dc73a )
                    embed.set_footer(text="에어코리아")
                    name = message.content[6:].lstrip()
                    if name == "":
                        for i in sido.keys():
                            embed.add_field(name=i, value="%s㎍/m³ | %s" %(sido[i], checkpm10(sido[i])), inline=True)
                        await message.channel.send(embed=embed)
                    else:
                        if name in sido.keys():
                            embed.add_field(name=name, value="%s㎍/m³ | %s" %(sido[name], checkpm10(sido[name])), inline=True)
                            await message.channel.send(embed=embed)
                        else:
                            embed=discord.Embed(title="⚠ 주의", description="지역 이름이 없습니다. 시·도별기준으로 불러오며, 도는 줄인 이름으로, 광역시는 `광역시` 글자를 제거해주세요.\n\n```ex) 경북, 경기, 서울, 광주...```",color=0xd8ef56)
                            await message.channel.send(embed=embed)


        if message.content.startswith("봇 초미세먼지"):
            async with aiohttp.ClientSession() as session:
                async with session.get('http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureLIst?serviceKey=' + TOKEN.misae + '&numOfRows=1&pageSize=1&pageNo=1&startPage=1&itemCode=PM25&dataGubun=HOUR') as r:
                    c = await r.text()
                    
                    soup = BeautifulSoup(c,"lxml-xml")
                    datatime = lxml_string(soup, "dataTime")
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
                    sido = {"서울" : seoul, "부산" : busan, "대구":daegu, "인천":incheon, "광주":gwangju, "대전":daejon, "울산":ulsan, "경기":gyeonggi, "강원": gangwon, "충북": chungbuk, "충남":chungnam, "전북":jeonbuk, "전남" : jeonnam, "경북" : gyeongbuk, "경남" : gyeongnam, "제주":jeju, "세종": sejong}
                    embed=discord.Embed(title="💨 PM2.5 초미세먼지 농도", description=datatime + " 기준", color=0x1dc73a )
                    embed.set_footer(text="에어코리아")
                    name = message.content[7:].lstrip()
                    if name == "":
                        for i in sido.keys():
                            embed.add_field(name=i, value="%s㎍/㎥ | %s" %(sido[i], checkpm25(sido[i])), inline=True)
                        await message.channel.send(embed=embed)
                    else:
                        if name in sido.keys():
                            embed.add_field(name=name, value="%s㎍/㎥ | %s" %(sido[name], checkpm25(sido[name])), inline=True)
                            await message.channel.send(embed=embed)
                        else:
                            embed=discord.Embed(title="⚠ 주의", description="지역 이름이 없습니다. 시·도별기준으로 불러오며, 도는 줄인 이름으로, 광역시는 `광역시` 글자를 제거해주세요.\n\n```ex) 경북, 경기, 서울, 광주...```",color=0xd8ef56)
                            await message.channel.send(embed=embed)

        if message.content.startswith("봇 프사"):
            memberid = message.content[4:].lstrip()
            memberid = memberid.replace("<@", "")
            memberid = memberid.replace("!", "")
            memberid = memberid.replace(">", "")
            if memberid == "":
                memberid = message.author.id
                member = self.client.get_user(memberid)
                a = member.avatar_url
                if a == "":
                    a = member.default_avatar_url
                embed=discord.Embed(title="🖼️ 프로필 사진", description="",color=0x62bf42)

                embed.set_image(url=a)
                await message.channel.send(embed=embed)
                
            else:
                memberid = int(memberid)

                member = self.client.get_user(memberid)
                a = member.avatar_url
                if a == "":
                    a = member.default_avatar_url
                embed=discord.Embed(title="🖼️ 프로필 사진", description="",color=0x62bf42)

                embed.set_image(url=a)
                await message.channel.send(embed=embed)

        if message.content.startswith("봇 가사검색"):   
            try:
                a = message.content[6:].lstrip()
                if a == "":
                    embed=discord.Embed(title="⚠ 주의", description="검색어가 없습니다.",color=0xd8ef56)
                    await message.channel.send(embed=embed)
                else:     
                    async with aiohttp.ClientSession() as session:
                        async with session.get("http://music.naver.com/search/search.nhn?query=" + a + "&target=track") as r:

                            c = await r.text()
                            soup = BeautifulSoup(c,"html.parser")
                            f = soup.find_all("a",{"title":"가사"})[0]['class'][1]
                            print(f)
                            f = f.split(",")
                            # print(f)
                            f = f[2]
                            f = f[2:]
                            load = "http://music.naver.com/lyric/index.nhn?trackId=" + f
                            async with aiohttp.ClientSession() as session:
                                async with session.get(load) as r:
                                    c = await r.text()
                                    soup = BeautifulSoup(c,"html.parser")
                                    f = soup.find("div",{"id":"lyricText"}).text
                                    f = f[:100]
                                    embed=discord.Embed(title="🎵 " + a + "에 대한 가사 검색", description="\n" + f +"...", color=0x237ccd)
                                    embed.add_field(name="자세히 보기", value=load, inline=False)

                                    await message.channel.send(embed=embed)
            except Exception as error:
                embed=discord.Embed(title="❌ 오류", description="오류가 발생하였습니다.\n%s",color=0xff0909)
                await message.channel.send(embed=embed)


        
        if message.content.startswith("봇 한강"):
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
                        await message.channel.send(embed=embed)
                    else:
                        embed=discord.Embed(title="❌ 오류 발생", description="API에서 정보를 제공하지 않습니다.",color=0xff0909)
                        await message.channel.send(embed=embed)


        if message.content.startswith("봇 영어한글번역"):
            a = message.content[8:].lstrip()
            trans = await nmt("en", "ko", a)
            if trans is None:
                embed=discord.Embed(title="❌ 오류 발생", description="번역에 오류가 발생하였습니다.",color=0xff0909)
                await message.channel.send(embed=embed)
            else:
                embed=discord.Embed(title="✅ 한글 번역", description=trans,color=0x1dc73a )
                await message.channel.send(embed=embed)

        if message.content.startswith("봇 한글영어번역"):
            a = message.content[8:].lstrip()
            trans = await nmt("ko", "en", a)
            if trans is None:
                embed=discord.Embed(title="❌ 오류 발생", description="번역에 오류가 발생하였습니다.",color=0xff0909)
                await message.channel.send(embed=embed)
            else:
                embed=discord.Embed(title="✅ 영어 번역", description=trans,color=0x1dc73a )
                await message.channel.send(embed=embed)


        if message.content.startswith("봇 일어한글번역"):
            a = message.content[8:].lstrip()
            trans = await nmt("ja", "ko", a)
            if trans is None:
                embed=discord.Embed(title="❌ 오류 발생", description="번역에 오류가 발생하였습니다.",color=0xff0909)
                await message.channel.send(embed=embed)
            else:
                embed=discord.Embed(title="✅ 한글 번역", description=trans,color=0x1dc73a )
                await message.channel.send(embed=embed)

        if message.content.startswith("봇 한글일어번역"):
            a = message.content[8:].lstrip()
            trans = await nmt("ko", "ja", a)
            if trans is None:
                embed=discord.Embed(title="❌ 오류 발생", description="번역에 오류가 발생하였습니다.",color=0xff0909)
                await message.channel.send(embed=embed)
            else:
                embed=discord.Embed(title="✅ 일본어 번역", description=trans,color=0x1dc73a )
                await message.channel.send(embed=embed)

        if message.content.startswith("봇 자동번역"):
            a = message.content[6:].lstrip()
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
                                    embed=discord.Embed(title="⚠ 주의", description="언어가 한국어로 감지되었습니다. 한국어가 많이 섞여있다면 한국어를 삭제해보시고 다시 시도해주세요." ,color=0xd8ef56)
                                    await message.channel.send(embed=embed)



                                else:
                                    trans = await nmt(langcode, "ko", a)
                                    if trans is None:
                                        embed=discord.Embed(title="❌ 오류 발생", description="번역에 오류가 발생하였습니다.",color=0xff0909)
                                        await message.channel.send(embed=embed)
                                    else:
                                        embed=discord.Embed(title="✅ 자동 번역", description=trans,color=0x1dc73a )
                                        embed.set_footer(text=langcode + " >> ko")
                                        await message.channel.send(embed=embed)

                            else:
                                embed=discord.Embed(title="❌ 오류 발생", description="번역에 오류가 발생하였습니다.",color=0xff0909)
                                await message.channel.send(embed=embed)
            except:
                embed=discord.Embed(title="❌ 오류 발생", description="언어 감지에 오류가 발생하였습니다.",color=0xff0909)
                await message.channel.send(embed=embed)

        if message.content.startswith("봇 백과사전"):
            try:
                a = message.content[6:].lstrip()
                if a == "":
                    embed=discord.Embed(title="⚠ 주의", description="검색어가 없습니다.",color=0xd8ef56)
                    await message.channel.send(embed=embed)
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
                            embed=discord.Embed(title="🔖 백과사전", description="**" + title+ "**에 대한 검색결과.", color=0x237ccd)
                            embed.add_field(name="내용", value=description, inline=False)
                            embed.add_field(name="자세히 읽기", value=link, inline=False)
                            embed.set_image(url=thumbnail)

                            await message.channel.send(embed=embed)

            except:
                embed=discord.Embed(title="❌ 오류 발생", description="해당 검색어에 대한 내용을 찾을 수 없습니다.",color=0xff0909)
                await message.channel.send(embed=embed)



        if message.content.startswith("봇 링크축약") or message.content.startswith("봇 링크단축") or message.content.startswith("봇 주소단축") or message.content.startswith("봇 주소축약"):
            a = message.content[6:].lstrip()
            headers = {"X-Naver-Client-Id" : TOKEN.url_id, "X-Naver-Client-Secret" : TOKEN.url_secret}
            data = {"url":a}
            try:
                async with aiohttp.ClientSession(headers=headers) as session:
                    async with session.post("https://openapi.naver.com/v1/util/shorturl", data=data) as r:
                            if r.status == 200:
                                c = await r.json()
                                url = c["result"]["url"]
                                embed=discord.Embed(title="✅ 링크 축약", description="링크 축약을 성공하였습니다.",color=0x1dc73a )
                                embed.add_field(name="처음 URL", value=a)
                                embed.add_field(name="단축된 URL", value=url)
                                await message.channel.send(embed=embed)
                            else:
                                embed=discord.Embed(title="❌ 오류 발생", description="정상적인 값이 출력되지 않았습니다. 나중에 다시 시도해주세요.\nHTTP CODE : %s" %(r.status),color=0xff0909)
                                await message.channel.send(embed=embed)

            except:
                embed=discord.Embed(title="❌ 오류 발생", description="단축에 오류가 발생하였습니다.",color=0xff0909)
                await message.channel.send(embed=embed)

        if message.content.startswith("봇 나무위키"):
            a = message.content
            a = a[7:]
            title = a
            a = "http://namu.wiki/w/" + a.replace(" ","%20")
            async with aiohttp.ClientSession() as session:
                async with session.get(a) as r:
                    if r.status == 404:
                        embed=discord.Embed(title="", description="없는 문서입니다.", color=0x1dc73a)
                        embed.set_author(name="문서를 찾을 수 없습니다.", icon_url="https://i.imgur.com/FLN2B5H.png")
                        await message.channel.send(embed=embed)
                    else:
                        data = await r.text()
                        soup = BeautifulSoup(data,"html.parser")
                        d = soup.find("div", {"class":"wiki-inner-content"}).text
                        content = htmltotext(d)[:150]
                        embed=discord.Embed(title="", description=content+"...", color=0x1dc73a)
                        embed.add_field(name="바로가기", value="[여기](%s)를 클릭하세요. " %(a))
                        embed.set_author(name=title, icon_url="https://i.imgur.com/FLN2B5H.png")
                        await message.channel.send(embed=embed)
    
        if message.content.startswith("봇 서버리스트"):
            
            a = ""
            user = 0
            server = []
            for s in self.client.guilds:
                a = a + "`" + s.name + "`" + "\n"
                user += s.member_count
                # embed.add_field(name="\n", value=s.name, inline=False)
            embed=discord.Embed(title="🗒 서버리스트", description=a, color=0x1dc73a)
            embed.set_footer(text="봇이 동작하는 서버는 %s개 입니다.\n중복 유저수는 %s명 입니다." %(str(len(self.client.guilds)),user))

            try:
                await message.author.send(embed=embed)
                embed=discord.Embed(title="✅ 서버리스트", description="DM 전송 완료!", color=0x1dc73a )
                await message.channel.send(embed=embed)
            except:
                embed=discord.Embed(title="❌ 오류 발생", description="DM 전송에 실패했습니다. 계정의 DM 설정을 확인해주세요.",color=0xff0909)
                await message.channel.send(embed=embed)

        if message.content.startswith("봇 프레타는?"):
            send = ["??? : 그말 꺼내지 마세요.", "???", "@.@", "불-편", "안사요"]
            await message.channel.send(random.choice(send))

        if message.content.startswith('봇 냥이') or message.content.startswith("봇 고양이"):
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
            await message.channel.send(embed=embed)

        if message.content.startswith('봇 강아지') or message.content.startswith("봇 댕댕이"):
            async with aiohttp.ClientSession() as session:
                    async with session.get("http://random.dog/woof.json") as r:
                        data = await r.json()
                        file = data["url"]
                        embed=discord.Embed(title=" ",color=0xf2e820)
                        embed.set_image(url=file)
                        embed.set_footer(text="http://random.dog")
                        await message.channel.send(embed=embed)

        if message.content.startswith("봇 네이버 실검") or message.content.startswith("봇 네이버 실시간검색어") or message.content.startswith("봇 네이버 실시간 검색어") or message.content.startswith("봇 네이버실검"):
            async with aiohttp.ClientSession() as session:
                    async with session.get("http://naver.com") as r:
                        c = await r.text()
                # s = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
                        now = time.localtime()
                        now = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

                        soup = BeautifulSoup(c,"html.parser")
                        embed=discord.Embed(title="✅ 네이버 실시간 검색어", description=now + " 기준 네이버 실시간 검색어입니다. \n\n　", color=0x1dc73a)
                        number = 0
                        for i in soup.find_all("span",{"class":"ah_k"}):
                            try:
                                number = number + 1
                                print(i.text)
                                
                                embed.add_field(name=str(number) + "위", value=i.text, inline=False)
                                if number == 10:
                                    break

                            except:
                                pass
                        await message.channel.send(embed=embed)


        if message.content.startswith("봇 다음 실검") or message.content.startswith("봇 다음 실시간검색어") or message.content.startswith("봇 다음 실시간 검색어") or message.content.startswith("봇 다음실검"):
            async with aiohttp.ClientSession() as session:
                    async with session.get("http://m.daum.net") as r:
                        c = await r.text()
                # s = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
                        now = time.localtime()
                        now = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

                        soup = BeautifulSoup(c,"html.parser")
                        soup = soup.find("ol",{"class":"list_issue #hotissue list_realtime"})
                        embed=discord.Embed(title="☑ 다음 실시간 검색어", description=now + " 기준 다음 실시간 검색어입니다. \n\n　", color=0x0089ff)
                        number = 0
                        for i in soup.find_all("span",{"class":"txt_issue"}):
                            try:
                                number = number + 1
                                print(i.text)
                                
                                embed.add_field(name=str(number) + "위", value=i.text, inline=False)
                                if number == 10:
                                    break

                            except:
                                pass
                        await message.channel.send(embed=embed)

        if message.content.startswith("봇 이 서버는?") or message.content.startswith("봇 서버정보"):
            number = 0
            date = "%s (UTC)"% message.guild.created_at
            for i in message.guild.members:
                number = number + 1
            sunsunumber = 0
            for i in message.guild.members:
                if i.bot == False:
                    sunsunumber = sunsunumber + 1
            s = message.guild
            if s.get_member(self.client.user.id).guild_permissions.administrator == False:
                clear = "정리 대상 입니다."

            else:

                clear = "정리 대상이 아닙니다."
                try:
                    welcome = message.guild.system_channel.name
                    if welcome == "" or welcome is None:
                        welcome = "존재하지 않습니다."
                except:
                    welcome = "존재하지 않습니다."
                
                embed=discord.Embed(title="ℹ️ 서버 정보", description="이 서버에 대한 정보를 불러왔습니다.\n\n" , color=0x1dc73a)
                embed.add_field(name="이름", value=message.guild.name, inline=False)
                embed.add_field(name="서버 ID", value=message.guild.id, inline=True)
                embed.add_field(name="서버 인원", value=number, inline=True)
                embed.add_field(name="순수 서버 인원 (봇 제외)", value=sunsunumber, inline=False)

                embed.add_field(name="서버 생성일", value=date, inline=True)
                embed.add_field(name="서버 오너", value=message.guild.owner, inline=False)
                embed.add_field(name="봇 정리 대상", value=clear, inline=True)
                embed.add_field(name="웰컴 채널", value="#" + welcome, inline=False)
                embed.add_field(name="서버 위치", value=message.guild.region, inline=True)

                embed.set_thumbnail(url=message.guild.icon_url)
                await message.channel.send(embed=embed)

        if message.content.startswith("봇 컵게임"):
            fstcup = random.randint(1,3)
            await message.channel.send("봇이 컵 3개를 섞습니다. 동전은 {}번 컵에 넣습니다...".format(fstcup))
            await asyncio.sleep(1)
            await message.channel.send("슥..슥..")
            await asyncio.sleep(1)
            await message.channel.send("쉭..쉭")
            await asyncio.sleep(1)
            await message.channel.send("슥삭..슥삭")
            lastcup = random.randint(1,3)
            await message.channel.send("동전은 1부터 3번 컵중에 어디에 있을까요?")
            def usercheck(a):
                return a.author == message.author
            try:
                cupinput = await self.client.wait_for('message', check=usercheck, timeout=10.0)
            except asyncio.TimeoutError:

                await message.channel.send("타임오버! 게임을 종료합니다.")
            lastcup1 = str(lastcup)
            a = cupinput.content
            if a.startswith(lastcup1):
                await message.channel.send("정답!\n당신이 승리하셨습니다!\n\n당신의 선택 : {}번\n동전의 위치 : {}번".format(a,lastcup))
            else:
                await message.channel.send("오답!\n당신이 패배하셨습니다!\n\n당신의 선택 : {}번\n동전의 위치 : {}번".format(a,lastcup))



        if message.content.startswith("봇 유저정보"):
            a = message.content
            a = a[7:]        
            if a == "":
                a = message.author.id
            try:
                a = a.replace("<", "")
                a = a.replace("@", "")
                a = a.replace("!", "")
                a = a.replace(">", "") 
                a = int(a)
            except:
                pass
            date = "%s (UTC)"% message.guild.get_member(a).created_at
            try:
                game = message.guild.get_member(a).activity.name
            except:
                game = "플레이 중인 게임이 없습니다."
            if game is None:
                game = "플레이 중인 게임이 없습니다."
            member =message.guild.get_member(a)
            status = message.guild.get_member(a).status
            joined = str(message.guild.get_member(a).joined_at)
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
            embed.add_field(name="이름", value=message.guild.get_member(a).name, inline=False)
            embed.add_field(name="유저 ID", value=message.guild.get_member(a).id, inline=True)
            embed.add_field(name="계정 생성일", value=date, inline=True)
            embed.add_field(name="서버 가입일", value=joined + " (UTC)", inline=False)
            
            embed.add_field(name="플레이 중", value=game, inline=True)
            embed.add_field(name="상태", value=status, inline=False)

            embed.set_thumbnail(url=asdf)
            await message.channel.send(embed=embed)



        if message.content.startswith("봇 멜론차트") or message.content.startswith("봇 맬론차트"):
            async with aiohttp.ClientSession() as session:
                async with session.get("https://music.cielsoft.me/api/getchart/melon") as r:
                    c = await r.text()
                    c = json.loads(c)
                    embed=discord.Embed(title="🎵 멜론 차트", description="멜론에서 TOP10 차트를 불러왔어요.",color=0x62bf42)
                    for i in range(11):
                        embed.add_field(name="TOP" + str(i+1),value=c[i]["title"] + " / " + c[i]["artist"])
                    await message.channel.send(embed=embed)


        if message.content.startswith("봇 질문"):
            response = ["절대 아닙니다.","잘 모르겠네요.","아마 아닐 것 같아요.","확실합니다.","네","아니오","그럴겁니다.","아마 맞을겁니다","무조건 맞을겁니다.","아닐겁니다"]
            a = random.choice(response)
            await message.channel.send(a)




        if message.content.startswith("봇 확률"):
            a = message.content[5:]
            per = random.randint(0,100)
            await message.channel.send("`%s` 은 `%s%%`입니다." %(a, per))



        if message.content.startswith("봇 날씨"):
            city = message.content[4:].lstrip()
            if city == "":
                embed=discord.Embed(title="⚠ 주의", description="도시가 정의되지 않았습니다.",color=0xd8ef56)
                await message.channel.send(embed=embed)

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
                                await message.channel.send(embed=embed)
                            elif r.status == 404:
                                embed=discord.Embed(title="⚠ 주의", description="선택하신 도시를 찾지 못했습니다. 다음을 시도해보세요:\n\n1. 지역명 뒤에 시, 광역시 붙이기 (`봇 날씨 부산광역시`)\n2. 주변에 있는 주요 도시로 재시도\n3. 영어로 해보기 (`봇 날씨 tokyo`)"
                                ,color=0xd8ef56)
                                await message.channel.send(embed=embed)


















        # if message.content.startswith('봇 재시작'):
        #     if message.author.id == 289729741387202560:

        #         try:
        #             embed=discord.Embed(title="봇 재시작", description="봇이 재시작 합니다.",color=0x237ccd )
        #             await message.channel.send(embed=embed)
        #             restart_bot()

        #         except Exception as error :
        #             embed=discord.Embed(title="❌ 경고", description="재시작 중 오류가 발생하였습니다. %s" %(error),color=0xff0909)
        #             await message.channel.send(embed=embed)
        #     else:
        #         embed=discord.Embed(title="⚠ 주의", description="봇 오너만 사용 가능한 명령어입니다.",color=0xd8ef56)
        #         await message.channel.send(embed=embed)

