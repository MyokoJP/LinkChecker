from discord.ext.commands import Bot

from plugins.status.status import Status


def setup(bot: Bot):
    return bot.add_cog(Status(bot))
