"""
A set of utility functions.
"""
import os
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

if __name__ == "__main__":
    strip_exif("./img/in", "./out")