import sys
import time
import os
from watchdog.utils.dirsnapshot import DirectorySnapshot
from watchdog.utils.dirsnapshot import DirectorySnapshotDiff

if __name__ == "__main__":

	path = '.'

	# Note:  does os.path work on Windows?
	if not os.path.exists('./snapshot.dat'):
		with open('./snapshot.dat', 'a'): pass			# do I have to close this?

	# Take a snapshot
	snapshot = DirectorySnapshot(path, recursive=True)

	try:
		while True:
			time.sleep(1)
			userInput = input()
			if (userInput == "promote"):

				# Get the current image and compare with snapshot
				current = DirectorySnapshot(path, recursive=True)
				diff = DirectorySnapshotDiff(snapshot, current)

				# Case when promotable items are available
				if ((len(diff.files_created) > 0 or len(diff.files_modified) > 0) and not (len(diff.files_modified) == 1 and "./snapshot.dat" in diff.files_modified)):

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
					file = open('./snapshot.dat', 'w')
					file.write(str(snapshot))
					file.close()

				else:
					print("No promotable changes have been made since the last promotion.")

	except KeyboardInterrupt:
		snapshot.stop()
	snapshot.join()
