#!/bin/bash
installLocation="/home/user/vacuum/"

# Get the newest mail items
$installLocation/getmail.py

# Work out how many images we need to process
ls $installLocation | egrep "\.jpg" > $installLocation/images

# Process them to get the text and push to splunk
while read image; do
	$installLocation/getdigits.sh $installLocation/$image
	rm $installLocation/$image
done < $installLocation/images
rm $installLocation/images
