# PromoteFiles
CLI app to promote text files to a [remote server](https://github.com/rottney/RuleSheetServer)


**UPDATE:**
The server is currently turned off due to AWS free tier restrictions.  To turn back on, please contact the maintainer at rottney123@gmail.com.
----------------------------------------------------------------


**SUMMARY:**
When run, this script monitors its parent directory for file changes.
Eligible files are automatically "promoted" to one of three remote clusters at the user's discresion.
When closed, this application stores a directory snapshot so that any changes in between runs are remembered.


**INSTALLATION:**
Clone [this repo](https://github.com/rottney/PromoteFiles.git) into a directory of your choice.
If not already installed, please install the following using your favorite Python package manager:
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
"Eligible files" in this context are of the form:

\<RuleType>\_\<CustomerID>\.txt

where RuleType is one of the following:
1. ExpenseRouting
2. Compliance
3. SubmitCompliance

and CustomerID is an integer between 0 and 1499, inclusive.
These files must be in the **exact** same directory as the script PromoteFiles.py (not a subdirectory therein).

The files may contain any text.  Emojis will be removed from the files' contents before they are stored on the servers.

The files will be routed to the appropriate servers based on CustomerID:
* 0 to 499 (incl.):  [cluster 1](http://cluster1.3dpqdi6p3x.us-west-2.elasticbeanstalk.com/home/view)
* 500 to 999 (incl.):  [cluster 2](http://cluster2.3dpqdi6p3x.us-west-2.elasticbeanstalk.com/home/view)
* 1000 to 1499 (incl.):  [cluster 3](http://cluster3.3dpqdi6p3x.us-west-2.elasticbeanstalk.com/home/view)

Any eligible files will be promoted and a success message stating the file name and version number will be printed to the command line.  Please see the [server documentation](https://github.com/rottney/RuleSheetServer/blob/master/README.md) for details about versioning.  File promotions may be tested using the links provided above:  please note that only the 10 most recent entries on each cluster will be returned in each view (unless fewer than 10 entries exist in the cluster, in which case all entries will be returned).
Any ineligible files will not be promoted, and a message stating why the files are ineligble will be printed to the command line.


**NOTE:**
Please do not modify the "snapshot.pkl" file created after running this script; this is used for serialization.
