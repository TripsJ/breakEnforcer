import http.client
import requests  # Make webrequests to apis
from tkinter import *
from PIL import Image, ImageTk, ImageShow, ImageGrab, UnidentifiedImageError
from timer import Timer


def get_input():
    target_time: str = input("When should the timer go off? ")
    try:
        h, m = target_time.lower().split("h")
        hours: int = int(h)
        minutes: int = int(m)

    except Exception as e:
        error(e)
    else:
        return hours, minutes


# TODO: make this not freeze the whole thing while counting down


def get_json_nasa(apikey: str = "DEMO_KEY"):
    """Grab image description from the nasa Astronomy image of the day, parse the returned json and return it as a dict. If Errors Occure, return the status code"""
    response = requests.get(
        "https://api.nasa.gov/planetary/apod", params={"api_key": apikey, "count": 1}
    )
    try:
        # raises HTTPError if requst was unsuccessfull
        response.raise_for_status()
        # the api sends a list of Json back as it could very well contain multiple images, However this request is structured to return
        return response.json()[0]
    except requests.HTTPError:
        return response.status_code


def cache_image(imageinfo: dict):
    if type(imageinfo) == dict:
        filename = imageinfo["url"].split("/")[-1]
        imagedata = requests.get(imageinfo["url"])
        with open(filename, "wb") as f:
            # the mode wb stands for write and binary, wich is relevant on Windows as it distinguishes between text and nontext files.
            # cf https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files
            f.write(imagedata.content)
        return filename
    else:
        return imageinfo


def get_image_offline():
    """Get random image from a set of local folders return path to that image"""
    return None


def get_monitor_size():
    monitor = ImageGrab.grab()
    return monitor.size


def resize_image(input_filename: str, resolution: tuple):
    with Image.open(input_filename) as im:
        im = im.resize(resolution)
        im.save(f"resized_{input_filename}")
    return f"resized_{input_filename}"


def check_connection() -> bool:
    conn = http.client.HTTPConnection(
        "www.google.com"
    )  # Testing against googles dns address
    try:
        conn.request(
            "HEAD", "/"
        )  # No need to download anything so limmiting the request to only get the Head
        return True
    except:
        return False  # In case of exception return False


def display_image(image, res):
    """display an Image"""
    try:
        root = Tk()
        root.minsize(res[0], res[1])
        im = Image.open(image)
        tkim = ImageTk.PhotoImage(im)
        label1 = Label(image=tkim)
        label1.image = tkim
        label1.pack()
    except UnidentifiedImageError:
        print("an error occured")

    return root


def error(exception: Exception):
    """handle Exceptions according to their nature"""
    print("Something went Wong")


def main():
    roundtimer = Timer()
    roundtimer.duration = "00:02"
    breaktime = 60000
    roundtimer.set_timer()
    print(roundtimer)

    if check_connection():
        info = get_json_nasa()
        image = cache_image(info)
        print(image)
    else:
        print("You are disconnected")

    roundtimer.run()
    resolution = get_monitor_size()
    resized_img = resize_image(image, resolution)
    window = display_image(resized_img, resolution)

    window.after(breaktime, window.destroy)
    window.mainloop()


if __name__ == "__main__":
    main()
