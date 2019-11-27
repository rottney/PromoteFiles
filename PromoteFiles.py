import sys
import time
import os
import dill
import re
import requests
from watchdog.utils.dirsnapshot import DirectorySnapshot
from watchdog.utils.dirsnapshot import DirectorySnapshotDiff

def run():
	# Note:  does os.path work on Windows?
	if not os.path.exists('./snapshot.pkl'):		
		with open('./snapshot.pkl', 'w') as file: pass	# why is this w not wb
		snapshot = DirectorySnapshot('.', recursive = True)
		file = open('./snapshot.pkl', 'wb')
		dill.dump(snapshot, file)
		file.close()
	else:
		with open('./snapshot.pkl', 'rb') as file:
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

	except KeyboardInterrupt:
		# Save snapshot to file
		file = open('./snapshot.pkl', 'wb')
		dill.dump(snapshot, file)
		file.close()

		print("")

def analyzeDiff(fileName, changeType):
	if (fileName.endswith(".txt")):
		if (validateFormat(fileName)):
			file = open("./" + fileName, "r")
			if file.mode == 'r':
				contents = file.read()
			file.close()
			data = {'name': fileName.replace("./", ""), 'contents': contents}
			requests.post('http://localhost:8080/home/add/', data=data)
			print(fileName.replace("./", "") + " has been " + changeType + ".")
	elif (fileName.endswith("snapshot.pkl") or fileName.endswith("PromoteFiles.py")):
		global scriptOrSnapshotChanged
		scriptOrSnapshotChanged = True
	else:
		print("A new file has been " + changeType + " in this directory, " + 
			"but this change is not promotable because only .txt files are supported by this application.")

def validateFormat(fileName):
	if not (re.search("([A-Z][a-z]*)*[_][0-9]+", fileName)):
		print("Please use the input format:\n\tRuleType_###\nor consult the official documentation.")
		return False;
	return True;

if __name__ == "__main__":
	run()
