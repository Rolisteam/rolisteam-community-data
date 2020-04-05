#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import sys, getopt
from pprint import pprint
from enum import Enum
import os

class ModeEdition(Enum):
    NONE = 0
    MINIMAL = 1
    COMPLETE = 2
    EXPORT = 3
    IMPORT = 4

def Usage():
    print("Usage")
    print("")
    print("-h, --help; show this documentation")
    print("-i, --input <file>; path to input file")
    print("-o, --output <file>; path to output file, should not exist")
    print("-c, --complete; change the sheet to use v1.9 SDK, may change the look of some items.")
    print("-m, --minimal; change the sheet to make it work on v1.9")
    print("-e, --export <file>; export characters data into file")
    print("-a, --addCharacter <file>; import characters data from file (erase the actual ones)")


def createNewField(data):
    newKeys=["additionnalBottomCode","additionnalHeadCode","additionnalImport"]
    for newKey in newKeys:
        if newKey not in data:
            data[newKey]=""
    return data


def uuidAndPageCount(data,key,pageCount):
    data['uuid']=key
    data['pageCount']=pageCount
    return data


def updateImage(data):
    key=""
    pageCount=0
    for p in data['background']:
        p['filename']=""
        p['isBg']=True
        pageCount+=1
        if len(key) == 0:
            tmp=p['key']
            key=tmp[0:tmp.find("_")]
        else:
            tmp=p['key']
            p['key']="{}{}".format(key,tmp[tmp.find("_"):])

    return (data,key,pageCount)


def qmlIncludeMinimal(data):
    #print("qmlIncludeMinimal")
    pattern="import \"qrc:/resources/qml/\""
    newPat="import Rolisteam 1.0"
    qml = data['qml']
    qml = qml.replace(pattern,newPat)
    data['qml'] = qml
    return data

def qmlIncludeComplete(data):
    #print("qmlIncludeComplete")
    pattern="import \"qrc:/resources/qml/\""
    newPat="import Rolisteam 1.1"
    qml = data['qml']
    qml = qml.replace(pattern,newPat)
    data['qml'] = qml
    return data

def changeDiceButton(data):
    #print("DiceButton")
    qml = data['qml']
    inCheck=False
    result=[]
    for line in qml.splitlines():
        if(line.find("DiceButton")>-1):
            inCheck=True
        if(line.find("textColor")>-1 and inCheck):
            line=line.replace("textColor","color")
        elif(line.find("color:")>-1 and inCheck):
            line=line.replace("color","backgroundColor")
            inCheck=False
        result.append(line)

    data['qml']="\n".join(result)
    return data


def changeTextFieldField(data):
    #print("TextFieldField")
    qml = data['qml']
    inCheck=False
    result=[]
    for line in qml.splitlines():
        if(line.find("TextFieldField")>-1):
            inCheck=True
        if(line.find("textColor")>-1 and inCheck):
            line=line.replace("textColor","color")
        elif(line.find("color:")>-1 and inCheck):
            line=line.replace("color","backgroundColor")
            inCheck=False
        result.append(line)

    data['qml']="\n".join(result)
    return data

def changeTextArea(data):
    #print("changeTextArea")
    qml = data['qml']
    inCheck=False
    result=[]
    for line in qml.splitlines():
        if(line.find("TextAreaField")>-1):
            inCheck=True
        if(line.find("textColor")>-1 and inCheck):
            line=line.replace("textColor","color")
        elif(line.find("color:")>-1 and inCheck):
            line=line.replace("color","backgroundColor")
            inCheck=False
        result.append(line)

    data['qml']="\n".join(result)
    return data

def changeCheckbox(data):
    #print("changeCheckbox")
    qml = data['qml']
    inCheck=False
    result=[]
    for line in qml.splitlines():
        if(line.find("CheckBoxField")>-1):
            inCheck=True
        if(line.find("textColor")>-1 and inCheck):
            line=line.replace("textColor","borderColor")
        if(line.find("color:")>-1 and inCheck):
            inCheck=False
            line="\n"
        result.append(line)

    data['qml']="\n".join(result)
    return data

def changeTextInputField(data):
    #print("changeTextInputField")
    qml = data['qml']
    inCheck=False
    result=[]
    for line in qml.splitlines():
        if(line.find("TextInputField")>-1):
            inCheck=True
        if(line.find("textColor")>-1 and inCheck):
            line=line.replace("textColor","color")
        elif(line.find("color")>-1 and inCheck):
            line=line.replace("color","backgroundColor")
            inCheck=False


        result.append(line)


    data['qml']="\n".join(result)
    return data

def completeChange(data):
    array = updateImage(data)
    data = array[0]
    key = array[1]
    pageCount = array[2]
    data = uuidAndPageCount(data,key,pageCount)
    data = qmlIncludeComplete(data)
    data = changeCheckbox(data)
    data = changeTextInputField(data)
    data = changeTextArea(data)
    data = changeTextFieldField(data)
    data = changeDiceButton(data)
    return data


def minimalChange(data):
    array = updateImage(data)
    data = array[0]
    key = array[1]
    pageCount=array[2]
    data = uuidAndPageCount(data,key,pageCount)
    data = qmlIncludeMinimal(data)
    return data


def extractCharacterData(data, outputFile):
    characters = data['characters']
    saveFile(outputFile, characters)

def loadFile(path):
    try:
        with open(path) as f:
            data = json.load(f)
            #print(data)
        return data
    except:
        print("Error: fail to read the input file")


def saveFile(path,data):
    try:
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)
    except:
        print("Error: fail to save data into {}").format(path)

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hi:o:e:a:cm",["help","input=","output=","complete","minimal"])
    except getopt.GetoptError:
        Usage()
        sys.exit(2)

    mode=ModeEdition.NONE
    inputFile=""
    outputFile=""
    importFile=""
    for key, value in opts:
        if key in ('-h',"--help"):
            Usage()
            sys.exit(0)
        elif key in ("-i","--input"):
            inputFile=value
        elif key in ("-o","--output"):
            outputFile=value
        elif key in ("-c", "--complete"):
            mode=ModeEdition.COMPLETE
        elif key in ("-m","--minimal"):
            mode=ModeEdition.MINIMAL
        elif key in ("-a","--add"):
            importFile = value
            mode=ModeEdition.IMPORT
        elif key in ("-e","--export"):
            importFile = value
            mode=ModeEdition.EXPORT

    if mode == ModeEdition.NONE:
        print("Error: no edition mode: minimal or complete")
        Usage()
        sys.exit(1)

    if os.path.exists(outputFile):
        print("Error: output file already exists")
        Usage()
        sys.exit(1)

    data=loadFile(inputFile)

    if mode == ModeEdition.MINIMAL:
        data = minimalChange(data)
    elif mode == ModeEdition.COMPLETE:
        data = completeChange(data)
    elif mode == ModeEdition.EXPORT:
        extractCharacterData(data, importFile)
        return
    elif mode == ModeEdition.IMPORT:
        character=loadFile(inputFile)
        data['characters']=character

    saveFile(outputFile, data)




    #i=1
    #for p in data['data']['items']:
    #    print(p['label'])
    #    print(str(i))
    #    p['id']='id_'+str(i)
    #    i+=1




if __name__ == '__main__':
    main(sys.argv[1:])
