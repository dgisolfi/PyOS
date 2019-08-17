# PyOS [![Py-OS version](https://img.shields.io/pypi/v/Py-OS.svg)](https://pypi.org/project/Py-OS)
An OS that runs a subset of the 6502 opcodes, implemented in python. 

## About

This is a python port of a Typescript OS I created for the Fall 2018 Operating Systems class. The Base OS for that class was provided and can be found [here](https://github.com/AlanClasses/TSOS). A direct port of the Base OS in python can be found under releases as version 1.0.0

## Setup
To run the OS it must be installed. It can be installed either from pypi or from the source code of the directory.

### From PyPi

Simply use pip to install the [latest release](https://pypi.org/project/PyOS/) of the PyOS. To do so run `pip install PyOS`. 

### From Source

Either in a Python Virtual Environment or just on your machine in the root of the directory run `make install` this will install the PyOS from the source code in the repo using the setup.py file. If you would like to uninstall simply run `make uninstall`

## Running

To run the OS run, `python3 -m PyOS`

## Releases

[1.0.0](https://github.com/dgisolfi/PyOS/tree/BaseOS) - Base OS

## Developing

To develop the PyOS it would be a nuisance to install each time a change is made, to avoid this use a python virtual environment. To create a Virtual environment or venv use the following command `python3 -m venv/path/to/new/virtual/environment` The path should be pointed at this repository. To enter a venv that already exists navigate to the bin dir inside of env and run `source activate`. In the case of this repo the command would look like this, `source ./env/bin/activate`.

Once in a venv to run the PyOS without installing use the following format: `python3 PyOS /path/to/source/file` while in the root of the directory.

## Testing

Coming Soon... 

## Publishing to PyPi

To publish the latest release of the build to pypi run the following recipe: `make release`. This will test, build and publish the release to pypi.