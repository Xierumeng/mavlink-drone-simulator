"""
Test download.
"""

from modules.platform import platform


# Test functions use test fixture signature names and access class privates
# No enable
# pylint: disable=protected-access,redefined-outer-name


def test_os() -> None:
    """
    Basic test to get OS.
    """
    # Run
    result, operating_system = platform.get_os()

    # Check
    assert result
    assert operating_system is not None

    print(operating_system)
