"""
A set of utility functions.
"""
import os, random
from PIL import Image

def validate_images():
    """
    Check if any images could not be posted to a platform.
    """

    for folder in ["./img/in", "./img/out"]:
        for f in os.listdir(folder):
            path = os.path.join(folder, f)

            reason = _check_bluesky(path)
            if reason:
                print(f"{os.path.basename(path)}: {reason}")

def strip_exif(in_folder: str, out_folder):
    """
    Remove all exif data from images in the specified folder.

    Args:
        in_folder: The folder containing images to remove exif data from.
        out_folder: The folder converted images should be placed in.
    """
    for f in os.listdir(in_folder):
        path = os.path.join(in_folder, f)

        image = Image.open(path)

        # Strip data
        data = list(image.getdata())
        image_without_exif = Image.new(image.mode, image.size)
        image_without_exif.putdata(data)

        image_without_exif.save(os.path.join(out_folder, f))
        image_without_exif.close()

def _check_bluesky(path: str) -> str|None:
    """
    Checks if the specified file could be posted on Bluesky.

    Args:
        path: The path to the image to check.

    Returns:
        The reason that the image is invalid or None if the image is valid.
    """
    with open(path, "rb") as f:
        file_bytes = f.read()
        if len(file_bytes) > 1000000:
            return f"[BSKY] File is too big. ({len(file_bytes)} of 1000000)"

def generate_image_list(img_folder: str, out_file: str):
    """
    Generates a random list of images and saves them to out_file, one per line. If the file already
    exists, then the order of the included images will be preserved.

    Args:
        img_folder: The path to the folder that contains the images.
        out_file: The path to where the randomized list should be saved.
    """
    imgs = []

    # Load existing images if possible
    if os.path.exists(out_file):
        with open(out_file) as f:
            imgs = [i.strip() for i in f.readlines()]

    # Get all the images in img_folder not in out_file
    new_imgs = []
    for f in os.listdir(img_folder):
        #path = os.path.abspath(os.path.join(img_folder, f))
        if f not in imgs:
            new_imgs.append(f)

    # Shuffle the new images
    random.shuffle(new_imgs)

    # Write everything to disk
    with open(out_file, "w") as f:
        for img in imgs + new_imgs:
            f.write(img + "\n")

def convert_to_jpg(img_folder: str, out_folder: str, extensions: list[str]=["png", "webp"]):
    """
    Converts all non-jpg images in img_folder into jpgs and saves them to out_folder. Only considers
    files with extensions in the extensions list.

    Args:
        img_folder: The folder containing images to be converted.
        out_folder: The folder where converted images will be saved.
        extensions: An array of extensions to convert.
    """
    for f in os.listdir(img_folder):
        ext = f.split(".")[-1]
        if ext not in extensions:
            continue

        im = Image.open(os.path.join(img_folder, f))
        rgb_im = im.convert("RGB")
        rgb_im.save(os.path.join(out_folder, f.removesuffix(ext) + "jpg"))

if __name__ == "__main__":
    generate_image_list("./img/in", "./img_list.txt")