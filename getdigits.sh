#!/bin/bash

installLocation="/home/user/vacuum"
splunkEndpoint="172.16.10.232"
splunkPort=88
splunkPath="/servers/collector/raw"
splunkAuth=""

if [ -z $tenMic ] || [ -z $ninetyMic ] || [ -z $oneeightyMic ] || [ -z $fivehundredMic ];
then
	${installLocation}/getDigits.py $1 11 10 32 > test
	cat test | sed 's/\./ /g; s/-/ /g' | awk 'NF' > test2
	mv test2 test
	tenMic=$(cat test | awk 'NF' | grep "10" | head -n 1 | awk -F'10' '{print $2}' | sed -e 's/\.//g; s/ //g; s/-//g')
	ninetyMic=$(cat test | awk 'NF' | grep "90" | head -n 1 | awk -F'90' '{print $2}' | sed -e 's/\.//g; s/ //g; s/-//g')
	oneeightyMic=$(head -n 3 test | tail -n 1 | awk '{print $2}')
	fivehundredMic=$(cat test | awk 'NF' | grep "500" | head -n 1 | awk -F'500' '{print $2}' | sed -e 's/\.//g; s/ //g; s/-//g')
	date=$(cat test | tail -n 1)
	echo -e "Vacuum Data\n------------\nDate: ${date}\n>10 : ${tenMic}\n>90 : ${ninetyMic}\n>180 : ${oneeightyMic}\n>500 : ${fivehundredMic}\n"
fi
rm test

# Push to splunk
if [ ! -z $tenMic ] && [ ! -z $ninetyMic ] && [ ! -z $oneeightyMic ] && [ ! -z $fivehundredMic ];
then
	csvData=$(echo "$date, $tenMic, $ninetyMic, $oneeightyMic, $fivehundredMic")
	curl --silent -k https://${splunkEndpoint}:${splunkPort}${splunkPath} -H "Authorization: Splunk $splunkAuth" -d "${csvData}"
fi
