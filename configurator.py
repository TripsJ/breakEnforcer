import os.path
import errno
import toml


class Configurator:
    def __init__(self, filepath="break.toml"):
        self.filepath = filepath  # path to configfile
        self.config = {}
        # commandline arguments

    def read_configfile(self):
        with open(self.filepath, "r", encoding="utf-8") as file:
            # open the config file using utf-8 as the encoding
            # because it has the most characters and avoids relying on system defaults
            return toml.load(file)

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, filepath):
        if os.path.isfile(os.path.abspath(filepath)):
            self._filepath = filepath
            self.config = self.read_configfile()
        else:
            print("YAY I BROKE IT")
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filepath)
