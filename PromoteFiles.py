import sys
import time
# consider ntpath
import os
from watchdog.utils.dirsnapshot import DirectorySnapshot
from watchdog.utils.dirsnapshot import DirectorySnapshotDiff

if __name__ == "__main__":

	path = '.'

	if not os.path.exists('./snapshot.dat'):
		with open('./snapshot.dat', 'a'): pass			# do I have to close this?

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

				# I feel like I shouldn't need to do this...
				elif ("./snapshot.dat" in diff.files_modified):
					print("handle this case!")

				else:
					#print(diff.files_modified)
					# Created files
					for file in diff.files_created:
						if (file.endswith(".txt")):
							print(file + " has been created.")
						else:
							print("A new file has been created in this directory, but this change is not promotable because only .txt files are supported by this application.")

					# Modified files
					for file in diff.files_modified:	# add case for when file name is ./snapshot.txt
						if (file.endswith(".txt")):
							print(file + " has been modified.")
						else:
							print("A new file has been modified in this directory, but this change is not promotable because only .txt files are supported by this application.")

					snapshot = current

					# Save snapshot to file
					file = open('./snapshot.dat', 'w')
					file.write(str(snapshot))
					file.close()

	except KeyboardInterrupt:
		snapshot.stop()
	snapshot.join()
