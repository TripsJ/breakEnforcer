import os
import unittest.mock as mock

import pytest

import configurator


@pytest.fixture
def valid_configurator():
    return configurator.Configurator("testdata/valid.toml")


def test_read_valid_configfile(valid_configurator):
    assert valid_configurator.read_configfile() == {
        "storage": {"path": ".", "max": 1},
        "breaks": {"long": 30, "short": 5},
        "work": {"interval": "40", "rounds": 3},
    }


def test_read_invalid_keys_configfile():
    pass


def test_read_invalid_path_configfile():
    pass


def test_write_configfile(valid_configurator):
    assert not os.path.isfile("config.toml")
    valid_configurator.write_configfile()
    assert os.path.isfile("config.toml")


def test_no_configfile():
    pass
