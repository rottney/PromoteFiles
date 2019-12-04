# PromoteFiles
CLI app to promote text files to a remote server


**SUMMARY:**
When run, this script monitors its parent directory for file changes.
Eligible files are automatically "promoted" to one of three remote clusters at the user's discresion.
When closed, this application stores a directory snapshot so that any changes in between runs are remembered.


**INSTALLATION:**
Clone [this repo](https://github.com/rottney/PromoteFiles.git) into a directory of your choice.
If not already installed, please install the following using your favorite package manager:
* python3
* dill
* requests
* watchdog


**USAGE:**
Using the terminal, browse to the directory in which `PromoteFiles.py` is located.
To run, type ```python3 PromoteFiles.py``` into the terminal.
To promote eligible files, type `promote` in the terminal while the script is running.
Type `exit` or CTRL + `C` to terminate the program.


**RULES:**
"Eligible files" in this context are of the form

<RuleType>_<CustomerID>.txt

where RuleType is one of the following:
1. ExpenseRouting
2. Compliance
3. SubmitCompliance
and CustomerID is an integer between 0 and 1499, inclusive.

The files may contain any text.  Emojis will be removed from the files' contents before they are stored on the servers.

If CustomerID is between 0 and 499 (incl.), the file will be routed to [cluster 1](http://cluster1.3dpqdi6p3x.us-west-2.elasticbeanstalk.com/home/view).

If CustomerID is between 500 and 999 (incl.), the file will be routed to [cluster 2](http://cluster2.3dpqdi6p3x.us-west-2.elasticbeanstalk.com/home/view).

If CustomerID is between 1000 and 1499 (incl.), the file will be routed to [cluster 3](http://cluster3.3dpqdi6p3x.us-west-2.elasticbeanstalk.com/home/view).

Any eligible files will be promoted and a success message stating the file name and version number will be printed to the command line.  Please see the [server documentation] for details about versioning.  File promotions may be tested using the links provided above:  please note that only the 10 most recent entries on each server will be returned in the view.
Any "ineligible" files will be validated and a message stating why the files are ineligble will be printed to the command line.
