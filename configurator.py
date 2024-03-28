import os.path
from InvalidFileError import InvalidFileError
import errno
import toml


class Configurator:
    def __init__(self, filepath="break.toml"):
        self.filepath = filepath  # path to configfile
        self.configuration = {
            "api": {"key": {"nasa": "defaultvalue"}},
            "storage": {"path": ".", "max": 1},
            "breaks": {"long": 30, "short": 5},
            "work": {"interval": 40, "rounds": 3},
        }
        # commandline arguments

    def read_configfile(self):
        with open(self.filepath, "r", encoding="utf-8") as file:
            # open the config file using utf-8 as the encoding
            # because it has the most characters and avoids relying on system defaults
            return toml.load(file)

    def write_configfile(self):
        with open("config.toml", "w") as f:
            toml.dump(self.configuration, f)
        print("config.toml created")

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, filepath):
        if os.path.isfile(os.path.abspath(filepath)):
            if os.path.splitext(filepath)[1] == ".toml":
                self._filepath = filepath
            else:
                print("invalid File")
                # errno.EINVAL is the invalid Argument errno
                raise InvalidFileError(
                    errno.EINVAL, os.strerror(errno.EINVAL), filepath
                )

        else:
            print("File not found")
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filepath)
