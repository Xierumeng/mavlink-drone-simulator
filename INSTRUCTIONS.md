# Instructions

## Setup

Tested with Python 3.12 .

1. Clone the repository and `cd` into the directory
1. Create a virtual environment:
    1. `python -m venv venv/`
1. Activate the virtual environment with 1 of the following:
    * Windows command prompt: `venv\Scripts\activate.bat`
    * Windows PowerShell: `venv/Scripts/Activate.ps1`
    * MacOS and Linux: `source venv/bin/activate`
1. You should now see `(venv)` in your terminal
1. Install required packages:
    1. `pip install -r requirements.txt`

## Usage

1. Activate the virtual environment if it isn't already activated
1. Run the program:
    1. `python -m main`
1. The simulator is ready to be used: https://ardupilot.org/dev/docs/sitl-simulator-software-in-the-loop.html
1. Repeat the above steps until you are done
1. Deactivate the virtual environment with 1 of the following:
    * Close the terminal
    * Windows command prompt: `venv\Scripts\deactivate.bat`
    * Everything else: `deactivate`

Common errors:

| Error                    | Solution                         |
|--------------------------|----------------------------------|
| Port 5760 already in use | Kill the process using port 5760 |

### MAVProxy

Tested on Windows 10 and Ubuntu 24.04 .

If you don't have an existing GUI program nor MAVProxy installed, you can install MAVProxy through `pip` .

1. Activate the virtual environment if it isn't already activated
1. Install required packages:
    * Windows and MacOS:
        1. `pip install -r requirements_mavproxy.txt`
    * Linux without MAVProxy GUI:
        1. `pip install mavproxy`
    * Linux with MAVProxy GUI:
        1. TODO: Cannot get Linux GUI to work
        1. `wxPython` does not have precompiled binaries for Linux. More information: https://wxpython.org/pages/downloads/

Run MAVProxy:
1. Run the program
1. Run MAVProxy:
    1. `mavproxy.py --master tcp:127.0.0.1:5760 --sitl 127.0.0.1:5501 --out 127.0.0.1:14550`
1. Repeat the above steps until you are done
1. Deactivate the virtual environment

More information: https://ardupilot.org/mavproxy/

Common errors:

| Error                        | Solution                                      |
|------------------------------|-----------------------------------------------|
| Connection could not be made | Start the simulator (ideally before MAVProxy) |
