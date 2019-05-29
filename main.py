from LZWFile import *
from LZWImage import *


def getFileExtension(file_path):
	return file_path[file_path.index('.') + 1 :]

def getFileName(file_path):
	index = -1

	for i in range(len(file_path)):
		if file_path[i] == '/':
			index = i
		elif file_path[i] == '.':
			return file_path[index + 1 : i]

	# return 'ERROR: ' + file_path + ' does not exist'

def getFileDetails(file_path):
	details = {
		'filePath': file_path,
		'fileName': getFileName(file_path),
		'fileExt': getFileExtension(file_path),
		'lastAccessed': time.ctime(os.path.getatime(file_path)),
		'lastModified': time.ctime(os.path.getmtime(file_path)),
		'created': time.ctime(os.path.getctime(file_path)),
		'size': os.path.getsize(file_path)}

	return details
	# print(getFileName(file_path))
	# print(getFileExtension(file_path))
	# print(time.ctime(os.path.getatime(file_path)))
	# print(time.ctime(os.path.getmtime(file_path)))
	# print(time.ctime(os.path.getctime(file_path)))
	# print(os.path.getsize(file_path))


if __name__ == '__main__':
	details = getFileDetails(sys.argv[1])

	if details['fileExt'] == 'txt':
		LZWFile().compress(details['filePath'])

	elif details['fileExt'] == 'lzw':
		LZWFile().decompress(details['filePath'])

	elif details['fileExt'] == 'tif':
		LZWImage(details['filePath']).compress()

	elif details['fileExt'] == 'lzwimg':
		LZWImage(details['filePath']).decompress()

