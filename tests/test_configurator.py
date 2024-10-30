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


@mock.patch("os.path.isfile")
def test_read_invalid_keys_configfile(mock_os_is_file):
    wrong_keys_data = """
   [storage]
   foo = "."
   max = 1
   [Jinx]
   long = 30
   short = 5

   [work]
   Peter = 3
   Horst = 5
   """
    mock_os_is_file.return_value = True
    mock_open = mock.mock_open(read_data=wrong_keys_data)
    with mock.patch("builtins.open", mock_open):
        with pytest.raises(configurator.InvalidConfigurationError):
            invalid_config = configurator.Configurator("mockfile.toml")
            invalid_config.read_configfile()


@mock.patch("os.path.isfile")
def test_read_invalid_configfile(mock_os_is_file):
    mock_os_is_file.return_value = True
    mock_junk_data = """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    In et urna ac est scelerisque varius.
    Pellentesque sed justo convallis lorem luctus semper.
    Aliquam vehicula sapien et velit tempor, vitae ullamcorper nisl bibendum.
    Aenean eget ante id tortor faucibus tristique in a lectus.
    Proin mollis turpis pulvinar lectus posuere, nec porta odio sollicitudin.
    Nunc consequat massa ac dui mattis, quis egestas diam ullamcorper.
    Donec vehicula nisl ut metus hendrerit consectetur.
    Proin ultricies massa condimentum neque malesuada lobortis.
    Integer commodo tortor quis vehicula consectetur.
    """
    mock_open = mock.mock_open(read_data=mock_junk_data)
    with mock.patch("builtins.open", mock_open):
        with pytest.raises(InvalidFileError):
            configurator.Configurator("junk.txt")


@mock.patch("os.path.isfile")
def test_read_non_exsistant_configfile(os_path_mock):
    os_path_mock.return_value = False
    with pytest.raises(FileNotFoundError):
        conf = configurator.Configurator()
