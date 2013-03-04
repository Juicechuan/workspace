"""this script extracts the features for the (training)raw data, and output the features 
in additional columns in the output_file"""
#usage:feature_extract.py [input_file][output_feature]

import sys
import string
import re

def isFirst(entry):
    """check if it is the first word in the sentence"""
    return entry[0] == '0'

def isInitCaps(entry):
    """check the word starts with a capital letter"""
    return entry[1][:1].isupper()
def isMixedCaps(entry):
    """check If it starts with a lower case letter, 
       and contains both upper and lower case letters"""
    if entry[1][:1].islower() and not entry[1][1:].islower():
        return True
    return False

def isAllCaps(entry):
    """check If it is made up of all capital letters"""
    return entry[1].isupper()

def isEndWithPeriod(entry):
    """check if ends with a period"""
    return entry[1][-1]=="."

def isOnlyOneCap(entry):
    """check if Contains only one capital letter"""
    return (len(entry[1])==1 and entry[1].isupper())

def isContainsDigit(entry):
    """check if Contains a digit"""
    for char in entry[1]:
        if char in string.digits:
            return True
    return False

def is2digits(entry):
    """check if made up of 2 digits"""
    return (entry[1].isdigit() and len(entry[1])==2)

def is4digits(entry):
    """check if made up of 4 digits"""
    return (entry[1].isdigit() and len(entry[1])==4)

def isDigitSlash(entry):
    """check if Made up of digits and slash"""
    match = re.match('[0-9]*\/+[0-9]*',entry[1])
    return match!=None

def isContainsDollar(entry):
    """check if Contains a dollar sign"""
    return entry[1].find('$')!=-1

def isContainsPercent(entry):
    """check if Contains a percent sign"""
    return entry[1].find('%')!=-1

def isContainsPeriod(entry):
    """Contains period"""
    return entry[1].find('.')!=-1

def extract_feature(sentence):
    """feature set one;
       given one sentence, extract features we want
       and return a list of dictionaries of feature name-value pairs
    """
    #isCaps = False
    #isFirst = False
    
    feature_list = []
    init_feature_dict = {"First":False,
                    "initCaps":False,
                    "allCaps":False,
                    "mixedCaps":False}
    for entry in sentence:
        feature_dict = init_feature_dict.copy()
        feature_dict["allCaps"] = isAllCaps(entry)
        feature_dict["mixedCaps"] = isMixedCaps(entry)
        feature_dict["First"] = isFirst(entry)
        feature_dict["initCaps"] = isInitCaps(entry)
        
#        if isFirst(entry) and isCaps(entry):
#            feature_dict["First_Caps"] = True
#        elif not isFirst(entry) and isCaps(entry):
#            feature_dict["notFirst_Caps"] = True
#        elif isFirst(entry) and not isCaps(entry):
#            feature_dict["First_notCaps"] = True
        
        feature_list.append(feature_dict)
    return feature_list    

def main():
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    raw_data = open(input_file,'r')
    output_data = open(output_file,'w')

    raw_tag_list = []
    new_tag_list = []

    sentence = []
    for rline in raw_data.readlines():
        if rline.strip():
            entry = rline.split()
            sentence.append(entry)
        else:
            raw_tag_list.append(sentence)
            sentence = []

    for sen in raw_tag_list:
        feature_list = extract_feature(sen)
        for entry,feature_dict in zip(sen,feature_list):
            new_tag_line = "{}\t{:<10}\t{:<5}".format(entry[0],entry[1],entry[2])
            for key,value in feature_dict.items():
                new_tag_line += "  "+str(value)
            if len(entry) == 4:
                new_tag_line += "  "+entry[3]+"\n"
            else:
                new_tag_line += "\n"
            
            output_data.write(new_tag_line)
        output_data.write("\n")

    output_data.close()

if __name__=="__main__":
    main()
