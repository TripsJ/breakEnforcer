import http.client
import os
import random
import sys
from tkinter import *

import requests  # Make webrequests to apis
from PIL import Image, ImageGrab, ImageShow, ImageTk, UnidentifiedImageError

from configurator import Configurator
from InvalidFileError import InvalidFileError


## Getting configuration
def get_conf():
    try:
        c = Configurator()
        return c.read_configfile()
    except InvalidFileError:
        print(
            """the specified file is invalid
            Now loading default configuration and saving it to file"""
        )
        return rebuild_config()
    except FileNotFoundError:
        print("the specified file was not Found")
        return rebuild_config()


def rebuild_config():
    c = Configurator()
    c.write_configfile()
    return c.configuration


def get_monitor_size():
    monitor = ImageGrab.grab()
    return monitor.size


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


##Getting Image info from Nasa api or cache


def get_json_nasa(apikey: str = "DEMO_KEY"):
    # handle timeout
    """Grab image description from the nasa Astronomy image of the day, parse the returned json and return it as a dict. If Errors Occure, return the status code"""
    response = requests.get(
        "https://api.nasa.gov/planetary/apod", params={"api_key": apikey, "count": 1}
    )
    try:
        # raises HTTPError if requst was unsuccessfull
        response.raise_for_status()
        # the api sends a list of Json back as it could very well contain multiple images. Requests from this api however, contain one url to an image.²
        # print(response.json()[0])
        if response.json()[0]["media_type"] == "image":
            return response.json()[0]
        else:
            print("received video, retrying")
            get_json_nasa(apikey)

    except requests.HTTPError:
        print(response.status_code)
        sys.exit()


def cache_image(imageinfo: dict, configuration: dict):
    if type(imageinfo) == dict:
        # Catch key error
        if targetpath := configuration.get("storage", {}).get("path"):
            filename = f'{targetpath}/{imageinfo["url"].split("/")[-1]}'
        else:
            filename = imageinfo["url"].split("/")[-1]

        imagedata = requests.get(imageinfo["url"])
        with open(filename, "wb") as f:
            # the mode wb stands for write and binary, wich is relevant on Windows as it distinguishes between text and nontext files.
            # cf https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files
            f.write(imagedata.content)
        return filename
    else:
        return imageinfo


def get_image_offline(configuration: dict):
    if targetpath := configuration.get("storage", {}).get("path"):
        if os.path.isdir(os.path.join(targetpath, "resized")):
            return random.choice(os.listdir(os.path.join(targetpath, "resized")))

    raise FielNotFoundError


def resize_image(input_filename: str, resolution: tuple, configuration: dict):
    try:
        with Image.open(input_filename) as im:
            im = im.resize(resolution)

            if targetpath := configuration.get("storage", {}).get("path"):
                if not os.path.isdir(os.path.join(targetpath, "resized")):
                    os.mkdir(os.path.join(targetpath, "resized"))
                im.save(f"{targetpath}/resized/resized_{input_filename.split('/')[-1]}")
                return f"{targetpath}/resized/resized_{input_filename.split('/')[-1]}"

            else:
                if not os.path.isdir("resized"):
                    os.mkdir("resized")
                im.save(f"resized/resized_{input_filename}")
                return f"resized/resized_{input_filename}"
    except UnidentifiedImageError:
        print("image invalid")
        try:
            return get_image_offline(configuration)
        except FileNotFoundError:
            print("unfortunately this file was not found /n Terminating")
            sys.exit()


def display_image(image, res, duration):
    """display an Image"""
    try:
        frame = Tk()
        frame.minsize(res[0], res[1])
        im = Image.open(image)
        tkim = ImageTk.PhotoImage(im)
        label1 = Label(image=tkim)
        label1.image = tkim
        label1.pack()
        frame.after(converttoms(duration), frame.destroy)
    except UnidentifiedImageError:
        print("an error occured")
    except FileNotFoundError:
        print("unfortunately this file was not found /n Terminating")
        sys.exit()
    return frame


### TIMER Functions


def converttoms(duration):
    if isinstance(duration, int):
        return duration * 60 * 1000

    if "h" in duration:
        splitchar = "h"
    elif ":" in duration:
        splitchar = ":"
    else:
        return 0
    sh, sm = duration.split(splitchar)
    h = int(sh)
    m = int(sm) + (h * 60)
    return m * 60 * 1000


def converttoclock(countdown):
    seconds = (countdown / 1000) % 60
    seconds = int(seconds)
    minutes = (countdown / (1000 * 60)) % 60
    minutes = int(minutes)
    hours = (countdown / (1000 * 60 * 60)) % 24
    return "%d:%d:%d" % (hours, minutes, seconds)


def turn(configuration, resized_img, resolution, currentround):
    duration: str = "0h:0m"
    countdown: int = -1
    global running
    running = True

    pause = configuration["breaks"]["short"]
    duration = configuration["work"]["interval"]
    countdown = converttoms(duration) / 1000
    root = Tk()
    clock = converttoclock(converttoms(duration))
    lable = Label(root, text=clock)
    startbtn = Button(
        root,
        text="Start",
        font=("Arial", 15),
        command=lambda: [
            startbtn.config(state=DISABLED),
            run(countdown, resized_img, resolution),
        ],
    )
    pausebtn = Button(
        root,
        text="Pause",
        font=("Arial", 15),
        command=lambda: [
            interrupt_count(),
        ],
    )

    def interrupt_count():
        global running
        running = not running

    def run(
        countdown,
        resized_image,
        resolution,
    ):
        global running
        print(running)
        c = StringVar()

        if countdown == 0:
            root.destroy()
            display_image(resized_img, resolution, pause)
            return
        if countdown < 0:
            print("please set timer first")
            return

        if running:
            c.set(
                converttoclock(countdown * 1000)
            )  # the countdown is in seconds but the conversion in ms so *1000
            lable.config(textvariable=c)
            # check for break
            # While running:
            countdown -= 1
        lable.after(
            1000,
            run,
            countdown,
            resized_img,
            resolution,
        )

    if currentround > 0:
        startbtn.invoke()

    lable.pack(anchor="center")
    startbtn.pack(padx=20, pady=20)
    pausebtn.pack(padx=20, pady=20)

    root.mainloop()


def main():
    configuration: dict = get_conf()
    currentround = 0
    maxround = configuration["work"]["rounds"]
    print(type(configuration))
    print(configuration)
    # example config as it is currently expected
    # {'api': {'key': {'nasa': 'hgjlcOGG6700ioscmSOo7zHVzdhnf', 'test': 'test'}}, 'storage': {'path': '~/.config/break', 'max': 4}, 'breaks': {'long': 30, 'short': 10}, 'work': {'interval': 30, 'rounds': 3}}

    if check_connection():
        if configuration["api"]["key"]["nasa"]:
            info = get_json_nasa(configuration["api"]["key"]["nasa"])
        else:
            print("no apikey in config, using Demo key")
            info = get_json_nasa()

        image = cache_image(info, configuration)
        print(image)
        imageoff = None
    else:
        imageoff = get_image_offline(configuration)
        image = None
        print(imageoff)

    resolution = get_monitor_size()
    if image is not None:
        resized_img = resize_image(image, resolution, configuration)

    elif imageoff is not None:
        resized_img = imageoff
    else:
        print("That is unexpected")

    while currentround < maxround:
        turn(configuration, resized_img, resolution, currentround)
        currentround += 1


if __name__ == "__main__":
    main()
