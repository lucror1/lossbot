import os, shutil, random, json, discord

bot = discord.Bot()

def load_secrets() -> dict:
    """
    Loads all the secrets from secrets.json into a dict object.

    Returns:
        A dict containing all the secrets.
    """
    with open("secrets.json") as f:
        return json.load(f)

def count_files(folder: str) -> int:
    """
    Counts the number of files in the specified directory.

    Args:
        folder: The directory to count files in.

    Returns:
        The number of files (excluding directories) present in the directory.

    Raises:
        FileNotFoundError: The specified path does not exist.
    """
    files = os.listdir(folder)
    files = [f for f in files if os.path.isfile(os.path.join(folder, f))]
    return len(files)

def move_file(file: str, dst: str) -> None:
    """
    Moves the specified file to the specified directory.

    Args:
        file: The file to move.
        dst: The directory to move the file to.

    Raises:
        FileNotFoundError: Either file or dst does not exist.
    """
    shutil.move(file, dst)

def move_all_files(src: str, dst: str) -> None:
    """
    Moves all the files from the src directory to the dest directory.

    Args:
        src: The directory to move files from.
        dst: The directory to move files to. May be eitehr a relative or absolute path.

    Raises:
        FileNotFoundError: Either src or dst does not exist.
    """
    for f in os.listdir(src):
        shutil.move(os.path.join(src, f), dst)

def get_random_file(folder: str) -> str|None:
    """
    Gets a random file in the specified directory.

    Args:
        folder: The directory to get the image from.

    Returns:
        The relative path to a random image in the directory or None if no files exist.

    Raises:
        FileNotFoundError: The specified folder does not exist.
    """
    num_files = count_files(folder)

    if num_files == 0:
        return None

    file_index = random.randrange(0, num_files)
    return os.path.join(folder, os.listdir(folder)[file_index])

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(name="losschannel",
                   description="Sets the channel for loss.jpg images to the current channel.",
                   guild_ids=[1189990166396407888])
@discord.default_permissions(administrator=True)
async def set_image_channel(ctx: discord.commands.context.ApplicationContext):
    await ctx.respond("OK")

@bot.slash_command(guild_ids=[1189990166396407888])
@discord.default_permissions(administrator=True)
async def debug(ctx: discord.commands.context.ApplicationContext):
    if ctx.author.id == 465897773007634442:
        # Ensure nothing times out
        await ctx.defer()

        # Ensure there are some input images
        if count_files("./img/in") == 0:
            move_all_files("./img/out", "./img/in")

        # Get a random image
        file = get_random_file("./img/in")

        # If the file is None, there are no images available
        if file is None:
            await ctx.followup.send("No images are available.")
        else:
            await ctx.followup.send(file=discord.File(file))

            # Ensure no duplicate images until all images are sent
            move_file(file, "./img/out")
    else:
        await ctx.respond("Nice try")

if __name__ == "__main__":
    secrets = load_secrets()
    bot.run(secrets["bot-token"])