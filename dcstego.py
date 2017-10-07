#!/usr/bin/python
import sys, os, argparse, binascii, array
from dcutils import *
from dcimage import * 
from PIL import Image

#Argument Parser
argumentParser = argparse.ArgumentParser(description="Steganography")
argumentParser.add_argument('-m','--main',dest='main', help='main image filename', required=True)
argumentParser.add_argument('-s','--secret',dest='secret', help='secret image filename')
argumentParser.add_argument('-o','--option',dest='option', help='option: \'read\' or \'write\'', required=True)
argumentParser.add_argument('-out','--output',dest='output', help='output filename')
args = argumentParser.parse_args()

#Put arguments into variables 
image = args.main
secret = args.secret
output = args.output

#Open image for encrypting
def openImage():
    return Image.open(secret)
 #Open image for decrypting
def readImage():
    return Image.open(output)

#check if cover image is big enough to hide secret data
#---------------------------------------------------------------
def CheckFileSize():
	image = Image.open(args.main)
	width, height = image.size
	
	storedbits = width * height * 3
	secretFileSize = os.path.getsize(args.secret) * 8  

	if storedbits > secretFileSize:
		return True
	else:
		print "\nMain image is not big enough"
		print "Need to be at least 3 times the size of the main image"

        exit()

#main function
#---------------------------------------------------------------
def main():

	if args.option == "write":
		if CheckFileSize():
			img = openImage()
			pxs = scramblePixels(img)
			storePixels(secret, img.size, pxs)
			write(image, secret, output)
	elif args.option == "read":
		read(image, output)
		img1 = readImage()
		pxs = unScramblePixels(img1)
        storePixels(output, img1.size, pxs)


main()
