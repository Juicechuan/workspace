# -*- coding: utf-8 -*-
"""Implementation of the Transition-Based dependency parsing
   Using the MaxEnt classifier
"""

from util import Stack, Buffer
import copy
from helper import Instance
#--------------------
class Configuration(object):
    """a wrapper class for the configurations in the transition system,
       which contains:
       1) sigma: a stack of tokens 
       2) beta: a buffer of tokens 
       3) A: a set of dependency arcs in which the arcs h(i)=j are represented by the tuple(j,i)
    """
    def __init__(self, sigma, beta, A):
        self.sigma = sigma
        self.beta = beta
        self.A = A
        
    def is_terminal(self):
        """test if the current configuration is terminal"""
        return self.beta.isEmpty()

    def getBufferStackPair(self, direction='right'):
        """For a configuration with sigma|i and j|beta,if direction is left return the pair (j,i);else if right return pair(i,j)"""
        if direction == 'left':
            return tuple((self.beta.top(), self.sigma.top()))
        elif direction == 'right':
            return tuple((self.sigma.top(), self.beta.top()))
        else:
            raise(Exception, 'right direction input')
    def one_head_test(self, item):
        """test whether the item has already become some token's head in the configuration dependency arcs."""
        v = [i for i, j in self.A if j == item]
        return len(v) == 0
    
    def __str__(self):
        return str(self.sigma.list) + ' ' + str(self.beta.list) + ' ' + str(self.A)  

class TranSys(object):
    """this class represent the transition system."""
    def __init__(self, transition_codebook):
        self.transition_codebook = transition_codebook
        self.token_dict = {}
    def init_config(self, sentence):
        """given the sentence, generate the initial configuration"""
        self.token_dict = dict([(element[0], element[1]) for element in sentence])
        self.token_dict[0] = 'root'
        self.POS_dict = dict([(element[0], element[2]) for element in sentence])
        self.POS_dict[0] = 'ROOT'
        self.GS_arcs = self.get_GS_parse(sentence)
        sigma = Stack([0])
        beta = Buffer(range(1, len(sentence) + 1))
        A = set()
        return Configuration(sigma, beta, A)

    def get_GS_parse(self, sentence):
        """given the sentence from the training set, get the correct dependency 
           parse(the correct dependency arcs).
        """
        GS_parse_arcs = []
        for word in sentence:
            GS_parse_arcs.append(tuple((word[3], word[0])))
            
        return GS_parse_arcs
    
    def Gold_parse(self, sentence):
        """the gold parse algorithm"""

        start_config = self.init_config(sentence)
        config = copy.deepcopy(start_config)
        # GS_arcs = self.get_GS_parse(sentence)
        CT_pairs = []
        while not config.is_terminal():
            if config.sigma == start_config.sigma:
                shift(config)
                # config1=copy.deepcopy(config)
                # CT_pairs.append(tuple(config1,'Shift'))
            else:
                transition_name = self.oracle(config)
                # print transition_name
                transition_func = self.transition_codebook[transition_name]
                config2 = copy.deepcopy(config)
                CT_pairs.append(tuple((config2, transition_name)))
                transition_func(config)
            
        return CT_pairs
    
    def oracle(self, config):
        """the oracle gives the correct transition for the current configuration"""
       # print config.getBufferStackPair()
       # print GS_arcs
        if config.getBufferStackPair('left') in self.GS_arcs:
            return 'LeftArc'
        elif config.getBufferStackPair('right') in self.GS_arcs:
            return 'RightArc'
        else:
            return 'Shift'
            
    def getBufferChildren(self, buffertop):
        """return the buffer top's children according to the GS_arcs"""
        children = [v for k, v in self.GS_arcs if k == buffertop]
        return children
        
    def feature_extract(self, CT_pairs):
        """extract features from the configuration and transition pairs;
           return the instance list for one sentence
        """
        instances = []
        for pair in CT_pairs:
            config = pair[0]
            label = pair[1]
            data = []
            featureset = {}
            
            # for nltk NaiveBayes feature selection stuff when doing MaxEnt decoding parser commit this
