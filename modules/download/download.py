"""
Download and save files from the World Wide Web.
"""

import pathlib
import shutil
import urllib.request

from . import download_data


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
    base_url_and_filenames: download_data.BaseUrlAndFilenames, base_save_path: pathlib.Path
) -> bool:
    """
    Download and save files to the path from the URL.

    base_url_and_filenames: Base URL and list of filenames.
    base_save_path: Local save location.

    Return: Success.
    """
    if not base_save_path.exists():
        print(f"ERROR: Path doesn't exist: {base_save_path}")
        return False

    if not base_save_path.is_dir():
        print(f"ERROR: Not a directory: {base_save_path}")
        return False

    for name in base_url_and_filenames.names:
        # Download
        full_url = base_url_and_filenames.base_url + name.remote_name

        try:
            with urllib.request.urlopen(full_url) as remote_file:
                content = remote_file.read()
        # Catching all exceptions for library call
        # pylint: disable-next=broad-exception-caught
        except Exception as exception:
            print(f"ERROR: Could not download {full_url} with exception: {exception}")

        # Save
        try:
            with open(pathlib.Path(base_save_path, name.local_name), "wb") as local_file:
                local_file.write(content)
        # Catching all exceptions for library call
        # pylint: disable-next=broad-exception-caught
        except Exception as exception:
            print(f"ERROR: Could not save {name.local_name} with exception: {exception}")

    return True
