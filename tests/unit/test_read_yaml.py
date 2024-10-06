"""
Test read_yaml.
"""

import pathlib

from modules.read_yaml import read_yaml


# Test functions use test fixture signature names and access class privates
# No enable
# pylint: disable=protected-access,redefined-outer-name


TEST_FILES_DIRECTORY = pathlib.Path("tests", "unit", "read_yaml_test_files")


def test_normal() -> None:
    """
    Normal YAML file.
    """
    # Setup
    file_path = pathlib.Path(TEST_FILES_DIRECTORY, "config_no_error.yaml")

    expected = {"config": "no_error"}

    # Run
    result, actual = read_yaml.open_config(file_path)

    # Check
    assert result
    assert actual == expected


def test_file_not_found() -> None:
    """
    File does not exist.
    """
    # Setup
    file_path = pathlib.Path(TEST_FILES_DIRECTORY, "config_does_not_exist.yaml")

    # Run
    result, actual = read_yaml.open_config(file_path)

    # Check
    assert not result
    assert actual is None
