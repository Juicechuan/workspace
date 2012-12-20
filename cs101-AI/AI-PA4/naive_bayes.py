from __future__ import division
import os
import nltk
from helper import Alphabet, Instance
import numpy as np
import math
import copy
from nltk.corpus import stopwords
from nltk import FreqDist

class Naive_Bayes(object):
    """"""
    def __init__(self, data, feature_function):
        """
        Takes a dictionary mapping labels to lists of strings with that label, and a function which
        produces a list of feature values from a string.
        """
        # your code here!
        self.data = data
        self.feature_codebook = Alphabet()
        # self.word_dict = Alphabet()
        self.label_codebook = Alphabet()
        self.feature_function = feature_function    
                
#     def _build_instance_list(self):
#         """"""
#         instance_list = {}
#         for label, documents in self.data.items():
#             instance_list[label] = []
#             for doc in documents:
#                 vector = self.extract_feature(self.data, doc, s)
#                 instance_list[label].append(vector)
#         self.instance_list = instance_list
#         
#    def _populate_codebook(self):
#         """"""
#         for label in self.instance_list:
#             self.label_codebook.add(label)
#         #here we use all the word set as features
#         self.feature_codebook = copy.deepcopy(self.word_dict)

    def extract_feature(self, string):
        """"""
        vector = np.zeros(self.feature_codebook.size())
        tokens = set(nltk.regexp_tokenize(string, pattern="\w+"))
        indice = 0
        
        for word in tokens:
            if self.feature_codebook.has_label(word):
                indice = self.feature_codebook.get_index(word)
                vector[indice] = 1.

        return vector
                 
    def _collect_counts(self):
        """"""
        self.count_table = np.zeros((self.feature_codebook.size(), self.label_codebook.size()))
        self.count_y_table = np.zeros(self.label_codebook.size())
        for label, docs in self.instance_list.items():
            Y_index = self.label_codebook.get_index(label)
            for vector in docs:
                self.count_y_table[Y_index] += 1.0
                self.count_table[:, Y_index] += vector
                
    def train(self,theta):
        """"""
        self.instance_list = self.feature_function(self.data, self.label_codebook, self.feature_codebook, theta)
        # self._populate_codebook_withSelectFeature()
        #self.instance_list = self.feature_function(self.data, self.label_codebook, self.feature_codebook, select_feature)
        self._collect_counts()
        self.p_x_given_y_table = np.zeros((self.feature_codebook.size(), self.label_codebook.size()))
        self.p_y_table = np.zeros(self.label_codebook.size())

        self.p_x_given_y_table = (self.count_table + 0.2) / (self.count_y_table + self.feature_codebook.size() * 0.2)
        self.p_y_table = self.count_y_table / self.count_y_table.sum()
        
    def compute_log_unnormalized_score(self, feature_vector):
        """Compute log P(X|Y) + log P(Y) for all values of Y
        
        Returns a vector of loglikelihood.
            loglikelihood_vector[0] = log P(X|Y=0) + log P(Y=0)
        """
        loglikelihood_vector = np.zeros(self.label_codebook.size())
        for label in range(0, self.label_codebook.size()):
            logpro = math.log(self.p_y_table[label])
            for feature_index in range(0, self.feature_codebook.size()):        
                    logpro += feature_vector[feature_index] * math.log(self.p_x_given_y_table[feature_index, label]) + (1 - feature_vector[feature_index]) * math.log(1 - self.p_x_given_y_table[feature_index, label])
            loglikelihood_vector[label] = logpro 
        return loglikelihood_vector

    def classify(self, string):
        """
        Classifies a string according to the feature function and training data
        provided at initialization.

        Predict the label of the given instance
        
        return the predict label for the input document
        """
        # your code here!
        feature_vector = self.extract_feature(string)
        logvector = self.compute_log_unnormalized_score(feature_vector)
        # print vector
        pre_label_index = np.argmax(logvector)         
        return self.label_codebook.get_label(pre_label_index)


def bag_of_words(data, label_codebook, feature_codebook, theta):
    """"""
    word_dict = Alphabet()
    stopset = set(stopwords.words('english'))
    for key, value in data.items():
        label_codebook.add(key)
        for doc in value:
            doc_tokens = set(nltk.regexp_tokenize(doc, pattern="\w+"))
            for word in doc_tokens:
                if word not in stopset:
                    word_dict.add(word)
                    
    all_words = word_dict._label_to_index.keys()
    fdict = FreqDist([w for w in all_words])
    word_feature = fdict.keys()[theta:]
    for word in all_words:
        if word in word_feature:
            feature_codebook.add(word)
    
    instance_list = {}
    for label, document_list in data.items():
        instance_list[label] = []
        for document in document_list:
            vector = np.zeros(feature_codebook.size())
            tokens = set(nltk.regexp_tokenize(document, pattern="\w+"))
            indice = 0
            
            for word in tokens:
                if feature_codebook.has_label(word):
                    indice = feature_codebook.get_index(word)
                    vector[indice] = 1.
            instance_list[label].append(vector)
    return instance_list


