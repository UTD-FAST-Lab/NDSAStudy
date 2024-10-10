# NDDetector

NDDetector (Nondeterminism detector) is a flexible tool that can be used to detect nondeterministic behaviors in configurable static analysis on a variety of benchmarks.
NDDetector can be extended to use alternative analyses, but currently, it can run 
call graph analyses on WALA, SOOT, DOOP, TAJS, PyCG, and Code2Flow, as well as taint analysis on Android applications using FlowDroid, AmanDroid, and DroidSafe.

# Prerequisites
This application is written for Python version 3.10.0, and is intended to be run on a Linux machine. We have tested this artifact on Ubuntu 20.04.Furthermore, 
NDDetector runs its analyses in Docker containers in order to maintain consistent
environments across runs, so you must have a working Docker installation.

# Usage

We recommend creating a virtual environment for NDDetector. To do so, run

`python -m venv <name_of_virtual_environment>`

where 'python' points to a Python 3.10 installation. This will create a new folder. If, for example, you named your folder 'venv', then
you can activate it as follows:

`source ./venv/bin/activate`

This will cause `python` to point to the version that you used to create the virtual environment.

In order to install NDDetector’s dependencies, from the root directory of the repository, run

`python -m pip install -r requirements.txt`

This will install all of the Python dependencies required. Then, in order to install
the application, run

`python -m pip install -e .`

We require the `-e` to be built in-place. Currently, omitting this option will cause the Dockerfile resolution to fail when we try to build tool-specific images.

This installation will put two executables on your system PATH: `dispatcher`, and `tester`. `dispatcher` is the command you run from your host, while `tester` is the command you run from inside the Docker container (under normal usage, a user
will never invoke `tester` themselves, but it can be useful for debugging to skip
container creation.)

Simply run `dispatcher --help` from anywhere in order to see the help doc on how to
invoke NDDetector.
