import time # Keep track of time and sleep
import requests # Make webrequests to apis

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


#TODO: make this not freeze the whole thing while counting down
def set_timer(hours, minutes) -> bool:
    current_time = time.strftime("%H:%M")
    target_time = f"{hours}:{minutes}"
    while current_time != target_time:
        time.sleep(1)
        current_time = time.strftime("%H:%M")
        print(current_time)
    return True

def read_config(configfile)->dict:
    '''reads necessary and optional configuration options from a file and returns them as a dict'''
    

def get_json_nasa(apikey :str="DEMO_KEY"):
    """Grab image description from the nasa Astronomy image of the day, parse the returned json and return it. If Errors Occure, return the status code"""
    response = requests.get("https://api.nasa.gov/planetary/apod",params={"api_key":apikey,"count":1})
    try:
        response.raise_for_status()# raises HTTPError if requst was unsuccessfull
        return response.json()
    except requests.HTTPError:
        return response.status_code
        


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
    #hours, minutes = get_input()
    #if set_timer(hours, minutes):
    #    print("Ready")
    print(get_json_nasa())

if __name__ == "__main__":
    main()
