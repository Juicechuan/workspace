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
sentence_instances = load_sentence("data/wsj.00.01.22.24.conll")
test_sentence_instances = load_sentence("data/wsj.23.conll")
#sentence_instances = load_sentence("data/test")
#test_sentence_instance = load_sentence("data/test")

transition_codebook = {'LeftArc':leftArc,
                       'RightArc':rightArc,
                       'Shift':shift}

tranSys = TranSys(transition_codebook)
instance_list = []
test_instance_list = []
sentence_list = []
for sentence,test_sentence in zip(sentence_instances,test_sentence_instances):
    CT_pairs = tranSys.Gold_parse(sentence)
    #print [c.sigma.list for c,t in CT_pairs]
    instances = tranSys.feature_extract(CT_pairs)
    instance_list += instances 
    
    #for testing the classifier 
    test_CT_pairs = tranSys.Gold_parse(test_sentence)
    test_instances = tranSys.feature_extract(test_CT_pairs)
    test_instance_list += test_instances
    
#----------------------------------
#training the NaiveBayes Classifier in nltk
# import nltk
# featuresets = [(instance.data,instance.label) for instance in instance_list]
# testsets = [(instance.data,instance.label) for instance in test_instance_list]
# train_set,test_set = featuresets[:],testsets[:] 
# classifier = nltk.NaiveBayesClassifier.train(train_set) 
# print nltk.classify.accuracy(classifier, test_set)
# #print classifier.labels()
# CM = test_classifier(classifier,test_set)
# CM.print_out()
#----------------------------------  
#ME = MaxEnt()
#ME.train(instance_list)
#ME.save("dependency_parsing_classifier.json")
#finish training
#----------------------------------
#testing parser
ME = MaxEnt.load("dependency_parsing_classifier.json")
# CM = test_classifier(ME,test_instance_list)
# CM.print_out()
tranSys = TranSys(transition_codebook)
wfile = open('parser.conll','w')
for test_sentence in test_sentence_instances:
	new_sentence = tranSys.decode_parser(ME,test_sentence)
	for element in new_sentence:
		if element[0] != 0:
			#wfile.write('{0:<10}{1:<15}{2:<10}{3:<10}{4:<10}{5:<10}{6:<10}{7:<10}{8:<10}{9:<10}'.format(element[0],element[1],'_',element[2],element[2],'_',element[3],'_','_','_'))
			wfile.write(str(element[0])+'\t'+str(element[1])+'\t'+'_'+'\t'+str(element[2])+'\t'+str(element[2])+'\t'+'_'+'\t'+str(element[3])+'\t'+str(element[4])+'\t'+'_'+'\t'+'_')
			wfile.write("\n")	
	wfile.write("\r\n")

wfile.close()

