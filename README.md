# PromoteFiles
CLI app to promote text files to a remote server


SUMMARY:
When run, this script monitors its parent directory for file changes.
Eligible files are automatically "promoted" to one of three remote clusters at the user's discresion.
When closed, this application stores a directory snapshot so that any changes in between runs are remembered.

INSTALLATION:
Clone this repo into a directory of your choice.
If not already installed, please install the following using your favorite package manager:
* python3
* dill
* requests
* watchdog


