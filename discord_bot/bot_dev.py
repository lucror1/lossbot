"""
Testing site for adding new bot commands without interfering with the existing bot.

All commands in this file should only be enabled on specific guilds.
"""

import discord
from bot import load_secrets
import db

bot = discord.Bot()

#              Gorb's Dev Server  , Gorb's Other Dev Server
dev_servers = [1189990166396407888, 1191442923062054973]

@bot.event
async def on_ready():
    print(f"Dev bot logged in as {bot.user}")

    for g in bot.guilds:
        print(g)

if __name__ == "__main__":
    secrets = load_secrets()["discord"]
    db.init(secrets["dev-db-connection"])
    bot.run(secrets["dev-bot-token"])
