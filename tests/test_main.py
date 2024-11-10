import unittest.mock as mock

import pytest
from PIL import Image as Im

import main

##################### Configuration related tests ################################


def test_write_default_config(tmpdir) -> None:
    """Test creates a Temporary directory and a test.oml file within it.
    Tests if that file contains the default configuration after write_default_config has been called.
    Returns:
           None
    Raises:
           AssertionError"""

    test_file = tmpdir.join("test.toml")
    main.write_default_config(test_file)
    assert (
        test_file.read()
        == """[storage]
path = "."
max = 1

[breaks]
long = 30
short = 5

[work]
interval = 40
rounds = 3

[api.key]
nasa = "DEMO_KEY"
"""
    )


@mock.patch("os.path.isfile")
def test_get_conf(mock_os_is_file) -> None:
    """Test fakes a valid config file .
    Tests if the values and keys are read and returned correctly.
    Returns:
           None
    Raises:
           AssertionError"""

    valid_data = """[storage]
path = "."
max = 2

[breaks]
long = 25
short = 6

[work]
interval = 25
rounds = 6

[api.key]
nasa = "DEMO_KEY"
"""
    mock_os_is_file.return_value = True
    mock_open = mock.mock_open(read_data=valid_data)
    with mock.patch("builtins.open", mock_open):
        assert main.get_conf()["storage"]["path"] == "."
        assert main.get_conf()["work"]["interval"] == 25
        assert main.get_conf()["work"]["rounds"] == 6
        assert main.get_conf()["api"]["key"]["nasa"] == "DEMO_KEY"
        assert main.get_conf()["breaks"]["long"] == 25


@mock.patch("os.path.isfile")
def test_get_conf_not_found(mock_os_is_file) -> None:
    """Test Forces a File not found Error on the config file, tests if default values are returned as expected
    Returns:
           None
    Raises:
           AssertionError"""
    mock_os_is_file.return_value = False
    assert main.get_conf()["storage"]["path"] == "."
    assert main.get_conf()["work"]["interval"] == 40
    assert main.get_conf()["work"]["rounds"] == 3
    assert main.get_conf()["api"]["key"]["nasa"] == "DEMO_KEY"
    assert main.get_conf()["breaks"]["long"] == 30


################ Image related tests ##########################################


@mock.patch("PIL.ImageGrab.grab")
def test_get_monitor_size(mock_monitor) -> None:

    return_image = Im.new(mode="RGB", size=(1, 1))
    mock_monitor.return_value = return_image
    assert main.get_monitor_size() == (1, 1)


def test_cache_image() -> None:
    pass


def test_get_image_offline() -> None:
    pass


def test_resize_image() -> None:
    pass


def test_display_image() -> None:
    pass


############################# Connection related tests ###########################


def test_check_connection() -> None:
    pass


def test_get_json_nasa() -> None:
    pass


####################### Timer related tests #####################################


def test_converttoms() -> None:
    pass


def test_converttoclock() -> None:
    pass


def test_turn() -> None:
    pass


def test_interrupt_count() -> None:
    pass


def test_run() -> None:
    pass


def test_main() -> None:
    pass
