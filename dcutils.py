#!/usr/bin/python
import os, sys, binascii, array
from bitstring import BitArray
import hashlib
from PIL import Image
import dcimage

#inserts data into the LSB of rgb value
#uses the null delimiter as flag
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
				#go to the end of the secret file
				if count >= len(Stringbits):
					#convert the bits to their rgb value and appened them
					for rgbValue in pixelList:
						pixelnumbers1 = int(''.join(str(b) for b in rgbValue), 2)
						rgb_Array.append(pixelnumbers1)
					pixels[x, y] = (rgb_Array[0], rgb_Array[1], rgb_Array[2])
					print "Done"
					return imageObject.save(output)
				else:
					pixelList[i][7] = Stringbits[count]
					count+=1
			pixels[x, y] = dcimage.getPixel(pixelList)




#examine the lsb of each pixel
#check for nulls to signify if we are dealing with data or header info
#bytes determined to be data result in a hidden file
#---------------------------------------------------------------
def read(mainimage, output):
	lsbByte_Array = []
	dataString = ""
	secretFileName = ""
	lsbString = ""
	count = 0
	headerReceived = False #default
	sizeReceived = False #default 
	imageObject = dcimage.openFile(mainimage)
	pixels = imageObject.load()
	imageWidth, imageHeight = imageObject.size

	#cycle through each pixel
	for x in range(imageWidth):
		for y in range(imageHeight):
			r, g, b = pixels[x, y]
			
			#trim to LSB
			redPixel = str(bin(r)[2:].zfill(8))[7]
			greenPixel = str(bin(g)[2:].zfill(8))[7]
			bluePixel = str(bin(b)[2:].zfill(8))[7]
			secretBits = [redPixel, greenPixel, bluePixel]

			#for each of rgb
			for i in range(0,3):
				#check for flags
				if (headerReceived == False or sizeReceived == False):
					lsbString += secretBits[i]

					#verify each byte
					if len(lsbString) == 8:
						lsbByte_Array.append(lsbString)
						if lsbString == "00000000":
							if headerReceived == False:

								#convert the the bit array into an ascii String
								#set flag when header and size was received
								fileName = ''.join(binascii.unhexlify('%x' % int(b,2)) for b in lsbByte_Array[0:len(lsbByte_Array) - 1])
								print "File name: " + str(fileName)
								headerReceived = True
							elif sizeReceived == False:
								fileSize = ''.join(binascii.unhexlify('%x' % int(b,2)) for b in lsbByte_Array[0:len(lsbByte_Array) - 1])
								print "File size: " + fileSize
								sizeReceived = True

							#reset the values
							lsbByte_Array = []
						lsbString = ""

				#hidden data handling 
				elif (headerReceived == True and sizeReceived == True):
					if int(count) < int(fileSize):
						dataString += secretBits[i]
						count += 1
					else:
						return dcimage.saveImage(output, dataString)
