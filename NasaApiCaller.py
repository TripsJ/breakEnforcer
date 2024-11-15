import sys
from typing import Union

import requests

from InvalidFileError import (  # Unions allow for a fixed set of types in variables, usefull for typing dicts stat hahe strings as keys and ints, floats or stringf as values
    InvalidFileError,
)


class NasaApiCaller:

    def __init__(self, api_key: str = "DEMO_KEY") -> None:
        self.api_url = "https://api.nasa.gov/planetary/apod"
        self.api_key = api_key

    def get_json(self, number_of_images=1, trys=3) -> dict:
        """Grab image"""
        params: dict[str, Union[str, int]] = {
            "api_key": self.api_key,
            "count": number_of_images,
        }
        response = requests.get(self.api_url, params)

        try:
            # raises HTTPError if requst was unsuccessfull
            response.raise_for_status()
            # the api sends a list of Json back as it could very well contain multiple images. Requests from this api however, contain one url to an image.²
            # print(response.json()[0])
            if response.json()[0]["media_type"] == "image":
                return response.json()[0]
            else:
                if trys > 0:
                    print("received video, retrying")
                    return self.get_json(number_of_images, trys - 1)
                else:
                    raise InvalidFileError
        except requests.HTTPError:
            print(response.status_code)
            sys.exit()
            return {"Error": response.status_code}  # this should never ever be reached
        # its just there so the function returns something and mypy can stop complaining
