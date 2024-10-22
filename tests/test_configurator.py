import builtins
import os
import unittest.mock as mock

import pytest

import configurator
from InvalidFileError import InvalidFileError

# TODO: Aparently the unittest.mock library contains a function mock.open that can mock files
# That could help by not having to use testdata stored aside from tests
# mock.patch fakes the call to os.path.isfile to return True cause we fake the file contents here.


@mock.patch("os.path.isfile")
def test_read_valid_configfile(mock_os_is_file):
    data = """
   [storage]
   path = "."
   max = 1
   [breaks]
   long = 30
   short = 5

   [work]
   interval = 40
   rounds = 3
   """
    mock_os_is_file.return_value = True
    mock_open = mock.mock_open(read_data=data)
    with mock.patch("builtins.open", mock_open):
        config = configurator.Configurator("mockfile.toml")
        assert config.read_configfile() == {
            "storage": {"path": ".", "max": 1},
            "breaks": {"long": 30, "short": 5},
            "work": {"interval": 40, "rounds": 3},
        }


def test_read_invalid_keys_configfile():
    pass


# If file exsists but is invalid check if new config has been written
# mock file open on empty file and check contents after
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


# @mock.patch('os.path.isfile')
# def test_write_config(mock_os_is_file):

#    data = '[storage]\npath = "."\nmax = 1\n[breaks]\nlong = 30\nshort = 5\n[work]\ninterval = 40\nrounds = 3'

#    mock_os_is_file.return_value =  True
#    mock_open = mock.mock_open(read_data=data)
#    with mock.patch("builtins.open", mock_open):
#        config = configurator.Configurator("mockfile.toml")

#    empty_file = ""
#    mock_open_empty = mock.mock_open(read_data=empty_file)
#    with mock.patch("builtins.open",mock_open_empty):
#        config.write_configfile()
#        print (empty_file)
#    data = data.replace("\n","").strip()
#    empty_file=empty_file.replace("\n","").strip()
#    # \n dont matter to the toml file
#    print(data)
#    print(empty_file)
#
#    assert data == empty_file


@mock.patch("os.path.isfile")
def test_read_non_exsistant_configfile(os_path_mock):
    os_path_mock.return_value = False
    with pytest.raises(FileNotFoundError):
        conf = configurator.Configurator()
