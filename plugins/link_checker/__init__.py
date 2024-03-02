from discord.ext.commands import Bot

from plugins.link_checker.checker import LinkChecker


def setup(bot: Bot):
    return bot.add_cog(LinkChecker(bot))
