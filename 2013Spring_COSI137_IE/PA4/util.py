#!usr/bin/python

"""Useful structure for the organization"""
import string
import copy

class Document:
    """Represent the doc"""
    def __init__(self,docID="",pair_list=[]):
        self.docID = docID
        self.pair_list = list(pair_list)

    def add_pair(self,pair):
        self.pair_list.append(pair)

    def set_ne_dict(self,ne_dict):
        self.ne_dict = copy.deepcopy(ne_dict)
        

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
    def __init__(self,sentenceID,offsets,type,entityID,str):
        self.sentenceID = eval(sentenceID)
        self.offsets = (eval(offsets[1]),eval(offsets[1]))
        self.type = type
        self.entityID = entityID
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



    
        
