import os
import sys
from main import *

class Downloader:
	def __init__(self):
		self.dstn = '/Users/arnav/Desktop/'

	def download(self, file_path):
		os.rename(file_path, self.dstn + getFileName(file_path) + '.' + getFileExtension(file_path))

if __name__ == '__main__':
	dwnldr = Downloader()
	dwnldr.download(sys.argv[1])