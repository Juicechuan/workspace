#import nltk
#import numpy as np
#from maxent import MaxEnt
#from helper import Instance
#import util
#import evaluator

def load_sentence(fname):
    f = open(fname,'r')
    data_instance = []
    sentence = [] 
    for line in f:
        if not line.strip():
            line = line.split()
            word_index = line[0]
            token = line[1]
            POS = line[3]
            head_index = line[6]
            label = line[7]
            element = tuple(word_index,token,POS,head_index,label)
            sentence.append(element)
        else:
            data_instance.append(sentence)
            sentence=[]
            
    return data_instance
            
