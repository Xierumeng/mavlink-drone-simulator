"""
For YAML files.
"""

import pathlib

import yaml


def open_config(file_path: pathlib.Path) -> "tuple[bool, dict | None]":
    """
    Open and decode YAML file.
    """
    try:
        with file_path.open("r", encoding="utf8") as file:
            config = yaml.safe_load(file)
            return True, config
    # Catching all exceptions for library call
    # pylint: disable-next=broad-exception-caught
    except Exception as exception:
        print(f"ERROR: Could not open and decode YAML file: {exception}")

    return False, None
