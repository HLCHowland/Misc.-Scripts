#!/usr/bin/env python3.4

#2019 Henry Howland
#CVEextractor
#This script is used to parse and save the data from the weaponized CVEs page on the Regeneron confluence. This data will
    #be monitored by a heavy forwarder and fed into Splunk, where machines with especially important CVEs exposed can be
    #monitored for expidited remediation. Is able to pull any CVEs out of text if wanted for another application.

#For the current use of scraping a confluence page of weaponized CVEs the full command should be:
    #curl -u username:password regenron.confluence.com/path/to/weaponized/CVE/table |./CVEextractor.sh

import re, sys, os

#This takes the data piped into the script, the html from the confluence web page
html = sys.stdin.read()

#Regular expression pulls out all CVEs in the text(html) piped into the program.
CVEs = re.findall("CVE-2...-.\d{3,7}", html)

#Prepares file for CVEs to go into
path = (os.getcwd())
output = (path + "/weaponizedCVEs.csv")
outF = open(output, "w")
#Creates the header for the .csv file.
outF.write("weaponizedCVE\n")
#Writes in each cve and closes file when finished.
for line in CVEs:
    outF.write(line)
    outF.write("\n")
outF.close()