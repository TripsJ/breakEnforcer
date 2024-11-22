import os
import unittest.mock as mock
from http.client import NotConnected

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
    """Test returns a fixed  size image as 'Monitor', and tests if the expected value is returned
    Returns:
           None
    Raises:
           AssertionError"""

    return_image = Im.new(mode="RGB", size=(1, 1))
    mock_monitor.return_value = return_image
    assert main.get_monitor_size() == (1, 1)


# Test needs to run at least twice.oce with a patched storage path thats configured once grabbing on the default config.


def test_cache_image() -> None:

    pass


def test_get_image_offline(tmpdir) -> None:

    os.mkdir(tmpdir.join("resized"))
    testfile = tmpdir.join("resized").join("test.jpg")
    conf = {"storage": {"path": tmpdir}}
    return_image = Im.new(mode="RGB", size=(1, 1))
    with open(testfile, "wb") as f:
        return_image.save(f)
    returnfile = main.get_image_offline(conf)
    assert returnfile == "test.jpg"


def test_resize_image() -> None:
    pass


def test_display_image() -> None:
    pass


############################# Connection related tests ###########################


@mock.patch("http.client.HTTPConnection")
@mock.patch("http.client.HTTPResponse")
def test_check_connection_successfull(mock_connection, mock_response) -> None:
    """mocks a Valid Network connectiont, checks if check connection returns true
    Returns
        None
    Raises
        AssertionError
    """
    mock_response.status = 200
    mock_connection.getresponse = mock.MagicMock(retun_value=mock_response)
    assert main.check_connection() == True


# @pytest.mark.skip(reason="Test not working yet")
def test_check_connection_unsuccessfull() -> None:
    """mocks an invalid Network connectiont, checks if check connection returns False
    Returns
        None
    Raises
        AssertionError
    """
    with mock.patch("http.client.HTTPConnection") as mock_connection:
        mock_connection.return_value = NotConnected
        assert main.check_connection() == False


def test_get_json_nasa() -> None:
    valid_json_data = {
        "date": "2024-11-13",
        "explanation": "A mere 56 million light-years distant toward the southern constellation Fornax, NGC 1365 is an enormous barred spiral galaxy about 200,000 light-years in diameter. That's twice the size of our own barred spiral Milky Way. This sharp image from the James Webb Space Telescope's Mid-Infrared Instrument (MIRI) reveals stunning details of this magnificent spiral in infrared light. Webb's field of view stretches about 60,000 light-years across NGC 1365, exploring the galaxy's core and bright newborn star clusters. The intricate network of dusty filaments and bubbles is created by young stars along spiral arms winding from the galaxy's central bar. Astronomers suspect the gravity field of NGC 1365's bar plays a crucial role in the galaxy's evolution, funneling gas and dust into a star-forming maelstrom and ultimately feeding material into the active galaxy's central, supermassive black hole.",
        "hdurl": "https://apod.nasa.gov/apod/image/2411/JWSTMIRI_ngc1365.png",
        "media_type": "image",
        "service_version": "v1",
        "title": "Barred Spiral Galaxy NGC 1365 from Webb",
        "url": "https://apod.nasa.gov/apod/image/2411/JWSTMIRI_ngc1365_1024.png",
    }
    mock_response = mock.Mock()
    mock_response.status_code = 200

    pass


################## Timer related tests #####################################


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
