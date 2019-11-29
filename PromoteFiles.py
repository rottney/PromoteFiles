import sys
import time
import os
import dill
import re
import requests
from watchdog.utils.dirsnapshot import DirectorySnapshot
from watchdog.utils.dirsnapshot import DirectorySnapshotDiff
from requests.exceptions import ConnectionError

def run():
	help()

	# Note:  does os.path work on Windows?
	if not os.path.exists("./snapshot.pkl"):		
		with open("./snapshot.pkl", "w") as file: pass	# why is this w not wb
		snapshot = DirectorySnapshot(".", recursive = True)
		file = open("./snapshot.pkl", "wb")
		dill.dump(snapshot, file)
		file.close()

	else:
		with open("./snapshot.pkl", "rb") as file:
			snapshot = dill.load(file)
			file.close()

	try:
		while True:
			time.sleep(1)
			userInput = input()

			if (userInput == "promote"):
				current = DirectorySnapshot('.', recursive = True)
				diff = DirectorySnapshotDiff(snapshot, current)

				if ((len(diff.files_created) > 0 or len(diff.files_modified) > 0)):
					global scriptOrSnapshotChanged
					scriptOrSnapshotChanged = False

					for fileName in diff.files_created:
						analyzeDiff(fileName, "created")

					for fileName in diff.files_modified:
						analyzeDiff(fileName, "modified")

					if (scriptOrSnapshotChanged):
						print("Utility files have changed on disk, but these changes are not promotable.")

					snapshot = current

				else:
					print("No promotable changes have been made in this directory since the last promotion.")

			if (userInput == "help"):
				help()

			if (userInput == "exit"):
				file = open("./snapshot.pkl", "wb")
				dill.dump(snapshot, file)
				file.close()

				print("")
				sys.exit(0)

	except KeyboardInterrupt:
		# Save snapshot to file
		file = open("./snapshot.pkl", "wb")
		dill.dump(snapshot, file)
		file.close()

		print("")

def analyzeDiff(fileName, changeType):
	if (fileName.endswith(".txt")):

		if (validateFormat(fileName)):
			file = open("./" + fileName, "r")

			if file.mode == "r":
				contents = file.read()

			file.close()

			data = {"name": fileName.replace("./", ""), "contents": contents}
			routeFile(fileName)
			sendRequest("http://localhost:8080", data)

	elif (fileName.endswith("snapshot.pkl") or fileName.endswith("PromoteFiles.py")):
		global scriptOrSnapshotChanged
		scriptOrSnapshotChanged = True

	else:
		print("A new file has been " + changeType + " in this directory, " + 
			"but this change is not promotable because only .txt files are supported " + 
			"by this application, or because the file in question has been deleted.")

def validateFormat(fileName):
	if not (re.search("([A-Z][a-z]*)*[_][0-9]+", fileName)):
		print("Please use the input format:\nRuleType_###\nor consult the official documentation.")
		return False;

	return True;

def routeFile(fileName):
	customerID = int(fileName.split("_")[1].split(".txt")[0])

	if (0 <= customerID and customerID <= 499):
		print("Route to Server 1.")

	elif (500 <= customerID and customerID <= 1001):
		print("Route to Server 2.")

	elif (1000 <= customerID and customerID <= 1499):
		print("Route to Server 3.")

	else:
		print("Your CustomerID is out of range.  We only support values between 0 and 1499.")

def sendRequest(domain, data):
	try:
		r = requests.post(domain + "/home/add/", data=data)
		print(r.text)
	except ConnectionError:
		print("The server is off!  Please contact the maintainer at github.com/rottney.\n" + 
			"Please re-save the file " + data.get("name").replace("./", "") + 
			" before your next promotion attempt.")

def help():
	print("\nUsage: type 'promote', and all promotable files within your local directory:\n" + 
		os.path.abspath("./") + "\nwill be promoted to the appropriate servers.\n" + 
		"Type 'exit' or CTRL + 'C' to exit this program.\nType 'help' to repeat this information.\n")

if __name__ == "__main__":
	run()
