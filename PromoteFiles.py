import sys
import time
import ntpath
from watchdog.utils.dirsnapshot import DirectorySnapshot
from watchdog.utils.dirsnapshot import DirectorySnapshotDiff

if __name__ == "__main__":

	path = '.'

	#	KNOWN ISSUE:  There's one caveat: Linux filenames may contain backslashes.
	#	So on linux, r'a/b\c' always refers to the file b\c in the a folder,
	#	while on Windows, it always refers to the c file in the b subfolder of the a folder.
	#	So when both forward and backward slashes are used in a path,
	#	you need to know the associated platform to be able to interpret it correctly.

	#	https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
	if not ntpath.exists('./snapshot.txt'):
		with open('./snapshot.txt', 'a'): pass			# do I have to close this?

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
				else:
					# Created files
					for file in diff.files_created:
						if (file.endswith(".txt")):		# add case for when file name is ./snapshot.txt
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
					file = open('./snapshot.txt', 'w')
					file.write(str(snapshot))
					file.close()

	except KeyboardInterrupt:
		snapshot.stop()
	snapshot.join()
