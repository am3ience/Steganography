#!/usr/bin/python
import os, sys, binascii, array, random, struct
from Crypto.Cipher import AES
from Crypto import Random
import bitarray
import hashlib
from PIL import Image
from cryptography.fernet import Fernet

binDataString =""
binDataSize =""

def seed(img):
    random.seed(hash(img.size))

def getPixels(img):
    w, h = img.size
    pxs = []
    for x in range(w):
        for y in range(h):
            pxs.append(img.getpixel((x, y)))
    return pxs

def scrambledIndex(pxs):
    idx = range(len(pxs))
    random.shuffle(idx)
    return idx

def scramblePixels(img):
    seed(img)
    pxs = getPixels(img)
    idx = scrambledIndex(pxs)
    out = []
    for i in idx:
        out.append(pxs[i])
    return out

def unScramblePixels(img):
    seed(img)
    pxs = getPixels(img)
    idx = scrambledIndex(pxs)
    out = range(len(pxs))
    cur = 0
    for i in idx:
        out[i] = pxs[cur]
        cur += 1
    return out

def storePixels(name, size, pxs):
    outImg = Image.new("RGB", size)
    w, h = size
    pxIter = iter(pxs)
    for x in range(w):
        for y in range(h):
            outImg.putpixel((x, y), pxIter.next())
    outImg.save(name)

#def main():
#    img = openImage()
#    if operation() == "scramble":
#        pxs = scramblePixels(img)
#        storePixels("scrambled.bmp", img.size, pxs)
#    elif operation() == "unscramble":
#        pxs = unScramblePixels(img)
#        storePixels("unscrambled.bmp", img.size, pxs)

# convert image into bites
#---------------------------------------------------------------
def createString(secret):

	global binDataString
	global binDataSize

	binName = ""
	nullDelimiter = "00000000"

    #get the file name in binary
	for bits in secret:
		binName += format(ord(bits), 'b').zfill(8)#convert the file name to binary

    #get the file data in binary
	fileData = bytearray(open(secret, 'rb').read())#opens the binary file in read or write mode
	for bits in fileData:
		binDataString += bin(bits)[2:].zfill(8)#convert the file data to binary
		#print binDataString 

    #get the number od bits of the file in binary
	dataSize = list(str(len(binDataString)))#data size as a list of each int

    #convert the array of decimal numbers into a bit string
	for bits in dataSize:
		binDataSize += format(ord(bits), 'b').zfill(8)#convert the data size to binary

    #assemble string with NULL delimiters
	bitString = binName + nullDelimiter + binDataSize + nullDelimiter + binDataString
	
	#bitString = encryption.encrypt(bitString)
	return bitString
	
#converts the binary values for rgb into decimal
#---------------------------------------------------------------
def getPixel(binRGB):
	rgbDecimalArray = []

	for col in binRGB:
		pixelnumbers = int(''.join(str(b) for b in col), 2)
		#print pixelnumbers
		rgbDecimalArray.append(pixelnumbers)
    #return the rgb value of the pixel in decimal
	return (rgbDecimalArray[0], rgbDecimalArray[1], rgbDecimalArray[2])
	
#save the datastring with file filename
#---------------------------------------------------------------
def saveImage(fileName, datastring):
	secretbyteStrings_array = []

    #convert bit string into array of bytes in decimal format
	for i in range (0, len(datastring)/8):
		secretbyteStrings_array.append(int(datastring[i*8:(i+1) * 8], 2))
		datastring
	print secretbyteStrings_array
	secretByteString = array.array('B', secretbyteStrings_array).tostring()
	secret = bytearray(secretByteString)
	secretFile = open(str(fileName), 'w')
	secretFile.write(secret)

#---------------------------------------------------------------
def openFile(imagePath):
	return Image.open(imagePath).convert('RGB')


