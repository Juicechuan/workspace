#!/usr/bin python

"""main.py: In this file I extract the feature from .txt files and we assume that the training process uses the 
raw_data of instance to train while the testing precess using the data of instance to test. But for #convenience of using the test_naive_bayes.py, I populate the data and raw_data of instance at the same time"""

# coding: utf-8
import nltk
from helper import Alphabet, Instance
from hmm import HMM
import util
import evaluator
#import random
#import argparse


__author__ = "chuan"



#get the feature selection function number
#parser = argparse.ArgumentParser(description ='choose certain feature selection fucntion')
#parser.add_argument('ID',metavar='N',type=int)
#parser.add_argument('limits', metavar='N',type=int)
#args = parser.parse_args()
#ID = args.ID
#limits = args.limits

util.label_codebook.add('B')
util.label_codebook.add('I')
util.label_codebook.add('O')

def load_instance(filename):
	"""load the data into codebooks and populate the instance_list
	   parameters: name of the file to load data from.
	   return: list of instance"""
	ins_list=[]
	f = open(filename,'r')
	label = []
	data = []
	for lines in f:
		if lines.strip():
			datapoint = lines.split()
			label.append(datapoint[0])
			data.append((datapoint[1],datapoint[2]))
			if not util.feature_codebook.has_label(datapoint[1]):
				util.feature_codebook.add(datapoint[1])
			if not util.feature_codebook.has_label(datapoint[2]):
				util.feature_codebook.add(datapoint[2])
		else:
			ins = Instance(label=label,data=data)
			ins_list.append(ins)
			label = []
			data = []	
	return ins_list

hmm = HMM()
train_instance_list = load_instance("np_chunking_wsj_15_18_train")
test_instance_list = load_instance("np_chunking_wsj_20_test")
#hmm.train(train_instance_list)
#get the confusion matrix
accuracy=evaluator.split_train_test(hmm,train_instance_list,(0.5,0.5))
#print accuracy
#hmm.train_semisupervised(test_instance_list)
cm = evaluator.test_classifier(hmm,test_instance_list)
cm.print_out()


