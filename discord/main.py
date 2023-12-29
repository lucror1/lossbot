import discord
import util, db

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"Main bot logged in as {bot.user}")

@bot.event
async def on_guild_join(guild: discord.Guild):
    print(f"Joined guild {guild.id}")

    for channel in guild.channels:
        if type(channel) is discord.TextChannel and channel.can_send(discord.File("../requirements.txt")):
            db.register_loss_channel(guild.id, channel.id)
            break

@bot.slash_command(name="losschannel",
                   description="Sets the channel for loss.jpg images to the current channel.")
@discord.default_permissions(administrator=True)
async def set_image_channel(ctx: discord.commands.context.ApplicationContext):
    db.register_loss_channel(ctx.guild_id, ctx.channel_id)
    await ctx.respond(":thumbsup:")

""" @bot.slash_command(guild_ids=[1189990166396407888])
@discord.default_permissions(administrator=True)
async def debug(ctx: discord.commands.context.ApplicationContext):
    if ctx.author.id == 465897773007634442:
        # Ensure nothing times out
        await ctx.defer()

        file = util.consume_random_image()
        if file is None:
            await ctx.followup.send("No images are available.")
        else:
            await ctx.followup.send(file=discord.File(file))

        #await ctx.followup.send("OK")
    else:
        await ctx.respond("Nice try") """

if __name__ == "__main__":
    secrets = util.load_secrets()
    db.init(secrets["db-connection"])
    bot.run(secrets["bot-token"])