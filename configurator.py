import errno
import os.path

import toml

from InvalidFileError import InvalidFileError


class InvalidConfigurationError(Exception):
    pass


class Configurator:

    def __init__(self, filepath: str = "config.toml") -> None:
        self.filepath: str = filepath  # path to configfile
        self.configuration: dict = {}

    def read_configfile(self) -> dict:
        """Reads the defined configuration file and checks its contents for invalid entrys
        If the configuration is valid, a Dictionary containig that config is returned else, an Error is raised

        Raises:
            InvalidConfigurationError

        Returns:
            Dictionary

        """
        invalid_entrys = []
        valid_keys = [
            "storage",
            "max",
            "breaks",
            "long",
            "short",
            "work",
            "rounds",
            "path",
            "interval",
            "api",
            "key",
            "nasa",
        ]
        with open(self.filepath, "r", encoding="utf-8") as file:
            # open the config file using utf-8 as the encoding
            # because it has the most characters and avoids relying on system defaults
            conf = toml.load(file)
            print(conf)
            print(file)
            # VALIDATE ENTRIES
            for key in conf.keys():
                if key not in valid_keys:
                    raise InvalidConfigurationError
            if conf["storage"]["path"]:
                path = conf["storage"]["path"]
                if not os.path.isdir(path):
                    print(f"invalid path detected: {conf["storage"]["path"]}")
                    invalid_entrys.append(conf["storage"]["path"])

            for entry in [
                conf["storage"]["max"],
                conf["breaks"]["short"],
                conf["breaks"]["long"],
                conf["work"]["rounds"],
            ]:
                if entry:
                    if not isinstance(entry, int):
                        print(f"invalid configuration detected: {entry}")
                        invalid_entrys.append(entry)

        if len(invalid_entrys) == 0:
            self.configuration = conf
            return self.configuration
        print(f"The following entries are not valid {invalid_entrys}")
        raise InvalidConfigurationError

    @property
    def filepath(self) -> str:
        return self._filepath

    @filepath.setter
    def filepath(self, filepath: str) -> None:
        """
        checks if the defined file exsists and is a .toml file, if so sets it to self.filepath
        Els raises eitehr FileNotFoundError Or InvalidFileError
            Returns:
                None
            Raises:
                 InvalidFileError
                 FileNotFoundError
        """
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
            raise FileNotFoundError
