import errno
import os.path

import toml

from InvalidFileError import InvalidFileError


class Configurator:
    def __init__(self, filepath: str = "break.toml") -> None:
        self.filepath: str = filepath  # path to configfile
        self.configuration: dict = {
            "api": {"key": {"nasa": "DEMO_KEY"}},
            "storage": {"path": ".", "max": 1},
            "breaks": {"long": 30, "short": 5},
            "work": {"interval": 40, "rounds": 3},
        }
        # commandline arguments

    def read_configfile(self) -> dict:
        with open(self.filepath, "r", encoding="utf-8") as file:
            # open the config file using utf-8 as the encoding
            # because it has the most characters and avoids relying on system defaults
            conf = toml.load(file)
            # VALIDATE ENTRIES
            if conf["storage"]["path"]:
                path = conf["storage"]["path"]
                if not os.path.isdir(path):
                    print(f"invalid path detected: {conf["storage"]["path"]}")
                    del conf["storage"]["path"]

            for entry in [
                conf["storage"]["max"],
                conf["breaks"]["short"],
                conf["breaks"]["long"],
                conf["work"]["rounds"],
            ]:
                if entry:
                    if not isinstance(entry, int):
                        print(f"invalid configuration detected: {entry}")
                        del entry

            return conf

    def write_configfile(self) -> None:
        with open("config.toml", "w") as f:
            toml.dump(self.configuration, f)
        print("config.toml created")

    @property
    def filepath(self) -> str:
        return self._filepath

    @filepath.setter
    def filepath(self, filepath: str) -> None:
        if os.path.isfile(os.path.abspath(filepath)):
            if os.path.splitext(filepath)[1] == ".toml":
                self._filepath: str = filepath
            else:
                print("invalid File")
                # errno.EINVAL is the invalid Argument errno
                raise InvalidFileError(
                    errno.EINVAL, os.strerror(errno.EINVAL), filepath
                )

        else:
            print("File not found")
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filepath)
