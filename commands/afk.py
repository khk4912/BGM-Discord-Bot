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
import datetime 

from send import Command

'''
AFK 부분을 담당합니다.
'''


''' Function '''

''' Main ''' 
class afk(Command):

    def __init__(self, *args, **kwargs):
        Command.__init__(self, *args, **kwargs)
        self.afk = {}

    async def on_message(self, message):


        if message.author.id in self.afk.keys():
            
            get = self.afk[message.author.id]
            embed=discord.Embed(title="👐 잠수 종료!", description="<@{}>님이 잠수를 종료하셨습니다.".format(message.author.id), color=get["color"])
            embed.add_field(name="잠수 사유", value="{0}".format(get["reason"]), inline=True)
            embed.add_field(name="잠수했던 시각", value="{0}".format(get["when"]), inline=True)
            del self.afk[message.author.id]
            await message.channel.send(embed=embed)


        if message.content.startswith("봇 잠수") or message.content.startswith("봇 afk"):
            msg = message.content
            msg = msg.replace("봇 잠수", "")
            msg = msg.replace("봇 afk", "")
            reason = msg.lstrip()
            if reason == "" : reason = "사유가 없습니다."
            try:
                authorcolor = message.author.colour
            except:
                authorcolor = 0x237ccd
            now = datetime.datetime.now()
            self.afk[message.author.id] = {"reason" : reason, "when" : now, "color"  : authorcolor}
            embed=discord.Embed(title="💤 잠수", description="<@{0}>님이 잠수를 시전하셨습니다.\n".format(message.author.id), color=authorcolor)
            embed.add_field(name="잠수 사유", value="{0}".format(reason), inline=False)
            embed.set_footer(text="{0}\n".format(now))
            await message.channel.send(embed=embed)
