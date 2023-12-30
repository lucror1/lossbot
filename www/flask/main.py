from flask import Flask, render_template, send_from_directory, redirect
import os, datetime

_IMG_LIST = "./img_list.txt"
_IMG_FOLDER = "./img"

app = Flask(__name__)

@app.get("/")
def index():
    return render_template("index.html", date=datetime_to_str(datetime.datetime.now()))

@app.get("/archive")
def archive():
    # Construct dates for images
    start_date = datetime.datetime(2024, 1, 1)
    dates = [start_date + datetime.timedelta(days=i) for i in range(get_current_index()+1)]
    dates = [datetime_to_str(d) for d in dates]

    return render_template("archive.html", dates=dates)

@app.get("/about")
def about():
    return render_template("about.html")

@app.get("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"), "favicon.ico",
                               mimetype="image/vnd.microsoft.icon")

@app.get("/loss.jpg")
def daily_loss():
    img_path = get_current_image()
    return send_from_directory(os.path.dirname(img_path), os.path.basename(img_path),
                               mimetype="image/jpeg")

@app.get("/img/<int:index>/loss.jpg")
def index_loss(index: int):
    # Prevent early access to images
    if index > get_current_index():
        return render_template("forbidden.html"), "403 Forbidden"

    img_path = get_image_by_index(index)
    return send_from_directory(os.path.dirname(img_path), os.path.basename(img_path),
                               mimetype="image/jpeg")

@app.get("/sneakpeek")
def sneakpeek():
    return redirect("https://youtu.be/dQw4w9WgXcQ")

def get_current_index() -> int:
    """
    Gets the current index for today's image. This is also the maximum allowable index.

    Returns:
        The index for today's image.
    """
    # Calculate the number of days that have passed
    # TODO: replace with New Year's date
    start_date = datetime.datetime(2023, 12, 29, 0, 0, 0, 0)
    now = datetime.datetime.now()
    return (now - start_date).days

def get_current_image() -> str:
    """
    Gets the current image for today and returns and absolute path to it.

    Returns:
        An absolute path to today's image.
    """
    day_index = get_current_index()

    # Read the image paths in
    with open(_IMG_LIST) as f:
        imgs = f.readlines()

    # Get the current image, looping if necessary
    f = imgs[day_index % len(imgs)].strip()
    return os.path.join(_IMG_FOLDER, f)

def get_image_by_index(index: int) -> str|None:
    """
    Gets the image corresponding with the specified index.

    Args:
        index: The index of the image that should be retrieved.

    Returns:
        An absolute path to the image with that index or None if no such image exists.
    """
    with open(_IMG_LIST) as f:
        for _ in range(index+1):
            img = f.readline()
    return os.path.join(_IMG_FOLDER, img.strip())

def get_images_in_range(start_index: int, end_index: int) -> list[str]:
    """
    Returns a list of absolute paths to images in the specified range.

    Args:
        start_index: The index to start getting images at. Included in the returned list.
        end_index: The index to stop getting images at. Included in the returned list.
    """
    imgs = []
    with open(_IMG_LIST) as f:
        i = 0
        for path in f.readlines():
            if i >= start_index and i <= end_index:
                imgs.append(path.strip())
            i += 1
    return imgs

def datetime_to_str(dt: datetime.datetime) -> str:
    """
    Converts a datetime to a string of the format "%A, %B %-d, %Y".
    """
    return dt.strftime("%A, %B ") + dt.strftime("%d").removeprefix("0") + dt.strftime(", %Y")

if __name__ == "__main__":
    app.run()