def bag_of_words_withTrigram(data, label_codebook, feature_codebook, theta):
    """"""
    word_dict = Alphabet()
    stopset = set(stopwords.words('english'))
    for key, value in data.items():
        label_codebook.add(key)
        for doc in value:
            doc_tokens = set(nltk.regexp_tokenize(doc, pattern="\w+"))
            for word in doc_tokens:
                if word not in stopset:
                    word_dict.add(word)
                    
    all_words = word_dict._label_to_index.keys()
    #fdict = FreqDist([w for w in all_words])
    #word_feature = fdict.keys()[theta:]
    for i,word in enumerate(all_words):
        feature_codebook.add(word)
        if i+2 < len(all_words):
        	feature_codebook.add(word+" "+all_words[i+1]+" "+all_words[i+2])
    
    instance_list = {}
    for label, document_list in data.items():
        instance_list[label] = []
        for document in document_list:
            vector = np.zeros(2*feature_codebook.size()-2)
            tokens = set(nltk.regexp_tokenize(document, pattern="\w+"))
            indice = 0
            
            for i,word in enumerate(tokens):
                if feature_codebook.has_label(word):
                    indice = feature_codebook.get_index(word)
                    vector[indice] = 1.
                 if feature_codebook.has_label(word+" "+tokens[i+1]+" "+tokens[i+2]):
                 	indice = feature_codebook.get_index(word+" "+all_words[i+1]+" "+all_words[i+2])
                 	vector[indice] = 1.   
                
            instance_list[label].append(vector)
    return instance_list


def select_feature_function(data, label_codebook, feature_codebook, select_feature):
    """"""
    for key, value in data.items():
        label_codebook.add(key)
    for word in select_feature:
        feature_codebook.add(word)
    
    instance_list = {}
    for label, document_list in data.items():
        instance_list[label] = []
        for document in document_list:
            vector = np.zeros(feature_codebook.size())
            tokens = set(nltk.regexp_tokenize(document, pattern="\w+"))
            indice = 0
            
            for word in tokens:
                if feature_codebook.has_label(word):
                    indice = feature_codebook.get_index(word)
                    vector[indice] = 1.
            instance_list[label].append(vector)
    return instance_list
    
def load_data(directory):
    """
    Given a pathname of a directory, creates a list of strings out of the
    contents of the files in that directory.
    """
    data_strings = []
    file_list = os.listdir(directory)
    for filename in file_list:
        pathname = os.path.join(directory, filename)
        data_strings.append(open(pathname).read())
    return data_strings

def print_evaluation(classifier, test_data):
    """
    Takes a classifier and a dictionary mapping labels to lists of test strings.
    Prints accuracy, precision, and recall scores for the classifier.
    """
    scores = {}
    correct = 0
    total = 0
    labels = test_data.keys()
    for label in labels:
        scores[label] = {"true_pos":0, "true_neg":0, "false_pos":0, "false_neg":0}
    for label in test_data:
        for string in test_data[label]:
            classification = classifier.classify(string)
            total += 1
            if classification == label:
                correct += 1
                scores[label]["true_pos"] += 1
                for other_label in labels:
                    if other_label != label:
                        scores[other_label]["true_neg"] += 1
            else:
                scores[label]["false_neg"] += 1
                scores[classification]["false_pos"] += 1
                for other_label in labels:
                    if other_label != label and other_label != classification:
                        scores[other_label]["true_neg"] += 1
    print "Accuracy: " + str(correct / total)
    for label in labels:
        true_pos = scores[label]["true_pos"]
        false_pos = scores[label]["false_pos"]
        true_neg = scores[label]["true_neg"]
        false_neg = scores[label]["false_neg"]
        print str(label)
        precision = true_pos / (true_pos + false_pos)
        recall = true_pos / (true_pos + false_neg)
        print "\tPrecision: " + str(precision)
        print "\tRecall: " + str(recall)
        print "\tF-Measure: " + str(2 * precision * recall / (precision + recall))
        
                


            
            
# Examples of how to use the print_evaluation function. The bag_of_words
# function will need to be written for this to work.
movie_train = {"pos":load_data("movie_train/pos"), "neg":load_data("movie_train/neg")}
movie_test = {"pos":load_data("movie_test/pos"), "neg":load_data("movie_test/neg")}
classifier = Naive_Bayes(movie_train,bag_of_words)
classifier.train(5000)
print_evaluation(classifier,movie_test)
# 
# print"\r\n"
# select_feature = "good bad terrible awful great wonderful amazing disaster interesting boring fun bland".split()
# classifier = Naive_Bayes(movie_train, select_feature_function)
# classifier.train(select_feature)
# print_evaluation(classifier, movie_test)

print"\r\n"

twitter_train = {"dutch":load_data("twitter_train/dutch"), "english":load_data("twitter_train/english"),"french":load_data("twitter_train/french"),"german":load_data("twitter_train/german"),"italian":load_data("twitter_train/italian"),"spanish":load_data("twitter_train/spanish")}
twitter_test = {"dutch":load_data("twitter_test/dutch"), "english":load_data("twitter_test/english"),"french":load_data("twitter_test/french"),"german":load_data("twitter_test/german"),"italian":load_data("twitter_test/italian"),"spanish":load_data("twitter_test/spanish")}
classifier = Naive_Bayes(twitter_train,bag_of_words)
classifier.train(2000)
print_evaluation(classifier,twitter_test)         
