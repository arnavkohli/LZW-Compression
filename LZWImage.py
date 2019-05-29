from PIL import Image
import os
import sys
from getFileInfo import *

class LZWImage:
	def __init__(self, path):
		self.path = path
		self.compressionDictionary, self.compressionIndex = self.createCompressionDict()
		self.decompressionDictionary, self.decompressionIndex = self.createDecompressionDict()

	def setImageSize(self):
		dimensions = self.image.size
		height, width = dimensions
		return height,width

	def processImage(self):
		image = self.image.convert('RGB')
		red, green, blue = [], [], []
		pixel_values = list(image.getdata())
		iterator = 0
		for height_index in range(self.height):
			R, G, B = "","",""
			for width_index in range(self.width):
				RGB = pixel_values[iterator]
				R = R + str(RGB[0]) + ","
				G = G + str(RGB[1]) + ","
				B = B + str(RGB[2]) + ","
				iterator+=1

			red.append(R[:-1])
			green.append(G[:-1])
			blue.append(B[:-1])

		return red,green,blue

	def printPixels(self):
		self.initCompress()
		add = [self.red,self.green,self.blue]
		with open("mainpixel1.txt",'w') as file:
			for y in add:
				for x in y:
					file.write(x)
					file.write('\n')

	def createCompressionDict(self):
		dictionary = {}
		for i in range(10):
			dictionary[str(i)] = i
		dictionary[','] = 10
		return dictionary,11

	def createDecompressionDict(self):
		dictionary = {}
		for i in range(10):
			dictionary[i] = str(i)
		dictionary[10] = ','
		return dictionary,11

	def printDict(self):
		# print("---------------------------------Dictionary---------------------------------")
		for x in list(self.decompressionDictionary)[-5:]:
			print(x,self.decompressionDictionary[x])
		print()
		print()

	def initCompress(self):
		self.image = Image.open(self.path)
		self.height, self.width = self.image.size
		self.red, self.green, self.blue = self.processImage()


	def compressColor(self, colorList):
		compressedColor = []
		i = 0
		for currentRow in colorList:
			currentString = currentRow[0]
			compressedRow = ""
			i+=1
			for charIndex in range(1, len(currentRow)):
				currentChar = currentRow[charIndex]
				if currentString+currentChar in self.compressionDictionary:
					currentString = currentString+currentChar
				else:
					compressedRow = compressedRow + str(self.compressionDictionary[currentString]) + ","
					self.compressionDictionary[currentString+currentChar] = self.compressionIndex
					self.compressionIndex += 1
					currentString = currentChar
				currentChar = ""
			compressedRow = compressedRow + str(self.compressionDictionary[currentString])
			# print("Compressing --->",currentRow,"----->",compressedRow)
			compressedColor.append(compressedRow)
		return compressedColor


	def compress(self):
		self.initCompress()
		compressedcColors = []
		# print("Compressing Red")
		compressedcColors.append(self.compressColor(self.red))
		# print("Compressed Red")
		# print("Compressing Green")
		compressedcColors.append(self.compressColor(self.green))
		# print("Compressed Green")
		# print("Compressing Blue")
		compressedcColors.append(self.compressColor(self.blue))
		# print("Compressed Blue")
		# print("Writing File")
		with open("compressed.lzwimg",'w') as file:
			for color in compressedcColors:
				for row in color:
					file.write(row)
					file.write("\n")

		with open("dict.txt",'w') as file:
			for x in list(self.compressionDictionary):
				file.write(x)
				file.write("   ")
				file.write(str(self.compressionDictionary[x]))
				file.write("\n")

		# print ("File compressed and saved as ")
		print (str(os.path.getsize(self.path)))
		print (str(os.path.getsize("compressed.lzwimg")))

	def savedict(self):
		with open("dict2.txt",'w') as file:
			for x in list(self.decompressionDictionary):
				file.write(str(x))
				file.write("   ")
				file.write(str(self.decompressionDictionary[x]))
				file.write("\n")

	def file_lengthy(self, fname):
		with open(fname) as f:
			for i, l in enumerate(f):
				pass
		return i + 1


	def decompressRow(self,line):
		currentRow = line.split(",")
		currentRow[-1] = currentRow[-1][:-1]
		decodedRow = ""
		S,C = "",""
		old = int(currentRow[0])
		decodedRow = decodedRow + self.decompressionDictionary[old]
		for i in range(1,len(currentRow)):
			#self.printDict()
			new = int(currentRow[i])
			if new not in self.decompressionDictionary:
				S = self.decompressionDictionary[old]
				S = S+C
			else:
				S = self.decompressionDictionary[new]
			decodedRow = decodedRow + S
			C = S[0]
			add = self.decompressionDictionary[old]+C
			self.decompressionDictionary[self.decompressionIndex] = add
			self.decompressionIndex+=1
			old = new
		self.savedict()

		try:
			newRow = decodedRow.split(',')
			decodedRow = [int(x) for x in newRow]
			return decodedRow
		except:
			decodedRow = decodedRow.replace(",,",",0,")
			newRow = decodedRow.split(',')
			decodedRow = [int(x) for x in newRow]
			return decodedRow


	def decompress(self):
		self.filelength = self.file_lengthy(self.path)
		lengthPerChannel = self.filelength//3
		image = []
		rowCounter = 0
		mainString = ""
		with open(self.path,"r") as file:
			currentChannel = []
			for line in file:
				if rowCounter<lengthPerChannel:
					currentChannel.append(self.decompressRow(line))
					rowCounter+=1
				else:
					# print("Compressed one channel ...")
					image.append(currentChannel)
					rowCounter = 0
					currentChannel = []
					currentChannel.append(self.decompressRow(line))
					rowCounter += 1
			# print(len(currentChannel))
			image.append(currentChannel)

		redimage = image[0]
		greenimage = image[1]
		blueimage = image[2]

		imagelist = []
		imagelen = len(redimage)
		imagewid = len(redimage[0])

		for i in range(imagelen):
			for j in range(imagewid):
				imagelist.append((redimage[i][j],greenimage[i][j],blueimage[i][j]))

		imagesize = (imagelen,imagewid)
		imagenew = Image.new('RGB',imagesize)
		imagenew.putdata(imagelist)
		imagenew.save("decompressed.tif")

		# print ("File compressed and saved as ")
		print (str(os.path.getsize(self.path)))
		print (str(os.path.getsize("decompressed.tif")))
		# print("Decompression Dones.")


#compressor = LZW(os.path.join("Images","naruto.tif"))
# compressor = LZW(os.path.join("compressed.lzw"))
#compressor.printPixels()
# compressor = LZW(sys.argv[1])
# compressor.compress()