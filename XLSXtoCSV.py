#!/usr/bin/env python
#
#2019 Henry Howland
#This script will take any .xlsx files in its cwd and turn them into .csv files. The .xlsx files will be
#    deleted unless code is changed.

from os import listdir
from os.path import isfile, join
import xlrd, csv, os


#This function opens the .xlsx file and puts it into a list for easy manipulation.
def XLSXtoCSV(xlsxFile):
#Opens up the xlsx file to be converted.
    input("debug")
    wb = xlrd.open_workbook(xlsxFile)
#Makes csv format.
    sh = wb.sheet_by_name('Sheet1')

#Replaces file extension with .csv and opens up.
    name = xlsxFile.replace("xlsx","csv")
#Splits at an artifact from curling from confluence and gets rid of it.
    newName= name.split("?")

    csvTable = []
    for rownum in range(sh.nrows):
        csvTable.append(sh.row_values(rownum))

    furtherParsing(csvTable, newName[0])
    threatActorColumnExtender(csvTable,"extended_"+newName[0])



#Discovers the threat actors and EKs and then adds them on as seperate columns.
def threatActorColumnExtender(csvTable,xlsxFile):
#Goes down the list of threat actors to get all of the threat actors in the sheet. At a later time they will be appended
    #to the header so that CVEs associated with certain APTs and EKs can clearly be represeneted.
    threatActors = []
    for i in csvTable:
        if i[1] != "":
        #This is just used so the first line, which is the header, is not included among the list of threat actors.
            if i[1] != "Threat Actor":
                x = i[1].split(", ")
                if len(x) == 1:
                    threatActors.append(i[1])
                else:
                    for q in x:
                        threatActors.append(q)
#Gets rid of duplicate threat actors.
    newThreatActors = []
    for i in threatActors:
      if i not in newThreatActors:
        newThreatActors.append(i)
#Used to fill in empty slots with an N/A and mark Yes or No for whether an exploit kit is being used with a certain CVE.
    for i in range(len(csvTable)):
        if i == 0:
            for r in range(len(newThreatActors)):
                csvTable[i].append(newThreatActors[r])
        else:
            for r in range(len(newThreatActors)):
                if newThreatActors[r] in csvTable[i][1]:
                    csvTable[i].append("Yes")
                else:
                    csvTable[i].append("")
    #Marks N/A for empty entries.
        for r in range(len(csvTable[i])):
            if csvTable[i][r] == "":
                csvTable[i][r] = "N/A"
    csvWriter(csvTable, xlsxFile)


#Adds N/A to blank fields the writes .csv.
def furtherParsing(csvTable, xlsxFile):
    for i in range(len(csvTable)):
        for r in range(len(csvTable[i])):
            if csvTable[i][r] == "":
        #Fills in with N/A
                csvTable[i][r] = "N/A"
    csvWriter(csvTable,xlsxFile)


#Writes the .csv using the original name with a new extension after all the parsing and transformations have been done.
def csvWriter(csvTable, xlsxFile):
    with open(xlsxFile, mode='w') as wp:
    #Delimiter of ' , ' makes the file a .csv
        WCVE = csv.writer(wp, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in csvTable:
            WCVE.writerow(i)



def initialize():
    xlsxFiles = []
    files = [f for f in listdir(os.getcwd()) if isfile(join(f))]
    #Makes list of all xlsx files.
    for i in range(len(files)):
        if "xlsx" in files[i]:
            xlsxFiles.append(files[i])
    #Exits if there are no .xlsx files.
    if len(xlsxFiles) == 0:
        print("No .xlsx files in directory.")
        exit()
    #Takes list of all .xlsx files in directory and runs them through XLSXtoCSV.
    for i in range(len(xlsxFiles)):
        XLSXtoCSV(xlsxFiles[i])

initialize()

