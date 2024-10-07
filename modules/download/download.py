"""
Download and save files from the World Wide Web.
"""

import pathlib
import shutil
import urllib.request

from . import download_name_map


def delete_directory(directory_path: pathlib.Path) -> bool:
    """
    Delete the provided directory.

    directory_path: The directory.

    Return: Success.
    """
    if not directory_path.exists():
        print("ERROR: Path doesn't exist")
        return False

    if not directory_path.is_dir():
        print("ERROR: Not a directory")
        return False

    try:
        shutil.rmtree(directory_path)
        return True
    # Catching all exceptions for library call
    # pylint: disable-next=broad-exception-caught
    except Exception as exception:
        print(f"ERROR: Could not delete directory: {exception}")

    return False


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
