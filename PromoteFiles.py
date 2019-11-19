import sys
import time
import os
import dill	# pickle does not support lambda functions
import re
from watchdog.utils.dirsnapshot import DirectorySnapshot
from watchdog.utils.dirsnapshot import DirectorySnapshotDiff

def parseFileName(fileName):
	if not (re.search("([A-Z][a-z]*)*[_][0-9]+", fileName)):
		print("Please use the input format:\n\tRuleType_###\nor consult the official documentation.")
	else:
		print(fileName + " is well-formatted.  Wow-zoo!!!")
	

if __name__ == "__main__":

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

					# Created files
					for file in diff.files_created:
						if (file.endswith(".txt")):
							parseFileName(file)
							print(file + " has been created.")
						elif (file.endswith(".pkl")):
							print("just the diff [created], handle this")
						elif (file.endswith(".py")):
							print("this is the python file, handle this...")
						else:
							print("A new file has been created in this directory, but this change is not promotable because only .txt files are supported by this application.")
							print("that file's name is " + file + " and I don't know why the freak it has been modified...")

					# Modified files
					for file in diff.files_modified:
						if (file.endswith(".txt")):
							parseFileName(file)
							print(file + " has been modified.")
						elif (file.endswith(".pkl")):
							print("just the diff [modified], handle this")
						elif (file.endswith(".py")):
							print("this is the python file, handle this...")
						else:
							print("A new file has been modified in this directory, but this change is not promotable because only .txt files are supported by this application.")
							print("that file's name is " + file + " and I don't know why the freak it has been modified...")

					snapshot = current

				else:
					print("No promotable changes have been made since the last promotion.")

	except KeyboardInterrupt:
		# Save snapshot to file
		file = open('./snapshot.pkl', 'wb')
		#file.write(str(snapshot))
		dill.dump(snapshot, file)
		file.close()

		#snapshot.stop()	# Do I need this lol

	#snapshot.join()		# Do I need this lol
