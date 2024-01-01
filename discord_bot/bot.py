"""
Controls the bot's actions that do not relate to posting loss.jpg images. This includes
handling new servers and altering channel registration.

If this script is not running when the bot joins a server, then the bot will not send images in that
server. An admin would have to manually invoke /losschannel to set the channel.
"""
import discord, time, os, calendar, json
import db

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"Main bot logged in as {bot.user}")

    # Set custom status
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Activity(type=discord.ActivityType.listening,
                                                        name="/setchannel"))

    servers = get_new_servers()

    for server in servers:
        pass

@bot.event
async def on_guild_join(guild: discord.Guild):
    print(f"Joined guild {guild.id}")

    for channel in guild.channels:
        if can_send_in_channel(channel):
            db.register_loss_channel(guild.id, channel.id)
            break

@bot.slash_command(name="setchannel",
                   description="Sets the channel for loss.jpg images.")
async def new_losschannel(
    ctx: discord.ApplicationContext,
    channel: discord.Option(discord.TextChannel, "The channel to send images in.", required=True)
):
    if not ctx:
        return
    await ctx.defer()

    # Check if the bot has send permissions for this command
    if can_send_in_channel(channel):
        db.register_loss_channel(ctx.guild_id, channel.id)
        await ctx.respond(":thumbsup:")
    else:
        await ctx.respond("I can't send messages in that channel! Please adjust permissions or"\
                          " choose another channel.")

def get_new_servers() -> list[discord.Guild]:
    """
    Get all servers the bot has joined since it went offline last.
    """
    if not os.path.exists("./stoptime.txt"):
        return []

    with open("stoptime.txt") as f:
        stoptime = float(f.read())

    new_servers = []

    for g in bot.guilds:
        dt = g.me.joined_at
        if dt is not None:
            timestamp = calendar.timegm(dt.timetuple())

            if timestamp > stoptime:
                new_servers.append(g)

    return new_servers

def can_send_in_channel(channel: discord.TextChannel):
    return type(channel) is discord.TextChannel and channel.can_send(discord.File("requirements.txt"))

def load_secrets() -> dict:
    """
    Loads all the secrets from secrets.json into a dict object.

    Returns:
        A dict containing all the secrets.
    """
    with open("../secrets.json") as f:
        return json.load(f)

if __name__ == "__main__":
    secrets = load_secrets()["discord"]
    db.init(secrets["bot-db-connection"])
    bot.run(secrets["bot-token"])

    # Record when the bot stopped
    with open("stoptime.txt", "w") as f:
        f.write(str(time.time()))