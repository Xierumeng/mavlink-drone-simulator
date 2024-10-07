"""
Download and save files from the World Wide Web.
"""

import pathlib
import urllib.request

from . import download_name_map


def download_and_save(
    base_url: str, names: download_name_map.DownloadNameMap, base_save_path: pathlib.Path
) -> bool:
    """
    Download and save file to the path from the URL.

    base_url: Must have / at end.
    names: Filenames.
    base_save_path: Local save location.

    Return: Success.
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
