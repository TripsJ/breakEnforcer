import os
import unittest.mock as mock

import pytest

import configurator
from InvalidFileError import InvalidFileError


@pytest.fixture
def valid_configurator():
    return configurator.Configurator("testdata/valid.toml")


def test_read_valid_configfile(valid_configurator):
    assert valid_configurator.read_configfile() == {
        "storage": {"path": ".", "max": 1},
        "breaks": {"long": 30, "short": 5},
        "work": {"interval": 40, "rounds": 3},
    }


def test_read_invalid_keys_configfile():
    pass


@pytest.mark.parametrize(
    "invalid_file, error",
    [
        ("./in/va/lid/nonexsistent.toml", FileNotFoundError),
        ("testdata/invalid_extension.txt", InvalidFileError),
        ("testdata/nonexsistent.toml", FileNotFoundError),
        ("testdata/copyvalidasyaml.yaml", InvalidFileError),
    ],
)
def test_read_invalid_configfile(invalid_file, error):

    assert (
        (not os.path.isfile(invalid_file))
        or (
            invalid_file == "testdata/invalid_extension.txt"
            and os.path.isfile(invalid_file)
        )
        or (
            invalid_file == "testdata/copyvalidasyaml.yaml"
            and os.path.isfile(invalid_file)
        )
    )
    with pytest.raises(error):
        configurator.Configurator(invalid_file)


def test_write_configfile(valid_configurator):
    assert not os.path.isfile("config.toml")
    valid_configurator.write_configfile()
    assert os.path.isfile("config.toml")


def test_no_configfile():
    pass
