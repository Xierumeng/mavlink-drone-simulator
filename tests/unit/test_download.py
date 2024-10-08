"""
Test download.
"""

import pathlib

import pytest

from modules.download import download
from modules.download import download_data


# Test functions use test fixture signature names and access class privates
# No enable
# pylint: disable=protected-access,redefined-outer-name


@pytest.fixture
def test_directory_create(tmp_path: pathlib.Path) -> pathlib.Path:  # type: ignore
    """
    Create temporary directory.
    """
    tmp_path.mkdir(parents=True, exist_ok=True)

    yield tmp_path


@pytest.fixture
def base_url_and_single_name() -> download_data.BaseUrlAndFilenames:  # type: ignore
    """
    Single name.
    """
    result, name = download_data.DownloadNameMap.create(
        "copter.parm",
        "test.parm",
    )
    assert result
    assert name is not None

    base_url = "https://raw.githubusercontent.com/ArduPilot/ardupilot/refs/heads/master/Tools/autotest/default_params/"
    result, base_url_and_filenames = download_data.BaseUrlAndFilenames.create(
        base_url,
        [name],
    )

    assert result
    assert base_url_and_filenames is not None

    yield base_url_and_filenames


class TestDeleteDirectory:
    """
    Test delete_directory() function.
    """

    def test_normal(self, test_directory_create: pathlib.Path) -> None:
        """
        Basic test.
        """
        # Setup
        test_file_path = pathlib.Path(test_directory_create, "test_file.txt")
        with open(test_file_path, "w", encoding="utf-8") as test_file:
            test_file.write("Test")

        assert test_file_path.exists()

        # Run
        result = download.delete_directory(test_directory_create)

        # Check
        assert result
        assert not test_directory_create.exists()

    def test_nonexistent_path(self, test_directory_create: pathlib.Path) -> None:
        """
        Path doesn't exist.
        """
        # Setup
        nonexistent_directory = pathlib.Path(test_directory_create, "nonexistent_directory")

        # Run
        result = download.delete_directory(nonexistent_directory)

        # Check
        assert not result
        assert test_directory_create.exists()

    def test_not_a_directory(self, test_directory_create: pathlib.Path) -> None:
        """
        Non directory path.
        """
        # Setup
        test_file_path = pathlib.Path(test_directory_create, "test_file.txt")
        with open(test_file_path, "w", encoding="utf-8") as test_file:
            test_file.write("Test")

        assert test_file_path.exists()

        # Run
        result = download.delete_directory(test_file_path)

        # Check
        assert not result
        assert test_directory_create.exists()


class TestDownloadAndSave:
    """
    Test download_and_save() function.
    """

    def test_single_file(
        self, base_url_and_single_name: download_data.BaseUrlAndFilenames, tmp_path: pathlib.Path
    ) -> None:
        """
        Basic test to download and save a single file.

        This test is fragile as it depends on a remote server!
        """
        # Setup
        # Build a temporary directory using tmp_path so
        # the files are cleaned after the tests are run
        tmp_path.mkdir(parents=True, exist_ok=True)

        # Run
        result = download.download_and_save(base_url_and_single_name, tmp_path)

        # Check
        assert result

        local_filepath = pathlib.Path(tmp_path, base_url_and_single_name.names[0].local_name)
        assert local_filepath.stat().st_size == 1957
