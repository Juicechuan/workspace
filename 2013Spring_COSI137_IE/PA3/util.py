#!usr/bin/python

"""Useful structure for the organization"""
import string

class Document:
    """Represent the doc"""
    def __init__(self,docID="",pair_list=[]):
        self.docID = docID
        self.pair_list = list(pair_list)

    def add_pair(self,pair):
        self.pair_list.append(pair)

class Pair:
    """the coreference pair with first second entity pair"""
    def __init__(self,first,second):
        self.first = first
        self.second = second
        self.label = ''
    def set_label(self,label):
        self.label = label


class Entity:
    """the entity"""
    def __init__(self,sentenceID,offsets,type,str):
        self.sentenceID = sentenceID
        self.offsets = offsets
        self.type = type
        self.str = str


def format_contextual(postagged_file):
    """format the sentences to be parsed"""
    raw_data = open(postagged_file,'r')
    output_file = open(postagged_file[:-4]+".sen",'w')
    sentence_list = []

    for rline in raw_data.readlines():
        if rline.strip():
            tagged_tokens = rline.split()
            output_file.write("<s>")
            for w in tagged_tokens:
                if w[:2]!= "__":
                    output_file.write(" "+w.split("_")[0])
                else:
                    output_file.write(" _")
            output_file.write(" </s>\n")
    output_file.close()
    raw_data.close()



    
        
