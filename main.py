"""
Downloads and starts the simulator.
"""

import argparse
import os
import pathlib
import subprocess

from modules.download import download
from modules.download import download_data
from modules.platform import platform
from modules.read_yaml import read_yaml


CONFIG_FILE_PATH = pathlib.Path("config.yaml")


def download_simulator(
    local_directory: pathlib.Path,
    config_download_parameters_base_url: str,
    config_download_parameters_filenames: list[list[str]],
    config_download_simulator_base_url: str,
    config_download_simulator_executable: list[list[str]],
    config_download_simulator_filenames: list[list[str]],
) -> bool:
    """
    Download parameters and simulator.
    """
    result, download_parameters_properties = download_data.BaseUrlAndFilenames.create_from_config(
        config_download_parameters_base_url, config_download_parameters_filenames
    )
    if not result:
        print("ERROR: Could not create download properties for parameters")
        return False

    # Get Pylance to stop complaining
    assert download_parameters_properties is not None

    result, download_simulator_properties = download_data.BaseUrlAndFilenames.create_from_config(
        config_download_simulator_base_url, config_download_simulator_executable
    )
    if not result:
        print("ERROR: Could not create download properties for simulator executable")
        return False

    # Get Pylance to stop complaining
    assert download_simulator_properties is not None

    if len(config_download_simulator_filenames) > 0:
        result, download_simulator_support_properties = (
            download_data.BaseUrlAndFilenames.create_from_config(
                config_download_simulator_base_url, config_download_simulator_filenames
            )
        )
        if not result:
            print("ERROR: Could not create download properties for simulator support files")
            return False

        download_simulator_properties.names += download_simulator_support_properties.names

    print("Downloading parameters")
    result = download.download_and_save(download_parameters_properties, local_directory)
    if not result:
        print("ERROR: Could not download parameters")
        return False

    print("Downloading simulator")
    result = download.download_and_save(download_simulator_properties, local_directory)
    if not result:
        print("ERROR: Could not download simulator")
        return False

    print("Simulator downloaded!")

    return True


def run_executables(
    simulator_directory: pathlib.Path,
    simulator_executable_name: str,
    simulator_options: list[str],
) -> bool:
    """
    Run simulator.
    """
    os.chdir(simulator_directory)

    # Non blocking operation
    # pylint: disable-next=consider-using-with
    simulator_process = subprocess.Popen(
        [simulator_executable_name] + simulator_options, stdout=subprocess.PIPE
    )

    while True:
        output = simulator_process.stdout.readline()
        if output:
            print(output.decode(encoding="utf-8").strip("\r\n"))

        simulator_process_return_code = simulator_process.poll()
        if simulator_process_return_code is not None:
            print(f"Simulator ended with return code: {simulator_process_return_code}")
            break

    return True


def main() -> int:
    """
    Main function.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Option to overwrite existing simulator",
    )

    # Simulator options
    parser.add_argument(
        "-M",
        action="store",
        default="+",
        help="Simulator option",
    )
    parser.add_argument(
        "--home",
        action="store",
        default="43.472978,-80.540103,336,0",
        help="Simulator option",
    )
    parser.add_argument(
        "--defaults",
        action="store",
        default="copter.parm",
        help="Simulator option",
    )

    args = parser.parse_args()

    simulator_options = [
        "-M",
        args.M,
        f"--home={args.home}",
        "--defaults",
        args.defaults,
    ]
    print(simulator_options)

    result, os_type = platform.get_os()
    if not result:
        print("ERROR: Could not get OS type")
        return -1

    result, config = read_yaml.open_config(CONFIG_FILE_PATH)
    if not result:
        print(f"ERROR: Could not open config: {CONFIG_FILE_PATH}")
        return -1

    # Get Pylance to stop complaining
    assert config is not None

    # Get settings
    try:
        config_download = config["download"]

        config_download_local_directory = config_download["local_directory"]

        config_download_parameters_base_url = config_download["parameters"]["base_url"]
        config_download_parameters_filenames = config_download["parameters"]["file_list"]

        config_download_os_key = (
            "windows"
            if os_type == platform.OperatingSystem.WINDOWS
            else (
                "unix"
                if os_type == platform.OperatingSystem.UNIX
                else "ERROR: OS value not in the enumeration list"
            )
        )

        config_download_simulator_base_url = config_download[config_download_os_key]["base_url"]
        config_download_simulator_executable = config_download[config_download_os_key]["executable"]
        config_download_simulator_filenames = config_download[config_download_os_key]["file_list"]
    # Catching all exceptions for library call
    # pylint: disable-next=broad-exception-caught
    except Exception as exception:
        print(f"ERROR: Could not open configs: {exception}")
        return -1

    simulator_directory = pathlib.Path(config_download_local_directory)
    if not args.overwrite and simulator_directory.exists():
        print(f"Found directory, skipping download: {simulator_directory}")
    else:
        simulator_directory.mkdir(parents=True, exist_ok=True)
        result = download_simulator(
            simulator_directory,
            config_download_parameters_base_url,
            config_download_parameters_filenames,
            config_download_simulator_base_url,
            config_download_simulator_executable,
            config_download_simulator_filenames,
        )
        if not result:
            print("ERROR: Could not download simulator")
            return -1

    simulator_executable_name = config_download_simulator_executable[0][1]

    result = run_executables(
        pathlib.Path(simulator_directory), simulator_executable_name, simulator_options
    )
    if not result:
        print("ERROR: Could not run programs")
        return -1

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main != 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
