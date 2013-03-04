"""this script extracts the features for the (training)raw data, and output the features 
in additional columns in the output_file"""
#usage:feature_extract.py [input_file][output_feature]

import sys
import string
import re
import collections
import copy
from util import *

from namelist import extract_FWL

def write_features(output_file,doc_list):

    new_tag_line = ""
    output_data = open(output_file,'w')

    for doc in doc_list:
        for sent in doc.sent_list:
            for entry,feature_dict in zip(sent.entry_list,sent.feature_list):
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

def main():
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    raw_data = open(input_file,'r')

    #raw_tag_list = []
    #new_tag_list = []

    #sentence = []
    #zone = ""
    
    FWL_list = extract_FWL(input_file)
    sentence = Sent()
    doc = None
    doc_list  = []

    
    for rline in raw_data.readlines():
        if rline.strip():
            entry = rline.split()
            if re.match('\w{3}\d{8}.\d{4}.\d{4}',entry[1]):
                if doc!=None:
                    doc.extract_global_feature()
                    doc_list.append(doc)
                doc = Documt()
            sentence.add(entry)
        else:
            sentence.extract_zone()
            sentence.extract_local_feature(FWL_list)
            #raw_tag_list.append((sentence,zone))
            doc.add(sentence)
            sentence = Sent()
    doc.extract_global_feature()
    doc_list.append(doc)
    
    write_features(output_file,doc_list)

if __name__=="__main__":
    main()
