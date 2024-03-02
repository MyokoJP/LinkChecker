import discord
from discord.ext import tasks
from discord.ext.commands import Bot, Cog


class Status(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.playing = 0

        self.switch_status.start()

    @tasks.loop(seconds=10)
    async def switch_status(self):

        if self.playing == 0:
            count = 0
            for i in self.bot.guilds:
                count += i.member_count

            await self.bot.change_presence(
                activity=discord.Game(name=f"{len(self.bot.guilds)} サーバー | {count} メンバー"))
            self.playing = 1
        else:
            await self.bot.change_presence(activity=discord.Game(name=f"By UTA SHOP"))
            self.playing = 0
