"""Implementation of the Transition-Based dependency parsing
   Using the MaxEnt classifier
"""

from util import Stack,Buffer
import copy
#--------------------
class Configuration(object):
    """a wrapper class for the configurations in the transition system,
       which contains:
       1) sigma: a stack of tokens 
       2) beta: a buffer of tokens 
       3) A: a set of dependency arcs in which the arcs h(i)=j are represented by the tuple(j,i)
    """
    def __init__(self,sigma,beta,A):
        self.sigma = sigma
        self.beta = beta
        self.A = A
        
    def is_terminal(self):
    	"""test if the current configuration is terminal"""
    	return self.beta.isEmpty()
    	
class TranSys(object):
    """this class represent the transition system."""
    def __init__(self):
        
    def init_config(self,sentence):
        """given the sentence, generate the initial configuration"""
        sigma = Stack([0])
        beta = Buffer(range(1,len(sentence)+1))
        A = set()
        return Configuration(sigma,beta,A)

    def get_GS_parse(self,sentence):
        """given the sentence from the training set, get the correct dependency 
           parse(the correct dependency arcs).
        """
        GS_parse_arcs = []
        for word in sentence:
        	GS_parse_arcs.append(tuple(word[3],word[0]))
        	
        return GS_parse_arcs
	
	def Gold-parse(self,sentence):
		""""""
		start_config = self.init_config(sentence)
		config = copy.deepcopy(start_config)
		GS_arcs = self.get_GS_parse(sentence)
		CT_pairs = []
		while not config.is_terminal():
			if config.sigma == start_config.sigma:
				
			
        
