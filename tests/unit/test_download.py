"""
Test download.
"""

import pathlib

import pytest

from modules.download import download
from modules.download import download_name_map


# Test functions use test fixture signature names and access class privates
# No enable
# pylint: disable=protected-access,redefined-outer-name


@pytest.fixture
def names() -> list[download_name_map.DownloadNameMap]:  # type: ignore
    """
    Single name.
    """
    result, name = download_name_map.DownloadNameMap.create(
        "ArduCopter.elf",
        "ArduCopter.exe",
    )
    assert result
    assert name is not None

    yield [name]  # type: ignore


def test_single_file(
    names: list[download_name_map.DownloadNameMap], tmp_path: pathlib.Path
) -> None:
    """
    Basic test to download and save a single file.

    This test is fragile as it depends on a remote server!
    """
    # Setup
    base_url = "https://firmware.ardupilot.org/Tools/MissionPlanner/sitl/CopterStable/"

    # Build a temporary directory using tmp_path so
    # the files are cleaned after the tests are run
    tmp_path.mkdir(parents=True, exist_ok=True)

    # Run
    result = download.download_and_save(base_url, names, tmp_path)

    # Check
    assert result
    assert pathlib.Path(tmp_path, names[0].local_name).stat().st_size == 9511971
