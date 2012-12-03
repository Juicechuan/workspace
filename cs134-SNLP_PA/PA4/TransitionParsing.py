"""Implementation of the Transition-Based dependency parsing
   Using the MaxEnt classifier
"""

class Configuration(object):
    """a wrapper class for the configurations in the transition system,
       which contains:
       1) sigma: a stack of tokens 
       2) beta: a buffer of tokens 
       3) A: a set of dependency arcs in which the arcs i->j are represented by the tuple(i,j)
    """
    def __init__(self,sigma,beta,A):
        self.sigma = sigma
        self.beta = beta
        self.A = A
        
class TranSys(object):
    """this class represent the transition system."""
    def __init__(self):
        
    def init_config(self,sentence):
        """given the sentence, generate the initial configuration"""
        sigma = [0]
        beta = range(1,len(sentence)+1)
        A = set()

    def get_GS_parse(self,sentence):
        """given the sentence from the training set, get the correct dependency 
           parse.
        """



        
