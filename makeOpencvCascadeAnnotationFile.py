
import glob, os
import os.path
import time
import argparse
import cv2
from xml.dom import minidom
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

#==============================================================
positiveDesc = "positives.info"  #output file
xmlFolder = "datasets/labeled/palm/v1/labels"
imgFolder = "datasets/labeled/palm/v1/images"
labelName = "palm"

#==============================================================

totalLabels = 0
wLabels = 0
hLabels = 0

def createPositive(imgFolder, xmlFilename, assignName=""):
    global totalLabels, wLabels, hLabels

    labelXML = minidom.parse(xmlFilename)
    labelName = []
    labelXstart = []
    labelYstart = []
    labelW = []
    labelH = []
    totalW = 0
    totalH = 0
    countLabels = 0

    tmpArrays = labelXML.getElementsByTagName("filename")
    for elem in tmpArrays:
        filenameImage = elem.firstChild.data
    #print ("Image file: " + filenameImage)


    tmpArrays = labelXML.getElementsByTagName("name")
    for elem in tmpArrays:
        labelName.append(str(elem.firstChild.data))

    tmpArrays = labelXML.getElementsByTagName("xmin")
    for elem in tmpArrays:
        labelXstart.append(int(elem.firstChild.data))

    tmpArrays = labelXML.getElementsByTagName("ymin")
    for elem in tmpArrays:
        labelYstart.append(int(elem.firstChild.data))

    tmpArrays = labelXML.getElementsByTagName("xmax")
    for elem in tmpArrays:
        labelW.append(int(elem.firstChild.data))

    tmpArrays = labelXML.getElementsByTagName("ymax")
    for elem in tmpArrays:
        labelH.append(int(elem.firstChild.data))

    opencvCascade = ""
    tmpChars = ""
    countLabels = 0

    image = cv2.imread(imgFolder + "/" + filenameImage)
    image2 = image.copy()
    filepath = imgFolder
    filename = filenameImage

#    with open(descFile, 'a') as the_file_aug:
    for i in range(0, len(labelName)):
        if(assignName=="" or assignName==labelName[i]):
            countLabels += 1
            totalW = totalW + int(labelW[i]-labelXstart[i])
            totalH = totalH + int(labelH[i]-labelYstart[i]) 
            rois = "{} {} {} {}   ".format( labelXstart[i], labelYstart[i], int(labelW[i]-labelXstart[i]), int(labelH[i]-labelYstart[i]) )
            tmpChars = tmpChars + rois

    wLabels += totalW
    hLabels += totalH
    totalLabels += countLabels

    #print("Average W, H: {}, {}".format(int(totalW/countLabels), int(totalH/countLabels)) )
    #print("{}, {}, {}".format(totalLabels, wLabels, hLabels) )
    return "../{}  {}  {}".format(filepath+"/"+filename, countLabels, tmpChars)


with open(positiveDesc, 'a') as the_file:

    for file in os.listdir(xmlFolder):
        filename, file_extension = os.path.splitext(file)

        if(file_extension==".xml"):
            #print("XML: {}".format(filename))

            #imgfile = imgFolder+"/"+filename+"."+imageType
            xmlfile = xmlFolder + "/" + file
            #print(xmlfile)
            #if(os.path.isfile(imgfile)):
            outLabels = createPositive(imgFolder, xmlfile, labelName)
            the_file.write(outLabels + '\n')
            #print( outLabels )
            #print()
    #print("{}, {}, {}".format(totalLabels, wLabels, hLabels) )
    avgW = round(wLabels/totalLabels, 1)
    avgH = round(hLabels/totalLabels,1)
    print("----> Average W:H = {}:{}".format(avgW, avgH ))
