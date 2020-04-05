<?php






/*import json
import sys, getopt
from pprint import pprint
from enum import Enum
import os*/


class ModeEdition extends SplEnum {
    const __functionault = self::NONE;

    const NONE = 0
    const MINIMAL = 1
    const COMPLETE = 2
}



/*function Usage():
    print("Usage")
    print("")
    print("-h, --help; show this documentation")
    print("-i, --input <file>; path to input file")
    print("-o, --output <file>; path to output file, should not exist")
    print("-c, --complete; change the sheet to use v1.9 SDK, may change the look of some items.")
    print("-m, --minimal; change the sheet to make it work on v1.9")
*/


function createNewField($data) {
    $newKeys=array("additionnalBottomCode","additionnalHeadCode","additionnalImport");
    foreach( $newKeys as &$key)
    {
        if(in_array($key, $data))
        {
            $data[$newKey]="";
        }
    }
    return $data;
}


function uuidAndPageCount($data,$key,$pageCount)
{
    $data['uuid']=$key;
    $data['pageCount']=$pageCount;
    return $data;
}


function updateImage($data) {
    $key="";
    $pageCount=0;
    foreach( data['background'] as &$p)
    {
        $p['filename']="";
        $p['isBg']=True;
        $pageCount+=1;
        if( len(key) == 0)
        {
            $tmp=p['key'];
            $key=tmp[0:tmp.find("_")];
        }
        else
        {
            $tmp=p['key'];
            $p['key']="{}{}".format(key,tmp[tmp.find("_"):]);
        }
    }

  return array(data,key,pageCount);
}


function qmlIncludeMinimal(data)
{
    #print("qmlIncludeMinimal")
    pattern="import \"qrc:/resources/qml/\"";
    newPat="import Rolisteam 1.0";
    qml = data['qml'];
    qml = qml.replace(pattern,newPat);
    data['qml'] = qml;
    return data;
}

function qmlIncludeComplete(data)
{
    #print("qmlIncludeComplete")
    pattern="import \"qrc:/resources/qml/\"";
    newPat="import Rolisteam 1.1";
    qml = data['qml'];
    qml = qml.replace(pattern,newPat);
    data['qml'] = qml;
    return data;
}

function changeDiceButton(data)
{
    #print("DiceButton")
    qml = data['qml'];
    inCheck=False;
    result=[];
    foreach( line in qml.splitlines())
    {
        if(line.find("DiceButton")>-1)
        {
            inCheck=True;
          }
        if(line.find("textColor")>-1 and inCheck)
          {
            line=line.replace("textColor","color");
          }
        elif(line.find("color:")>-1 and inCheck)
        {
            line=line.replace("color","backgroundColor");
            inCheck=False;
          }
        result.append(line);
      }

    data['qml']="\n".join(result);
    return data;
}

function changeTextFieldField(data)
{
    #print("TextFieldField")
    qml = data['qml'];
    inCheck=False;
    result=[];
    foreach (line in qml.splitlines())
    {
        if(line.find("TextFieldField")>-1)
            {inCheck=True}
        if(line.find("textColor")>-1 and inCheck)
        {
            line=line.replace("textColor","color");
          }
        else if(line.find("color:")>-1 and inCheck)
        {
            line=line.replace("color","backgroundColor");
            inCheck=False;
          }
        result.append(line);
    }
    data['qml']="\n".join(result);
    return data;
  }

function changeTextArea(data)
{
    #print("changeTextArea")
    qml = data['qml'];
    inCheck=False;
    result=[];
    foreach (qml.splitlines() as $line)
    {
        if($line.find("TextAreaField")>-1)
        {
            inCheck=True;
        }
        if($line.find("textColor")>-1 and inCheck)
        {
            $line=$line.replace("textColor","color");
        }
        else if($line.find("color:")>-1 and inCheck)
        {
            $line=$line.replace("color","backgroundColor")
            $inCheck=False;
        }
        $result.append($line);
    }

    $data['qml']="\n".join($result)
    return $data;
}

function changeCheckbox($data)
{
    #print("changeCheckbox")
    qml = data['qml'];
    inCheck=False;
    result=[];
    for line in qml.splitlines():
        if(line.find("CheckBoxField")>-1):
            inCheck=True;
        if(line.find("textColor")>-1 and inCheck):
            line=line.replace("textColor","borderColor");
        if(line.find("color:")>-1 and inCheck):
            inCheck=False;
            line="\n";
        result.append(line);

    data['qml']="\n".join(result);
    return data;
  }

function changeTextInputField(data)
{
    #print("changeTextInputField")
    qml = data['qml'];
    inCheck=False;
    result=[];
    foreach(qml.splitlines() as &$line)
    {
        if(line.find("TextInputField")>-1)
        {
            inCheck=True;
          }
        if(line.find("textColor")>-1 and inCheck)
        {
            line=line.replace("textColor","color");
          }
        else if(line.find("color")>-1 and inCheck)
        {
            line=line.replace("color","backgroundColor");
            inCheck=False;
          }



        result.append(line);

      }
    data['qml']="\n".join(result);
    return data;
}

function completeChange(data)
{
    array = updateImage(data);
    data = array[0];
    key = array[1];
    pageCount = array[2];
    data = uuidAndPageCount(data,key,pageCount);
    data = qmlIncludeComplete(data);
    data = changeCheckbox(data);
    data = changeTextInputField(data);
    data = changeTextArea(data);
    data = changeTextFieldField(data);
    data = changeDiceButton(data);
    return data;
}

function minimalChange(data)
{
    array = updateImage(data);
    data = array[0];
    key = array[1];
    pageCount=array[2];
    data = uuidAndPageCount(data,key,pageCount);
    data = qmlIncludeMinimal(data);
    return data;
}

function loadFile($path)
{
  $handle=fopen($path, 'r');
  $data=json_decode($handle);
  return $data;
}

function saveFile($path,$data)
{
    $handle= fopen(path, 'w');
    fwrite($handle, json_encode($data));
    fclose($handle);
}

function main()
{
    $mode=$_POST['complete'] ? ModeEdition.COMPLETE : ModeEdition.COMPLETE;
    $inputFile=$_FILES['uploadedfile']['tmp_name'];
    $outputFile=replace($_FILES['uploadedfile']['name'],"rcs",'_fixed.rcs');

    if ($mode == ModeEdition.NONE)
        echo ("Error: no edition mode: minimal or complete")

    data=loadFile($inputFile)

    if $mode == ModeEdition.MINIMAL:
      $data = minimalChange($data);
    elif mode == ModeEdition.COMPLETE:
        $data = completeChange($data);

    saveFile($outputFile, $data);
}
if(!empty($_POST['submit']))
  main();
?>

<html>
<header>
</header>
<body>
  <form method="post" action="">
    <input type="file" value="" id="source" name="source"/><br/>
    <label for="complete">Use 1.9 style:</label><input type="checkbox" value="" id="complete" name="complete" /><br/>
    <input type="submit" name="convert" value="convert" id="convert" /><br/>
  </form>
</body>
</html>
