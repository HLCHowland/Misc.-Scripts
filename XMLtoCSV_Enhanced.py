#2019 Henry Howland
#This script will convert the Qualys DB .xml into a .csv, you can select the path, what to seperate by, and where the
    #output goes to.
import xml.etree.ElementTree as ET
import csv, sys, re

#Help screen when program fails out or it is requested
help = ("Converts .xml files to .csv files where the .xml has a max depth of 4."
        "\nXMLtoCSV [-h, or -o (element to seperate by) (file path)]"
        "\n   -h     help"
        "\n   -o     output via stdout"
        "Ex.\n\n"
        "State>\n<Resident Id='100'>\n<Name>Sample Name</Name>\n\t<PhoneNumber>1234567891</PhoneNumber>"
        "\n\t<EmailAddress>sample_name@example.com</EmailAddress>\n\t<Address>"
        "\n\t\t<StreetLine1>Street Line1</StreetLine1>\n\t\t<City>City Name</City>"
        "\n\t\t<StateCode>AE</StateCode>"
        "\n\t\t<PostalCode>12345</PostalCode>"
        "\n\t</Address>\n</Resident>\n<Resident Id='101'>"
        "\n\t<Name>Sample Name1</Name>\n\t<PhoneNumber>1234567891</PhoneNumber>"
        "\n\t<EmailAddress>sample_name1@example.com</EmailAddress>\n\t<Address>"
        "\n\t\t<StreetLine1>Current Address</StreetLine1>\n\t\t<City>Los Angeles</City>"
        "\n\t\t<StateCode>CA</StateCode>\n\t\t<PostalCode>56666</PostalCode>\n\t</Address>\n</Resident>"
        "\n</State>\n\nTo get the values in 'Resident' in the above .xml followed by the file name in your CWD. "
        "\nsimply call:\nXMLtoCSV.py Resident residents.xml")



#Goes in and discovers paths to all values, gets the values in a table, parses them, saves them in a .csv or outputs
    #via stdout
def converter(delimiter, path, stdout):
#Parses xml into python workable format
    try:
        tree = ET.parse(path)
    except:
#If the .xml file fails to load in, it will probably be because it is formatted incorrectly, so this case is handled below
        print(".xml formatted incorrectly...")
        exit()
#Grabs root element of tree
    root = tree.getroot()
#Empty lists needed for data collection
    doneXmlPaths = []
    elemList = []
    output = []
#Grabs the tag of every surface level element in the tree
    for elem in tree.iter():
        elemList.append(elem.tag)
    elemList = list(set(elemList))
#Used to seperate chunks we will look at by the delimiter set at prog init. For example, if its 'VULN' this gets everything
    #between <VULN> and </VULN>.
    for subDelim1 in root.findall('.//' + delimiter):
        xmlPaths = []
        formattedXmlPaths = []
