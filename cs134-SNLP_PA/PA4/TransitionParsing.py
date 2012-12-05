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

    def getBufferStackPair(self,direction='right'):
        """For a configuration with σ|i and j|β,if direction is left return the pair (j,i);else if right return pair(i,j)"""
    	if direction == 'left':
            return tuple(self.beta.top(),self.sigma.top())
        else if direction == 'right':
            return tuple(self.sigma.top(),self,beta.top())
        else:
            raise(Exception,'right direction input')

class TranSys(object):
    """this class represent the transition system."""
    def __init__(self,transition_codebook):
        self.transition_codebook = transition_codebook
        
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
	
    def Gold_parse(self,sentence):
        """the gold parse algorithm"""

        start_config = self.init_config(sentence)
        config = copy.deepcopy(start_config)
        GS_arcs = self.get_GS_parse(sentence)
        CT_pairs = []
        while not config.is_terminal():
            if config.sigma == start_config.sigma:
		config = shift(config)
                CT_pairs.append(tuple(config,'Shift'))
            else:
                transition_name = oracle(config,GS_arcs)
                transition_func = self.transition_codebook.get_func(transition_name)
                CT_pairs.append(tuple(config,transition_name))
                config = transition_func(config)
			
        return CT_pairs
    
    def oracle(self,config,GS_arcs):
        """the oracle gives the correct transition for the current configuration"""
        if config.getBufferStackPair('left') in GS_arcs:
            return 'LeftArc'
        else if config.getBufferStackPair('right') in GS_arcs:
            return 'RightArc'
        else:
            return 'Shift'


#------------------------
transition_codebook = {'LeftArc':leftArc,
                       'RightArc':rightArc,
                       'Shift':shift}

def leftArc(config):
    
