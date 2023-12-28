import os, shutil, random

# TODO: add "Raises" to functions as needed

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

if __name__ == "__main__":
    # Ensure there are some input images
    if count_files("./img/in") == 0:
        move_all_files("./img/out", "./img/in")

    # Get a random image
    file = get_random_file("./img/in")

    # If the file is None, there are no images available
    if file is not None:
        # Ensure no duplicate images until all images are sent
        move_file(file, "./img/out")
