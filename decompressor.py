from struct import *
import sys
import os
import time
from file_manip import *


DB_DECOMP = '/Users/arnav/Desktop/Projects/ElectronAppDS/DB_DECOMP/'

def decompress(input_file):
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
	output_file_path = DB_DECOMP + out + '_decoded.txt'
	output_file = open(output_file_path, "w")

	for data in decompressed_data:
	    output_file.write(data)

	    
	print ("File uncompressed and saved at " + output_file.name)
	print (str(os.path.getsize(input_file)))
	print (str(os.path.getsize(output_file_path)))


	output_file.close()
	file.close()

decompress(sys.argv[1])