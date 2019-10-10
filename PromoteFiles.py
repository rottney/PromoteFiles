import sys
import time
import os
from watchdog.utils.dirsnapshot import DirectorySnapshot
from watchdog.utils.dirsnapshot import DirectorySnapshotDiff

if __name__ == "__main__":

	path = sys.argv[1] if len(sys.argv) > 1 else '.'
	ref = DirectorySnapshot(path, recursive=True)

	try:
		while True:
			time.sleep(1)
			userInput = input()
			if (userInput == "promote"):
				snapshot = DirectorySnapshot(path, recursive=True)
				diff = DirectorySnapshotDiff(ref, snapshot)
				
				# Case when no promotable changes have been made
				if (len(diff.files_created) == 0 and len(diff.files_modified) == 0):
					print("No promotable changes have been made since the last promotion.")

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
						print("Only .txt files are supported by this application.")

				ref = snapshot
	except KeyboardInterrupt:
		ref.stop()
	ref.join()
