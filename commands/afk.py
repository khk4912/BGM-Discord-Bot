import discord
from discord.ext import commands
import datetime 

afk = {}


class Afk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot





def setup(bot):

    # @bot.event
    # async def on_message(message):
        
    bot.add_cog(Afk(bot))