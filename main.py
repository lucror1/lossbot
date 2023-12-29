"""
Manages all daily loss services. All services must contain a "main.py" file with a "run" function.
"""
import os, shutil, random, json
from discord_bot import main as discord_main

_IMG_SRC = "./img/in"
_IMG_DST = "./img/out"

def consume_random_image() -> str|None:
    """
    Returns the path to a random image, moving it from _IMG_SRC to _IMG_DST.

    Also ensures that there is always a valid image that can be consumed, if possible. This is not
    possible if there are no images in either _IMG_SRC or _IMG_DST.

    Returns:
        An absolute path to the consumed image or None if no images can be found.
    """
    # Ensure there are some input images
    if _count_files(_IMG_SRC) == 0:
        _move_all_files(_IMG_DST, _IMG_SRC)

    # Get a random image
    file = _get_random_file(_IMG_SRC)

    # If the file is None, there are no images available
    if file is None:
        return None

    # Ensure no duplicate images until all images are sent
    _move_file(file, _IMG_DST)

    basename = os.path.basename(file)
    return os.path.abspath(os.path.join(_IMG_DST, basename))

def _load_secrets() -> dict:
    """
    Loads all the secrets from secrets.json into a dict object.

    Returns:
        A dict containing all the secrets.
    """
    with open("./secrets.json") as f:
        return json.load(f)

def _count_files(folder: str) -> int:
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

def _move_file(file: str, dst: str) -> None:
    """
    Moves the specified file to the specified directory.

    Args:
        file: The file to move.
        dst: The directory to move the file to.

    Raises:
        FileNotFoundError: Either file or dst does not exist.
    """
    shutil.move(file, dst)

def _move_all_files(src: str, dst: str) -> None:
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

def _get_random_file(folder: str) -> str|None:
    """
    Gets a random file in the specified directory.

    Args:
        folder: The directory to get the image from.

    Returns:
        The relative path to a random image in the directory or None if no files exist.

    Raises:
        FileNotFoundError: The specified folder does not exist.
    """
    num_files = _count_files(folder)

    if num_files == 0:
        return None

    file_index = random.randrange(0, num_files)
    return os.path.join(folder, os.listdir(folder)[file_index])

if __name__ == "__main__":
    secrets = _load_secrets()
    
    discord_main.run(secrets["discord"])