#             featureset["topOfBuffer"] = self.token_dict[config.beta.top()]
#             featureset["topOfStack"] = self.token_dict[config.sigma.top()]
#             featureset["bufferStackPair"] = (self.token_dict[config.sigma.top()], self.token_dict[config.beta.top()])
#             featureset["topOfBuffer"] = self.POS_dict[config.beta.top()]
#             featureset["topOfStack"] = self.POS_dict[config.sigma.top()]
#             featureset["bufferStackPair"] = tuple((self.POS_dict[config.sigma.top()], self.POS_dict[config.beta.top()]))
            
            # add the (StackTopPOS,BufferTopPOS,bufferchildren_POS) feature
            #value_set = tuple([self.POS_dict[config.sigma.top()], self.POS_dict[config.beta.top()]] + [self.POS_dict[child] for child in self.getBufferChildren(config.beta.top())])
            #featureset["bufferStackbufferChildrenPair"] = value_set
            
            # for MaxEnt decoding stuff
            # token variants
            data.append(("topOfBuffer",self.token_dict[config.beta.top()]))
            data.append(("topOfStack",self.token_dict[config.sigma.top()]))
            data.append(("bufferStackPair",self.token_dict[config.sigma.top()],self.token_dict[config.beta.top()]))
            #POS variants
            data.append(("topOfBuffer",self.POS_dict[config.beta.top()]))
            data.append(("topOfStack",self.POS_dict[config.sigma.top()]))
            data.append(("bufferStackPair",self.POS_dict[config.sigma.top()],self.POS_dict[config.beta.top()]))
            ins = Instance(label=label, data=data)
            #ins = Instance(label=label, data=featureset)
            instances.append(ins)
        
        return instances
                
    def decode_parser(self, classifier, sentence):
        """This function parse the sentence with the classifier as oracle
           return the arc set
        """
        start_config = self.init_config(sentence)
        config = copy.deepcopy(start_config)
        
        while not config.is_terminal():
            if config.sigma == start_config.sigma:
                shift(config)
            else:
                # here the feature extraction will only return one instance instead of instance list
                instance = self.feature_extract([(config, '')])
                transition_name = classifier.label_codebook.get_label(classifier.classify_instance(instance[0]))
                transition_func = self.transition_codebook[transition_name]
                transition_func(config)
        # print config.A
        new_sentence = sentence[:]
        for i, element in enumerate(sentence):
            arc = [(k, v) for k, v in config.A if v == element[0]]
            # print arc
            if len(arc) > 1:
                # raise Exception("Error: one word must have one head\n")
                print "Error: one word must have one head\n"
            if arc != []:
                header = arc[0][0]
            else:
                header = 0
            new_sentence[i] = tuple((element[0], element[1], element[2], header, element[4]))
            
        return new_sentence

#------------------------
# transition_codebook = {'LeftArc':leftArc,
#                       'RightArc':rightArc,
#                       'Shift':shift}

# def leftArc(config):
#     j,i = config.getBufferStackPair('left')
#     if i != 0 and config.one_head_test(i):
#         config.sigma.pop()
#         config.A.add((j,i))
# 
# def rightArc(config):
#     i,j = config.getBufferStackPair('right')
#     if config.one_head_test(j):
#         config.A.add((i,j))
#         config.beta.pop()
#         config.beta.push(config.sigma.top())
#         config.beta.pop()
# 
# def shift(config):
#     config.sigma.push(config.beta.top())
#     config.beta.pop()
def leftArc(config):
    j, i = config.getBufferStackPair('left')
    # if i != 0 and config.one_head_test(i):
    config.sigma.pop()
    config.A.add((j, i))

def rightArc(config):
    i, j = config.getBufferStackPair('right')
    # if config.one_head_test(j):
    config.A.add((i, j))
    config.beta.pop()
    config.beta.push(config.sigma.top())
    config.beta.pop()

def shift(config):
    config.sigma.push(config.beta.top())
    config.beta.pop()
