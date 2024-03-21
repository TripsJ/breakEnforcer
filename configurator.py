import toml
import os.path
import errno


class Configurator:
    def __init__(self, filepath="break.toml"):
        self.filepath = filepath  # path to configfile
        # commandline arguments

    def read_configfile(self):
        with open(self.filepath, "r") as f:
            return toml.load(f)

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, filepath):
        if os.path.isfile(os.path.abspath(filepath)):
            self._filepath = filepath
        else:
            print("YAY I BROKE IT")
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filepath)
