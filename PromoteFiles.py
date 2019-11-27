import sys
import time
import os
import dill	# pickle does not support lambda functions
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

				# Get the current image and compare with snapshot
				current = DirectorySnapshot('.', recursive = True)
				diff = DirectorySnapshotDiff(snapshot, current)

				# Case when promotable items are available
				if (len(diff.files_created) > 0 or len(diff.files_modified) > 0):

					scriptOrSnapshotChanged = False

					# Created files
					for fileName in diff.files_created:
						if (fileName.endswith(".txt")):
							if (validateFormat(fileName)):
								file = open("./" + fileName, "r")
								if file.mode == 'r':
									contents = file.read()
								file.close()
								data = {'name': fileName.replace("./", ""), 'contents': contents}	# FIXME?
								response = requests.post('http://localhost:8080/home/add/', data=data)
								print(fileName + " has been created.")
						elif (fileName.endswith("snapshot.pkl") or fileName.endswith("PromoteFiles.py")):
							scriptOrSnapshotChanged = True
						else:
							print("A new file has been created in this directory, but this change is not promotable because only .txt files are supported by this application.")

					# Modified files
					for fileName in diff.files_modified:
						if (fileName.endswith(".txt")):
							if (validateFormat(fileName)):
								file = open("./" + fileName, "r")
								if file.mode == 'r':
									contents = file.read()
								file.close()
								data = {'name': fileName.replace("./", ""), 'contents': contents}	# FIXME?
								response = requests.post('http://localhost:8080/home/add/', data=data)
								print(fileName + " has been modified.")
						elif (fileName.endswith("snapshot.pkl") or fileName.endswith("PromoteFiles.py")):
							scriptOrSnapshotChanged = True
						else:
							print("A new file has been created in this directory, but this change is not promotable because only .txt files are supported by this application.")

					if (scriptOrSnapshotChanged):
						print("No promotable changes have been made since the last promotion.")	

					snapshot = current

				else:
					print("No promotable changes have been made since the last promotion.")

	except KeyboardInterrupt:
		# Save snapshot to file
		file = open('./snapshot.pkl', 'wb')
		dill.dump(snapshot, file)
		file.close()

		print("")

def validateFormat(fileName):
	if not (re.search("([A-Z][a-z]*)*[_][0-9]+", fileName)):
		print("Please use the input format:\n\tRuleType_###\nor consult the official documentation.")
		return False;
	return True;

if __name__ == "__main__":
	run()
