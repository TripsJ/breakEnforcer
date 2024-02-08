import time


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


# make this not freeze the whole thing while counting down
def set_timer(hours, minutes) -> bool:
    current_time = time.strftime("%H:%M")
    target_time = f"{hours}:{minutes}"
    while current_time != target_time:
        time.sleep(1)
        current_time = time.strftime("%H:%M")
        print(current_time)
    return True


def get_image_online():
    """Grab image from api and save it to a local folder
    returns the path to the saved image"""
    return None


def get_image_offline():
    """Get random image from a set of local folders
    return path to that image"""
    return None


def check_connection() -> bool:
    """Check if Machine is connected to the internet
    return True if it is, false if not"""
    return None


def display_image(image):
    """get focus from Window Manager and display image Full Screen"""
    return None

def error(exception: Exception):
    '''handle Exceptions according to their nature'''
    print("Something went Wong")

def main():
    hours, minutes = get_input()
    if set_timer(hours, minutes):
        print("Ready")


if __name__ == "__main__":
    main()
