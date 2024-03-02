import re

import discord
from discord import app_commands
from discord.ext.commands import Bot, Cog


class LinkChecker(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(name="linkchecker", description="リンクチェッカーをオン・オフします")
    async def switch(self, ctx: discord.Interaction):
        pass
        """setting = GuildSettings.get(ctx.guild_id)

        if not setting:
            GuildSettings.set_link_checker(ctx.guild_id, True)
            await ctx.response.send_message("リンクチェッカーをオンにしました", ephemeral=True)

        elif setting.link_checker:
            GuildSettings.set_link_checker(ctx.guild_id, False)
            await ctx.response.send_message("リンクチェッカーをオフにしました", ephemeral=True)

        else:
            GuildSettings.set_link_checker(ctx.guild_id, True)
            await ctx.response.send_message("リンクチェッカーをオンにしました", ephemeral=True)"""

    @Cog.listener()
    async def on_message(self, msg: discord.Message):
        """try:
            setting = GuildSettings.get(msg.guild.id)
        except AttributeError:
            return

        if not setting or not setting.link_checker:
            return"""

        if "pay.paypay.ne.jp" in msg.content or "qr.paypay.ne.jp" in msg.content:
            link_result = re.findall(r"\[(.*?)]\((https?://.*?)\)", msg.content)
            if len(link_result) != 0:
                fake_links = []
                not_pay_but_qr = []
                not_qr_but_pay = []
                safe_links = []

                for i in link_result:
                    if not i[1].startswith("https://pay.paypay.ne.jp/") and not i[1].startswith(
                            "https://qr.paypay.ne.jp/"):
                        fake_links.append(i[1])
                    elif "pay.paypay.ne.jp" in i[0] and i[1].startswith("https://qr.paypay.ne.jp"):
                        not_pay_but_qr.append(i[1])
                    elif "qr.paypay.ne.jp" in i[0] and i[1].startswith("https://pay.paypay.ne.jp"):
                        not_qr_but_pay.append(i[1])
                    else:
                        safe_links.append(i[1])

                if fake_links:
                    embed = discord.Embed(
                        title=":warning: 詐欺リンク",
                        description="このリンクはPayPayの送金リンクではありません",
                        color=discord.Color.red(),
                    )

                    content = ""
                    for link in fake_links:
                        content += f":x: 詐欺: `{link}`\n"
                    for link in not_pay_but_qr:
                        content += f":x: QRリンク: `{link}`\n"
                    for link in not_qr_but_pay:
                        content += f":question: 送金リンク: `{link}`\n"
                    for link in safe_links:
                        content += f":blue_circle: 正常 `{link}`\n"

                    embed.add_field(name="検証結果", value=content)

                elif not_pay_but_qr:
                    embed = discord.Embed(
                        title=":question: 不明リンク",
                        description="このリンクはテキストの送金リンクと一致していません",
                        color=discord.Color.red(),
                    )

                    content = ""
                    for link in not_pay_but_qr:
                        content += f":x: QRリンク: `{link}`\n"
                    for link in not_qr_but_pay:
                        content += f":question: 送金リンク: `{link}`\n"
                    for link in safe_links:
                        content += f":blue_circle: 正常 `{link}`\n"

                    embed.add_field(name="検証結果", value=content)

                elif not_qr_but_pay:
                    embed = discord.Embed(
                        title=":interrobang: 意味不明リンク",
                        description="乞食かと思いきや、ただの送金リンクです。意味不明。",
                        color=discord.Color.yellow(),
                    )

                    content = ""
                    for link in not_qr_but_pay:
                        content += f":question: 送金リンク: `{link}`\n"
                    for link in safe_links:
                        content += f":blue_circle: 正常 `{link}`\n"

                    embed.add_field(name="検証結果", value=content)

                else:
                    embed = discord.Embed(
                        title=":white_check_mark: 正常リンク",
                        description="安全性が確認できました",
                        color=3916277,
                    )

                    content = ""
                    for link in fake_links:
                        content += f":blue_circle: 正常: `{link}`\n"

                    embed.add_field(name="検証結果", value=content)
                await msg.reply(embed=embed, mention_author=False)

    @Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        channel = guild.channels[0]

