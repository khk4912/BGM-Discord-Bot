import discord
from discord.ext import commands
import datetime

class Uptime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_start_time = datetime.datetime.utcnow()


    @commands.command(name="업타임")
    async def uptime(self, ctx):

        uptime = datetime.datetime.utcnow() - self.bot_start_time

        day = uptime.days
        day = str(day)

        uptime = str(uptime)
        uptime = uptime.split(":")

        hours = uptime[0]

        hours = hours.replace(" days,", "일")
        hours = hours.replace(" day,", "일")

        minitues = uptime[1]

        seconds = uptime[2]
        seconds = seconds.split(".")
        seconds = seconds[0]

        embed = discord.Embed(title="🕐 업타임", description="봇이 꺼지지 않고 동작한 시간은  %s시간 %s분 %s초 입니다." % (hours, minitues, seconds), color=0x237ccd,
                              timestamp=self.bot_start_time)
        embed.set_footer(text="봇 시작 시각")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Uptime(bot))