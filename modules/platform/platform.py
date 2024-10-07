"""
Get platform.
"""

import enum
import os


class OperatingSystem(enum.Enum):
    """
    MacOS is Unix.
    """

    WINDOWS = 0
    UNIX = 1


def get_os() -> tuple[bool, OperatingSystem | None]:
    """
    Get OS.

    Return: Success, the operating system as an enumeration value.
    """
    # Use os instead of platform as MacOS and Linux are treated identically.
    os_name = os.name

    if os_name == "nt":
        return True, OperatingSystem.WINDOWS

    if os_name == "posix":
        return True, OperatingSystem.UNIX

    return False, None
