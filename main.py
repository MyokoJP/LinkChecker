from pathlib import Path

import discord
from discord.ext import commands

import config

bot = commands.Bot(intents=discord.Intents.all(), command_prefix=[])


@bot.event
async def on_ready():

    await load_extensions()
    await bot.tree.sync()

    print(f"{bot.user} としてログインしました")
    print("同期が完了しました")


async def load_extensions():
    names = []

    plugins_dir = Path("plugins")
    plugins_dir.mkdir(exist_ok=True)

    for child in plugins_dir.iterdir():

        if child.name.startswith("_"):
            continue

        if child.is_file() and child.suffix == ".py":
            name = child.name.split(".")[0]
            await bot.load_extension(f"plugins.{name}")
            names.append(name)

        elif child.is_dir():
            name = child.name
            await bot.load_extension(f"plugins.{name}")
            names.append(name)

    print(f"ロード完了 plugins({len(names)}):", ", ".join(names))


bot.run(config.TOKEN)