#Begin descending into .xml tree to look for the paths to each tag it pull earlier. If the end of the tag is not found,
    #it will look for it one more layer down. The tags do not go more than three levels deep for the knowledge base .xml
    #but it will go to five incase formatiing changes, or this script is used with other .xml files. The different levels
    #are indicated by the subDelim (subDelimiter) variables
        for i in range(len(elemList)):
        #If statements set up so if element is not found it will go one more level deeper
            for subDelim2 in subDelim1.findall(elemList[i]):
                #Try statement used to catch errors in case file is not formatted right
                try:
                #The sD#txt are the variables used to check if the end of the element search has been reached or if it goes
                    #deeper. If you get the whitespaces and \n that you see below, that indicates you must go deeper to get
                    #to the end of the branch.
                    sD2txt = (list(subDelim2.text))
                    #TDue to the way Qualys formatted their .xml, the spaces and #\n have to be listed out even though
                        #it shoudlnt make a difference.
                    if sD2txt == ['\n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']:
                        for subDelim3 in subDelim2.findall('*'):
                            sD3txt = subDelim3.text
                            if sD3txt == "\n            ":
                                for subDelim4 in subDelim3.findall('*'):
                                    sD4txt = subDelim4.text
                                    if sD4txt == "\n            ":
                                    #Bottom of search depth
                                        for subDelim5 in subDelim4.findall('*'):
                                            ePath = (subDelim2.tag + "/" + subDelim3.tag + "/" + subDelim4.tag + "/" + subDelim5)
                                            xmlPaths.append(ePath)
                                    #Once the end has been reached, the ePath (element path) is then added to an array.
                                        #These paths will be used later on to extract the text they lead to.
                                    else:
                                        ePath = (subDelim2.tag + "/" + subDelim3.tag + "/" + subDelim4.tag)
                                        xmlPaths.append(ePath)
                            else:
                                ePath = (subDelim2.tag + "/" + subDelim3.tag)
                                xmlPaths.append(ePath)
                    else:
                        ePath = (subDelim2.tag)
                        xmlPaths.append(ePath)
                except:
                #The clause of the try statement in case it fails, as it will most likley be a formatting issue informs
                    #the user of an issue with the file.
                    print("No data in .xml file...")
    #Takes the paths collected and sorts them alphabetically for ease of use.
    for i in xmlPaths:
        if i not in formattedXmlPaths:
            formattedXmlPaths.append(i)
    formattedXmlPaths = sorted(formattedXmlPaths)

    #Each path is essentially a field that data is sorted by, switching the : and the / allows you to read the path more
        #easily as a field, as well as allowing it to integrate better in other environments like Splunk better.
    for i in range(len(formattedXmlPaths)):
        doneXmlPaths.append(formattedXmlPaths[i].replace("/", ":"))
    for subDelim1 in root.findall('.//VULN'):
    #vulnUnits will be a line of the fields looked up appended together, which is then appended as one line of the .csv
        #to the output.
        vulnUnits = []
        for i in range(len(formattedXmlPaths)):
        #If there is a failure ,as in,it goes to the field but finds there is onthing there for that entry, it will leave
            #a N/A as in not applicable.
            try:
            #Goes to each part of the tree looking for the field's .txt attribute. It iterates through the list of
                #formatted element paths and appends the result, positive or negative to vulnUnits based on whether the
                #program fails out of the try statement or not.
                doneXmlPaths[i] = subDelim1.find(formattedXmlPaths[i]).text
                vulnUnits.append(doneXmlPaths[i])
            except:
                vulnUnits.append("N/A")
    #The list of data collected above counting as one line is appended onto the larger list which makes up the csv
        output.append(vulnUnits)
    #The doneXmlPaths here are remade as they can be overwritten in the statements above using them as an incrementer
        #depending on python version.
    doneXmlPaths = []
    for i in range(len(formattedXmlPaths)):
        doneXmlPaths.append(formattedXmlPaths[i].replace("/", ":"))
#Creates the header at the top of tehe csv used to indicate which fields are which
    output.insert(0, doneXmlPaths)
#Next few lines and loops used to do additional parsing, taking out newlines and <.?> tags leftover from earlier parsing
    lines = []
    vals = []
#Regex to take out '<>' tags and anything inbetween them
    clean = re.compile('<.*?>')
    for i in output:
        lines = []
        for x in i:
            x = x.replace("\n","")
            lines.append(re.sub(clean, '', x))
        vals.append(lines)
#Overwrites output with newly parsed list.
    output = vals


#Depeding on if -o switch is used, output will either automatically go to a .csv or it will go through standard out
    if stdout == False:
    #Replaces extension of file
        name = path.replace("xml", "csv")
    #Opens file and writes .csv
        Resident_data = open(name, 'w')
        csvWriter = csv.writer(Resident_data)
        for i in range(len(output)):
            csvWriter.writerow(output[i])
        Resident_data.close()
    else:
    #File delivered through standard out via print statements
        for i in range(len(output)):
            print(output[i])



#Function handling command line arguments.
def initialization():
    try:
        if __name__ == "__main__":
        #-h gets the help text
            if sys.argv[1] == "-h":
                print(help)
                exit()
        #-o makes the output go through standard out, not a text file.
            if sys.argv[1] == "-o":
        #Picks up the first argument as the -o, the second as the tags to check by, and the third the path
        #python3 XMLtoCSV.py -o TAG PATH
                converter(sys.argv[2], sys.argv[3], sys.argv[1])
            else:
        #Picks first argument as tags to search by and second as path putting output into file.
        # python3 XMLtoCSV.py TAG PATH
                converter(sys.argv[1], sys.argv[2], False)
    except IndexError:
    #Fail over to help screen incas of wholly invalid input
        print(help)
initialization()
