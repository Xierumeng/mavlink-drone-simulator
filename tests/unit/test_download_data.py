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
        "test_file_a",
        "test_file_b",
    )

    assert result
    assert name is not None

    yield [name]


class TestBaseUrlAndNames:
    """
    Test BaseUrlAndNames.
    """

    def test_create_from_config(self) -> None:
        """
        Normal.
        """
        # Setup
        input_url = "url"
        expected_url = input_url + "/"

        name_a = "test_file_a"
        name_b = "test_file_b"
        name_pairs = [(name_a, name_b)]

        result, download_map = download_data.DownloadNameMap.create(name_a, name_b)
        assert result
        assert download_map is not None

        expected_names = [download_map]

        # Run
        result, base_url_and_names = download_data.BaseUrlAndFilenames.create_from_config(
            input_url, name_pairs
        )

        # Check
        assert result
        assert base_url_and_names is not None
        assert base_url_and_names.base_url == expected_url
        assert len(base_url_and_names.names) == len(expected_names)

    def test_create_from_config_wrong_tuple_length(self) -> None:
        """
        Tuple of length 3 instead of 2 .
        """
        # Setup
        input_url = "url"

        name_a = "test_file_a"
        name_b = "test_file_b"
        name_c = "test_file_c"
        name_pairs = [(name_a, name_b, name_c)]

        # Run
        result, base_url_and_names = download_data.BaseUrlAndFilenames.create_from_config(
            input_url, name_pairs
        )

        # Check
        assert not result
        assert base_url_and_names is None

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
