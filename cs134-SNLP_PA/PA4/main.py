# -*- coding: utf-8 -*-
#import nltk
#import numpy as np
#from maxent import MaxEnt
#from helper import Instance
#import util
#import evaluator
from TransitionParsing import TranSys,leftArc,rightArc,shift
from maxent import MaxEnt
from evaluator import test_classifier

def load_sentence(fname):
    f = open(fname,'r')
    raw_data = []
    sentence = [] 
    for line in f:
        if line.strip():
            line = line.split()
            word_index = line[0]
            token = line[1]
            POS = line[3]
            head_index = line[6]
            label = line[7]
            element = tuple((int(word_index),token,POS,int(head_index),label))
            sentence.append(element)
        else:
            raw_data.append(sentence)
            #print sentence
            sentence=[]
            
    return raw_data

#--------------------------
#sentence_instances = load_sentence("data/wsj.00.01.22.24.conll")
#test_sentence_instance = load_sentence("data/wsj.23.conll")
sentence_instances = load_sentence("data/test")
test_sentence_instance = load_sentence("data/test")

transition_codebook = {'LeftArc':leftArc,
                       'RightArc':rightArc,
                       'Shift':shift}

tranSys = TranSys(transition_codebook)
instance_list = []
test_instance_list = []
for sentence,test_sentence in zip(sentence_instances,test_sentence_instance):
    CT_pairs = tranSys.Gold_parse(sentence)
    test_CT_pairs = tranSys.Gold_parse(test_sentence)
    #print [c.sigma.list for c,t in CT_pairs]
    instances = tranSys.feature_extract(CT_pairs)
    test_instances = tranSys.feature_extract(test_CT_pairs)
    instance_list += instances 
    test_instance_list += test_instances

ME = MaxEnt()
ME.train(instance_list)
ME.save("dependency_parsing_classifier.json")
#ME1 = MaxEnt.load("dependency_parsing_classifier.json")
CM = test_classifier(ME,test_instance_list)
CM.print_out()
