from struct import *
import sys
import os
import time
from file_manip import *

DB_COMP = '/Users/arnav/Desktop/Projects/ElectronAppDS/DB_COMP/'
# DB_UNCOMP = 'file_db/uncompressed/'
# print ("OLD SIZE: " + str(os.path.getsize(input_file)) + " bytes; " + "NEW SIZE: " + str(os.path.getsize(lzw_file_path)) + ' bytes')

def compress(input_file):
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
	lzw_file_path = DB_COMP + lzw_file_name
	lzw_file = open(lzw_file_path, 'wb')

	for data in compressed_data:
		lzw_file.write(pack('>H', int(data)))

	print ("File compressed and saved as " + lzw_file_name)
	print (str(os.path.getsize(input_file)))
	print (str(os.path.getsize(lzw_file_path)))

	lzw_file.close()
	file.close()

compress(sys.argv[1])
