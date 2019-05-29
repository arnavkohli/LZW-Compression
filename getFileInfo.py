import sys
import os
import time

def getFileExtension(file_path):
	return file_path[file_path.index('.') + 1 :]

def getFileName(file_path):
	index = -1

	for i in range(len(file_path)):
		if file_path[i] == '/':
			index = i
		elif file_path[i] == '.':
			return file_path[index + 1 : i]

def getFileDetails(file_path):
	print(getFileName(file_path))
	print(getFileExtension(file_path))
	print(time.ctime(os.path.getatime(file_path)))
	print(time.ctime(os.path.getmtime(file_path)))
	print(time.ctime(os.path.getctime(file_path)))
	print(os.path.getsize(file_path))

getFileDetails(sys.argv[1])