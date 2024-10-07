"""
Test download_data.
"""

import pytest

from modules.download import download_data


# Test functions use test fixture signature names and access class privates
# No enable
# pylint: disable=protected-access,redefined-outer-name


@pytest.fixture
def download_name_map() -> list[download_data.DownloadNameMap]:  # type: ignore
    """
    Single file to download.
    """
    result, name = download_data.DownloadNameMap.create(
        "test_file",
        "test_file",
    )

    assert result
    assert name is not None

    yield [name]


class TestBaseUrlAndNames:
    """
    Test BaseUrlAndNames.
    """

    def test_create_with_slash(
        self, download_name_map: list[download_data.DownloadNameMap]
    ) -> None:
        """
        Input URL has / suffix.
        """
        # Setup
        input_url = "url/"
        expected = input_url

        # Run
        result, base_url_and_names = download_data.BaseUrlAndFilenames.create(
            input_url, download_name_map
        )

        # Check
        assert result
        assert base_url_and_names is not None
        assert base_url_and_names.base_url == expected

    def test_create_without_slash(
        self, download_name_map: list[download_data.DownloadNameMap]
    ) -> None:
        """
        Input URL does not have / suffix.
        """
        # Setup
        input_url = "url"
        expected = input_url + "/"

        # Run
        result, base_url_and_names = download_data.BaseUrlAndFilenames.create(
            input_url, download_name_map
        )

        # Check
        assert result
        assert base_url_and_names is not None
        assert base_url_and_names.base_url == expected
