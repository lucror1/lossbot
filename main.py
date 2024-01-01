"""
Manages all daily loss services. All services must contain a "main.py" file with a "run" function.
"run" must have the signature run(image: str, secrets: dict, date: str), where image is a relative
path to the image to post, secrets is a dict of any secrets necessary for the application, and date
is the current date formated as a string.
"""
import json, datetime, os
from discord_bot import main as discord_main
from mastodon_bot import main as mastodon_main
from bluesky_bot import main as bluesky_main

_IMG_LIST = "./img_list.txt"
_IMG_FOLDER = "./img"

def consume_random_image() -> str|None:
    """
    Returns the path to a random image.

    Returns:
        A relative path to the consumed image or None if no images can be found.
    """
    # Calculate the number of days that have passed
    start_date = datetime.datetime(2024, 1, 1)
    now = datetime.datetime.now()
    num_days = (now - start_date).days

    # Read the image paths in
    with open(_IMG_LIST) as f:
        imgs = f.readlines()

    # Get the current image, looping if necessary
    f = imgs[num_days % len(imgs)].strip()
    return os.path.join(_IMG_FOLDER, f)

def datetime_to_str(dt: datetime.datetime) -> str:
    """
    Converts a datetime to a string of the format "%A, %B %-d, %Y".
    """
    return dt.strftime("%A, %B ") + dt.strftime("%d").removeprefix("0") + dt.strftime(", %Y")

def _load_secrets() -> dict:
    """
    Loads all the secrets from secrets.json into a dict object.

    Returns:
        A dict containing all the secrets.
    """
    with open("./secrets.json") as f:
        return json.load(f)

if __name__ == "__main__":
    secrets = _load_secrets()

    now = datetime_to_str(datetime.datetime.now())
    image = consume_random_image()

    mastodon_main.run(image, secrets["mastodon"], now)
    bluesky_main.run(image, secrets["bluesky"], now)
    discord_main.run(image, secrets["discord"], now)