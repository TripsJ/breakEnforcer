import unittest.mock as mock

import pytest

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


def test_get_conf() -> None:
    pass


################ Image related tests ##########################################


def test_get_monitor_size() -> None:
    pass


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
