from configurator import Configurator
from InvalidFileError import InvalidFileError


def main():
    try:
        c = Configurator("test.yml")
        print(c.filepath)
        print(c.read_configfile())
        print()
        print(type(c.read_configfile()))
    except InvalidFileError:
        print(
            "the specified file is invalid\nNow loading default configuration and saving it to file"
        )
        c = Configurator()
        c.write_configfile()
        print(c.configuration)
    except FileNotFoundError:
        print("thisFile does not exsist")


if __name__ == "__main__":
    main()
