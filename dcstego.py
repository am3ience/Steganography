#!/usr/bin/python
import sys, os, argparse, binascii, array
from dcutils import *
from dcimage import * 
from PIL import Image

key="comp8505comp8505"

argumentParser = argparse.ArgumentParser(description="Steganography")
argumentParser.add_argument('-m','--main',dest='main', help='main image filename', required=True)
argumentParser.add_argument('-s','--secret',dest='secret', help='secret image filename')
argumentParser.add_argument('-o','--option',dest='option', help='option: \'read\' or \'write\'', required=True)
argumentParser.add_argument('-out','--output',dest='output', help='output filename')
args = argumentParser.parse_args()

image = args.main
secret = args.secret
output = args.output

def openImage():
    return Image.open(secret)
   
def readImage():
    return Image.open(output)

#check if cover image is big enough to hide secret data
#---------------------------------------------------------------
def CheckFileSize():
	image = Image.open(args.main)
	width, height = image.size
	#3 bits in a pixel
	storedbits = width * height * 3
	secretFileSize = os.path.getsize(args.secret) * 8  #in bits

    #if main image large enough True
	if storedbits > secretFileSize:
		return True
	else:
		print "\nMain image is not big enough"
		print "Need to be at least 3 times the size of the main image"

        exit()

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
