#!usr/bin/python

"""Extract the feature from the trainning file"""
import sys
import string
from nltk import metrics,stem,tokenize,tree
from util import Document,Pair,Entity
import copy
from feature_functions import *

def extract_contextual(postagged_file):
    """extract the contextual information as lists"""
    raw_data = open(postagged_file,'r')
    sentence_list = []

    for rline in raw_data.readlines():
        if rline.strip():
            tagged_tokens = rline.split()
            sentence = [tuple(w.split("_")) for w in tagged_tokens]
            sentence_list.append(sentence)

    raw_data.close()
    return sentence_list

def extract_syntax(parsed_file):
    """get the parsed tree"""
    parsed_data = open(parsed_file,'r')
    tree_list = []

    for l in parsed_data.readlines():
        if l.strip():
            parsed_sentence = tree.Tree.parse(l.strip())
            tree_list.append(parsed_sentence)

    parsed_data.close()
    return tree_list

def load_data(input_file):
    
    raw_data = open(input_file,'r')

    doc_list = []
    doc = Document()
    ne_dict = {}
    for rline in raw_data.readlines():
        if rline.strip():
            i = 0
            entry = rline.split()
            if len(entry) == 14:
                i = 1
            docID = entry[i]
            #new document
            if docID != doc.docID:
                #import pdb
                #if doc.docID!='':
                #    pdb.set_trace()
                
                #record the name entity dictionary we have created
                doc.set_ne_dict(ne_dict)
                doc_list.append(doc)
                ne_dict = {}
                doc = Document(docID)
                first = Entity(entry[i+1],(entry[i+2],entry[i+3]),entry[i+4],entry[i+5],entry[i+6])
                ne_dict[entry[i+5]] = (entry[i+1],entry[i+2]) 
                second = Entity(entry[i+7],(entry[i+8],entry[i+9]),entry[i+10],entry[i+11],entry[i+12])
                ne_dict[entry[i+11]] = (entry[i+7],entry[i+8])
                pair = Pair(first,second)
                if i:
                    pair.set_label(entry[0])
                doc.add_pair(pair)
            else:
                first = Entity(entry[i+1],(entry[i+2],entry[i+3]),entry[i+4],entry[i+5],entry[i+6])
                ne_dict[entry[i+5]] = (entry[i+1],entry[i+2]) 
                second = Entity(entry[i+7],(entry[i+8],entry[i+9]),entry[i+10],entry[i+11],entry[i+12])
                ne_dict[entry[i+11]] = (entry[i+7],entry[i+8])
                pair = Pair(first,second)
                if i:
                    pair.set_label(entry[0])
                doc.add_pair(pair)
    doc.set_ne_dict(ne_dict)
    doc_list.append(doc)
    return doc_list
                
def output_features(output_file,feature_list):
    output_data = open(output_file,'w')
    
    for w in feature_list:
        label = w[0]
        if label != '':
            output_data.write(label)
        feature_vector = w[1]
        for key,value in feature_vector.items():
            output_data.write((" %s=%s")%(key,value))
        output_data.write("\n")
    
    output_data.close()

def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    doc_list = load_data(input_file)
    feature_list = []
    #the first doc is empty one
    for doc in doc_list[1:]:
        postagged_file = "data/postagged-files/"+doc.docID+".head.rel.tokenized.raw.tag"
        parsed_file = "data/parsed-files/"+doc.docID+".head.rel.tokenized.raw.parse"
        pos_tagged_sentences = extract_contextual(postagged_file)
        parsed_sentences = extract_syntax(parsed_file)
        print "processing "+doc.docID+"...\n"
        for pair in doc.pair_list:
            feature_dict = {}
            #word feature
            feature_dict["headword1"] = pair.first.str
            feature_dict["headword2"] = pair.second.str
            feature_dict["HM12"] = pair.first.str + pair.second.str
            WB = get_WB(pair,pos_tagged_sentences)
            if WB == 0:
                feature_dict["WBNULL"] = True
            elif isinstance(WB,str):
                feature_dict["WBFL"] = WB
            elif isinstance(WB,tuple):
                feature_dict["WBF"] = WB[0]
                feature_dict["WBL"] = WB[2]
                feature_dict["WBO"] = WB[1]
            feature_dict["BM1F"] = get_BM1F(pair,pos_tagged_sentences) 
            feature_dict["BM1L"] = get_BM1L(pair,pos_tagged_sentences) 
            feature_dict["AM2F"] = get_AM2F(pair,pos_tagged_sentences) 
            feature_dict["AM2L"] = get_AM2L(pair,pos_tagged_sentences) 
            feature_dict["ET12"] = get_ET12(pair)

            #Overlap feature
            feature_dict["#MB"] = getNumMB(pair,doc.ne_dict,pos_tagged_sentences)
            feature_dict["#WB"] = getNumWB(pair,pos_tagged_sentences)
            #base phrase chunking
            CPHB = get_CPHB(pair,parsed_sentences)
            #if CPHB == 0:
            #    feature_dict["CPHBNULL"] = True
            #elif isinstance(CPHB,str):
            #    feature_dict["CPHBFL"] = CPHB
            #elif isinstance(CPHB,tuple):
            #    feature_dict["CPHBF"] = CPHB[0]
            #    feature_dict["CPHBL"] = CPHB[2]
            #    feature_dict["CPHBO"] = CPHB[1]
            CPHBM1 = get_CPHBM1(pair,parsed_sentences)
            #feature_dict["CPHBM1F"] = CPHBM1[0]
            #feature_dict["CPHBM1L"] = CPHBM1[1]
            CPHAM2 = get_CPHAM2(pair,parsed_sentences)
            #feature_dict["CPHAM2F"] = CPHAM2[0]
            #feature_dict["CPHAM2L"] = CPHAM2[1]
            
            #Parse Tree
            feature_dict["PTP"] = get_PTP(pair,parsed_sentences)
            #feature_dict["PTPH"] = get_PTPH(pair,parsed_sentences)
            feature_list.append((pair.label,feature_dict))
            
    output_features(output_file,feature_list)
    
if __name__ == "__main__":
    main()
