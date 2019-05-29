from struct import *
import sys
import os
import time
from getFileInfo import *


class LZWFile:
	def __init__(self):
		self.DB_COMP = '/Users/arnav/Desktop/Projects/ElectronAppDS/DB_COMP/'
		self.DB_DECOMP = '/Users/arnav/Desktop/Projects/ElectronAppDS/DB_DECOMP/'

	def compress(self, input_file):
		file = open(input_file)
		data = file.read()

		dictionary_size = 256 #ASCII
		dictionary = {chr(i) : i for i in range(dictionary_size)}

		compressed_data = []
		string = ""

		# print ("Compressing data....")
		for data_element in data:

			updated_string = string + data_element

			if updated_string in dictionary:
				string = updated_string

			else:
				compressed_data.append(dictionary[string])
				dictionary[updated_string] = dictionary_size
				dictionary_size += 1
				string = data_element

		if string in dictionary:
			compressed_data.append(dictionary[string])


		file_name = getFileName(input_file)

		lzw_file_name = file_name + '.lzw'
		lzw_file_path = self.DB_COMP + lzw_file_name
		lzw_file = open(lzw_file_path, 'wb')

		for data in compressed_data:
			lzw_file.write(pack('>H', int(data)))

		# print ("File compressed and saved as " + lzw_file_name)
		print (lzw_file_path)
		print (str(os.path.getsize(input_file)))
		print (str(os.path.getsize(lzw_file_path)))

		lzw_file.close()
		file.close()

	def decompress(self, input_file):
		file = open(input_file, "rb")
		compressed_data = []
		next_code = 256
		decompressed_data = ""
		string = ""


		while True:
		    rec = file.read(2)
		    if len(rec) != 2:
		        break
		    (data, ) = unpack('>H', rec)
		    compressed_data.append(data)


		dictionary_size = 256
		dictionary = dict([(x, chr(x)) for x in range(dictionary_size)])

		# print ("Uncompressing file...")

		for code in compressed_data:
		    if not (code in dictionary):
		        dictionary[code] = string + (string[0])
		    decompressed_data += dictionary[code]
		    if not(len(string) == 0):
		        dictionary[next_code] = string + (dictionary[code][0])
		        next_code += 1
		    string = dictionary[code]

		out = getFileName(input_file)
		output_file_path = self.DB_DECOMP + out + '_decoded.txt'
		output_file = open(output_file_path, "w")

		for data in decompressed_data:
		    output_file.write(data)

		    
		# print ("File uncompressed and saved at " + output_file.name)
		print (output_file_path)
		print (str(os.path.getsize(input_file)))
		print (str(os.path.getsize(output_file_path)))


		output_file.close()
		file.close()