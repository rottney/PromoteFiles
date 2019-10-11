import sys
import time
import os
from watchdog.utils.dirsnapshot import DirectorySnapshot
from watchdog.utils.dirsnapshot import DirectorySnapshotDiff

if __name__ == "__main__":

	path = '.'

	# NOTE:  This part is not gonna work on Windows...
	if not os.path.exists('./snapshot.txt'):
		with open('./snapshot.txt', 'a'): pass	# do I have to close this?

	snapshot = DirectorySnapshot(path, recursive=True)

	try:
		while True:
			time.sleep(1)
			userInput = input()
			if (userInput == "promote"):
				current = DirectorySnapshot(path, recursive=True)
				diff = DirectorySnapshotDiff(snapshot, current)

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
						print("A new file has been modified in this directory, but this change is not promotable because only .txt files are supported by this application.")

				snapshot = current
				# I don't know...
				file = open('./snapshot.txt', 'a')
				file.write(str(snapshot))	# do I have to close this?
				print("made it here, oops lol")

	except KeyboardInterrupt:
		snapshot.stop()
	snapshot.join()
