"""
Responsible for sending images. It should be executed once daily using systemd, cron,
or some other scheduling tool.
"""
import discord
import discord_bot.db as db

bot = discord.Bot()
file = ""

@bot.event
async def on_ready():
    if file is None:
        return  # No images are available, don't send anything

    channels = db.get_all_channel_ids()

    for channel_id in channels:
        channel = bot.get_channel(channel_id)
        msg = discord.File(file)
        try:
            await channel.send(file=msg)
        except discord.errors.Forbidden as e:
            # Permissions got messed up for this channel
            # TODO: should this channel be removed from the db?
            # Maybe increment some kind of fail counter? If too many fails, remove?
            # At least check if the bot is not in the server anymore and remove it from the db if so
            print(e)
        except Exception as e:
            print(e)

    await bot.close()

def run(image: str, secrets: dict, date: str):
    global file
    file = image

    db.init(secrets["db-connection"])
    bot.run(secrets["bot-token"])