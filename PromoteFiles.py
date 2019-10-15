# NOTE:  the serialization still does not work...
import sys
import time
import os
import dill	# pickle does not support lambda functions
from watchdog.utils.dirsnapshot import DirectorySnapshot
from watchdog.utils.dirsnapshot import DirectorySnapshotDiff

if __name__ == "__main__":

	# Note:  does os.path work on Windows?
	if not os.path.exists('./snapshot.pkl'):		
		with open('./snapshot.pkl', 'w') as file: pass
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
				if ((len(diff.files_created) > 0 or len(diff.files_modified) > 0) and not (len(diff.files_modified) == 1 and "./snapshot.pkl" in diff.files_modified)):	# this logic is still fucky

					# Created files
					for file in diff.files_created:
						if (file.endswith(".txt")):
							print(file + " has been created.")
						else:
							print("A new file has been created in this directory, but this change is not promotable because only .txt files are supported by this application.")

					# Modified files
					for file in diff.files_modified:
						if (file.endswith(".txt")):
							print(file + " has been modified.")
						else:
							print("A new file has been modified in this directory, but this change is not promotable because only .txt files are supported by this application.")

					snapshot = current

					# Save snapshot to file
					#file = open('./snapshot.pkl', 'w')
					#file.write(str(snapshot))
					#file.close()

				else:
					print("No promotable changes have been made since the last promotion.")

	except KeyboardInterrupt:
		# Save snapshot to file
		file = open('./snapshot.pkl', 'w')
		file.write(str(snapshot))
		file.close()

		snapshot.stop()
	snapshot.join()
