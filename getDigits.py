#!/usr/bin/python3

import cv2
import pytesseract
import argparse
import exifread

parser = argparse.ArgumentParser(description="Load jpg file and output digits", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("file", help="File name of jpg")
parser.add_argument("binaryThresh1", help="Value of initial adaptive threshold - try 9")
parser.add_argument("binaryThresh2", help="Value of secondary adaptive threshold - try 10")
parser.add_argument("clipLimit", help="Clip Limit of contrast adaption - try 32")
args = vars(parser.parse_args())
imgFile = args["file"]
thresh1 = int(args["binaryThresh1"])
thresh2 = int(args["binaryThresh2"])
clipLimitVal = int(args["clipLimit"])

# edge detection and colour invert
img = cv2.imread(imgFile)
img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = cv2.bitwise_not(img)
img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, thresh1, thresh2)

# attempt to add contrast
img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
l_channel, a, b = cv2.split(lab)
clahe = cv2.createCLAHE(clipLimit=clipLimitVal, tileGridSize=(16,16))
cl = clahe.apply(l_channel)
limg = cv2.merge((cl,a,b))
img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

# grab digits
text = pytesseract.image_to_string(img, config='outputbase digits')
print(text)

# get the exif data date stamp
with open(imgFile, 'rb') as fh:
	exif = exifread.process_file(fh)
	if "DateTimeOriginal" in exif:
		tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal")
		dateTaken = tags["EXIF DateTimeOriginal"]
		print(dateTaken)
	else:
		pass
		# TODO: put current date time in instead
