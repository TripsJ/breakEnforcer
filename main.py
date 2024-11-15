import http.client
import os
import random
import sys
from tkinter import *
from typing import (  # Unions allow for a fixed set of types in variables, usefull for typing dicts stat hahe strings as keys and ints, floats or stringf as values
    Union,
)

import PIL.Image
import requests  # Make webrequests to apis
import toml
from PIL import ImageGrab, ImageTk, UnidentifiedImageError
from PIL.Image import (
    Image as PILImage,  # Allows to declare PIL Images as PILImage types
)

# chck how to correctly type PIL TKinter and pil dont seem too like each other
from configurator import Configurator
from InvalidFileError import InvalidFileError
from NasaApiCaller import NasaApiCaller

# glabal variable to keep track of pause state during turns
# just declaring and typing it so mypy knows it exsists as a global and what type it is
_running: bool


# Write out a standard configfile and return it
def write_default_config(filename: str) -> dict:
    """Write a sane default configuration to file and return it
    Returns:
       Dictionary
    """
    DEFAULT_CONFIG = {
        "api": {"key": {"nasa": "DEMO_KEY"}},
        "storage": {"path": ".", "max": 1},
        "breaks": {"long": 30, "short": 5},
        "work": {"interval": 40, "rounds": 3},
    }

    if os.path.isfile(filename):
        os.remove(filename)
    with open(filename, "w") as f:
        toml.dump(DEFAULT_CONFIG, f)
    print("default config created")
    return DEFAULT_CONFIG


## Getting configuration
def get_conf() -> dict:
    """Reads configuration from a file and stores it in a dict to be returned

    Should the provided configuration file cause an exception because it is invalid, a default configuration is returned

    Returns:
        Dictionary
    """

    try:

        c: Configurator = Configurator()
        print(c.read_configfile())
        return c.read_configfile()
    except InvalidFileError:
        print(
            """the specified file is invalid
            Now loading default configuration and saving it to file"""
        )
        return write_default_config("config.toml")

    except FileNotFoundError:
        print(
            "the specified file was not Found, Loading default config and writing to file"
        )
        return write_default_config("config.toml")


def get_monitor_size() -> tuple[int, int]:
    """Guesses teh size of a monitor by using the size property of a Pil Image of the currently focussed monitor
    Returns
        Tuple of Integers"""

    monitor: PILImage = ImageGrab.grab()
    return monitor.size


def check_connection() -> bool:
    """test if an internet connection can be established

    First tries to resolve the dns adress of google.com and if successfull, attempts to download the head of that webpage
    More than a Head is not necessary as we do not need data from google
        Returns
            bool
    """
    conn: http.client.HTTPConnection = http.client.HTTPConnection(
        "www.google.com"
    )  # Testing against googles dns address
    # print(type(conn))
    try:
        conn.request(
            "HEAD", "/"
        )  # No need to download anything so limmiting the request to only get the Head
        return True
    except:
        return False  # In case of exception return False


def cache_image(imageinfo: dict, configuration: dict) -> str | dict:
    """downloads an image and saves it to the disk

    if a filepath is configured in the configuration, it attempts to save in that directory, if not it saves in the current directory

    Arguments
        imageinfo: Dictionary containing the information from the api
        configuration: Dictionary containing the user set configuration

    Returns
        String Filename
        Dictionary Imageinfo
    """

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
        return imageinfo  # TODO: This should probably be an exception


def get_image_offline(configuration: dict) -> str:

    if targetpath := configuration.get("storage", {}).get("path"):
        if os.path.isdir(os.path.join(targetpath, "resized")):
            return random.choice(os.listdir(os.path.join(targetpath, "resized")))

    raise FileNotFoundError


def resize_image(input_filename: str, resolution: tuple, configuration: dict) -> str:
    try:
        with PIL.Image.open(input_filename) as im:
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


def display_image(image, res, duration) -> Tk:
    """display an Image"""
    try:
        frame: Tk = Tk()
        frame.minsize(res[0], res[1])
        im = PIL.Image.open(image)
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


def converttoms(duration: int | str) -> float:
    if isinstance(duration, int):
        return duration * 60 * 1000

    if "h" in duration:
        splitchar: str = "h"
    elif ":" in duration:
        splitchar = ":"
    else:
        return 0
    sh, sm = duration.split(splitchar)
    h: int = int(sh)
    m: int = int(sm) + (h * 60)
    return m * 60 * 1000


def converttoclock(countdown: float) -> str:
    seconds = (countdown / 1000) % 60
    seconds = int(seconds)
    minutes = (countdown / (1000 * 60)) % 60
    minutes = int(minutes)
    hours = (countdown / (1000 * 60 * 60)) % 24
    return "%d:%d:%d" % (hours, minutes, seconds)


def turn(
    configuration: dict,
    resized_img: str,
    resolution: tuple[int, int],
    currentround: int,
    maxround: int,
) -> None:
    duration: str = "0h:0m"
    countdown: float = -1
    global _running
    _running = True

    pause: int = configuration["breaks"]["short"]
    duration = configuration["work"]["interval"]
    countdown = converttoms(duration) / 1000
    root: Tk = Tk()
    clock: str = converttoclock(converttoms(duration))
    lable: Label = Label(
        root,
        text=clock,
        font=("Arial", 22),
    )
    startbtn: Button = Button(
        root,
        text="Start",
        font=("Arial", 15),
        command=lambda: [
            startbtn.config(state=DISABLED),
            run(countdown, resized_img, resolution),
        ],
    )
    pausebtn: Button = Button(
        root,
        text="Pause",
        font=("Arial", 15),
        command=lambda: [
            interrupt_count(),
        ],
    )

    def interrupt_count() -> int:
        global _running
        _running = not _running
        return 0  # Mypy does not like functions that are used by others when they return None so i return 0 it does not serve any other purpose

    def run(
        countdown: float,
        resized_image: str,
        resolution: tuple[int, int],
    ) -> int:
        global _running
        # print(running)
        c: StringVar = StringVar()

        if countdown == 0:
            root.destroy()
            display_image(resized_img, resolution, pause)
            return 0
        if countdown < 0:
            print("please set timer first")
            return 1

        if _running:
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
        return 0  # Mypy does not like functions that are used by others when they return None so i return 0 it does not serve any other purpose

    if currentround > 0:
        startbtn.invoke()

    lable.pack(anchor="center", pady=20)
    startbtn.pack(padx=20, pady=20)
    pausebtn.pack(padx=20, pady=20)

    root.mainloop()


def main() -> None:
    configuration: dict = get_conf()
    currentround: int = 0
    maxround: int = configuration["work"]["rounds"]

    # example config as it is currently expected
    # {'api': {'key': {'nasa': 'hgjlcOGG6700ioscmSOo7zHVzdhnf', 'test': 'test'}}, 'storage': {'path': '~/.config/break', 'max': 4}, 'breaks': {'long': 30, 'short': 10}, 'work': {'interval': 30, 'rounds': 3}}

    if check_connection():
        if configuration["api"]["key"]["nasa"]:
            nasa_caller = NasaApiCaller(api_key=configuration["api"]["key"]["nasa"])
        else:
            print("no apikey in config, using Demo key")
            nasa_caller = NasaApiCaller()
        nasa_img_info = nasa_caller.get_json()

        image = cache_image(nasa_img_info, configuration)
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
        turn(configuration, resized_img, resolution, currentround, maxround)
        currentround += 1


if __name__ == "__main__":
    main()
