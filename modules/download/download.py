"""
Download and save files from the World Wide Web.
"""

import pathlib
import urllib.request


class DownloadNameMap:
    """
    For renaming downloaded files.
    """

    __create_key = object()

    @classmethod
    def create(cls, remote_name: str, local_name: str) -> "tuple[bool, DownloadNameMap | None]":
        """
        remote_name: Filename on the server.
        local_name: Filename on the client.
        """
        if remote_name == "":
            return False, None

        if local_name == "":
            return False, None

        return True, DownloadNameMap(cls.__create_key, remote_name, local_name)

    def __init__(self, class_private_create_key: object, remote_name: str, local_name: str) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is DownloadNameMap.__create_key, "Use create() method"

        self.remote_name = remote_name
        self.local_name = local_name


def download_and_save(base_url: str, names: DownloadNameMap, base_save_path: pathlib.Path) -> bool:
    """
    Download and save file to the path from the URL.

    base_url: Must have / at end.
    names: Filenames.
    base_save_path: Local save location.
    """
    # TODO: Exception catching

    for name in names:
        # Download

        full_url = base_url + name.remote_name

        with urllib.request.urlopen(full_url) as remote_file:
            content = remote_file.read()

        # Save
        with open(pathlib.Path(base_save_path, name.local_name), "wb") as local_file:
            local_file.write(content)

    return True
