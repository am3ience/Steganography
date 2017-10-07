#!/usr/bin/python

#------------------------------------
#pixelnumbers1 = str(pixelnumbers1)
#pixelnumbers1 = int(pixelnumbers1.encode('rot13'))
#pixelnumbers1 = pad(str(pixelnumbers1))
#pixelnumbers1 = encryption_suite.encrypt(pixelnumbers1)
#pixelnumbers1 = int(pixelnumbers1, 2)
#------------------------------------

import os, sys, binascii, array
from Crypto.Cipher import AES
from Crypto import Random
from bitstring import BitArray
import hashlib
from PIL import Image
import dcimage
from cryptography.fernet import Fernet

keyf = Fernet.generate_key()
key="comp8505comp8505"
encryption_suite = AES.new(key, AES.MODE_CBC, 'This is an IV456')
decryption_suite = AES.new(key, AES.MODE_CBC, 'This is an IV456')
cipher_suite = Fernet(keyf)


#examine the lsb of each pixel, grouping into bytes
#check for nulls to signify if we are dealing with data or header info
#bytes determined to be data result in the hidden file
#---------------------------------------------------------------
def write(mainimage, secret, output):
	
	Stringbits = dcimage.createString(secret)
	imageObject = Image.open(mainimage).convert('RGB')
	imageWidth, imageHeight = imageObject.size
	pixels = imageObject.load()
	rgbDecimal_Array = []
	rgb_Array = []
	count = 0

	#loop through each pixel
	for x in range (imageWidth):
		for y in range (imageHeight):
			r,g,b = pixels[x,y]
			#convert each pixel into an 8 bit representation
			redPixel = list(bin(r)[2:].zfill(8))
			greenPixel = list(bin(g)[2:].zfill(8))
			bluePixel = list(bin(b)[2:].zfill(8))
			pixelList = [redPixel, greenPixel, bluePixel]

			#for each of rgb
			for i in range(0,3):
				#verify we have reached the end of our hidden file
				if count >= len(Stringbits):
					#convert the bits to their rgb value and appened them
					for rgbValue in pixelList:
						pixelnumbers1 = int(''.join(str(b) for b in rgbValue), 2)
						#pixelnumbers1 = cipher_suite.encrypt(bytes(pixelnumbers1))
						print pixelnumbers1
						#pixelnumbers1 = int(pixelnumbers1)
						rgb_Array.append(pixelnumbers1)
					pixels[x, y] = (rgb_Array[0], rgb_Array[1], rgb_Array[2])
					print "Completed"
					return imageObject.save(output)

				#If we haven't rached the end of the file, store a bit
				else:
					pixelList[i][7] = Stringbits[count]
					count+=1
			pixels[x, y] = dcimage.getPixel(pixelList)




#examine the lsb of each pixel, grouping into bytes
#check for nulls to signify if we are dealing with data or header info
#bytes determined to be data result in the hidden file
#---------------------------------------------------------------
def read(mainimage, output):
	lsbByte_Array = []
	dataString = ""
	secretFileName = ""
	lsbString = ""
	count = 0#iterator
	headerReceived=0#flags
	sizeReceived=0
	imageObject = dcimage.openFile(mainimage)
	pixels = imageObject.load()
	imageWidth, imageHeight = imageObject.size

	#cycle through each pixel
	for x in range(imageWidth):
		for y in range(imageHeight):
			r, g, b = pixels[x, y]
			#trim so we are dealing with only the least significant bit
			redPixel = str(bin(r)[2:].zfill(8))[7]
			greenPixel = str(bin(g)[2:].zfill(8))[7]
			bluePixel = str(bin(b)[2:].zfill(8))[7]
			secretBits = [redPixel, greenPixel, bluePixel]

			#for each of rgb
			for i in range(0,3):
				#check if our flags are set
				if (headerReceived == 0 or sizeReceived == 0):
					lsbString += secretBits[i]

					#verify each byte
					if len(lsbString) == 8:
						lsbByte_Array.append(lsbString)

						#check if we have received a NULL byte
						if lsbString == "00000000":
							if headerReceived == 0:

								#convert the the bit array into an ascii String
								#set flag when header and size was received
								fileName = ''.join(binascii.unhexlify('%x' % int(b,2)) for b in lsbByte_Array[0:len(lsbByte_Array) - 1])
								print "File name: " + str(fileName)
								headerReceived = 1
							elif sizeReceived == 0:
								fileSize = ''.join(binascii.unhexlify('%x' % int(b,2)) for b in lsbByte_Array[0:len(lsbByte_Array) - 1])
								print "File size: " + fileSize
								sizeReceived=1

							#reset the values
							lsbByte_Array = []
						lsbString = ""

				#once headers received, resulting data is hidden data
				elif (headerReceived == 1 and sizeReceived == 1):
					if int(count) < int(fileSize):
						#keep appending secret bits to the dataString until depleted
						dataString += secretBits[i]
						count += 1
					else:
						#send to have hidden file created
						return dcimage.saveImage(output, dataString)
