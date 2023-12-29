"""
Responsible for sending images. It should be executed once daily using systemd, cron,
or some other scheduling tool.
"""
import discord
import discord_bot.util as util, discord_bot.db as db

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"Daily bot logged in as {bot.user}")

    file = util.consume_random_image()
    print(file)
    if file is None:
        return  # No images are available, don't send anything

    channels = db.get_all_channel_ids()
    print(channels)

    for channel_id in channels:
        channel = bot.get_channel(channel_id)
        msg = discord.File(file)
        try:
            await channel.send(file=msg)
        except discord.errors.Forbidden as e:
            # Permissions got messed up for this channel
            # TODO: should this channel be removed from the db?
            # Maybe increment some kind of fail counter? If too many fails, remove?
            print("Forbidden")
            print(e)
            pass
        except Exception as e:
            print("Other error")
            print(e)
            # Don't prevent the other messages from sending
            pass

    print(f"Daily bot completed task")
    await bot.close()

def run(secrets: dict):
    db.init(secrets["db-connection"])
    bot.run(secrets["bot-token"])

if __name__ == "__main__":
    secrets = util.load_secrets()
    run(secrets["discord"])