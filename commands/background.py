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

'''
봇이 작동중에 사용할 백그라운드 태스크를 사용합니다.
'''

async def change_activity(self):
    await self.wait_until_ready()
    while not self.is_closed():

        number = 0
        user = 0

        for s in self.guilds:
            number = number + 1

            if not s.unavailable:
                user += s.member_count
        await self.change_presence(activity=discord.Game(name="%s개의 서버 / %s Servers"%(number,number)))
        await asyncio.sleep(30)
        await self.change_presence(activity=discord.Game(name="%s명의 유저 / %s Users"%(user, user)))
        await asyncio.sleep(30)
        await self.change_presence(activity=discord.Game(name="`봇 도움` 명령어를 사용해보세요!"))
        await asyncio.sleep(30)

