import discord


class Embed:
    @classmethod
    def check(cls, title=None, description=None) -> discord.Embed:
        embed = discord.Embed(
            title="✅ {}".format(title),
            description="{}".format(description),
            color=0x1DC73A,
        )
        return embed

    @classmethod
    def warn(cls, title=None, description=None) -> discord.Embed:
        embed = discord.Embed(
            title="⚠ {}".format(title),
            description="{}".format(description),
            color=0xD8EF56,
        )
        return embed

    @classmethod
    def error(cls, title=None, description=None) -> discord.Embed:
        embed = discord.Embed(
            title="❌ {}".format(title),
            description="{}".format(description),
            color=0xFF0909,
        )
        return embed
