"""
William Tarimo
PA3: Superchunking - creating larger constituents from chunked data
COSI 114
3/25/2013
"""

from nltk.tree import Tree
from nltk.corpus import treebank_chunk
lines = [line[:-1]+'.pos' for line in open('indices.txt','r').readlines()]
dev_test = treebank_chunk.chunked_sents(lines)
test_sentences =treebank_chunk.chunked_sents(['wsj_0156.pos','wsj_0160.pos',\
    'wsj_0163.pos','wsj_0165.pos','wsj_0167.pos','wsj_0170.pos','wsj_0175.pos',\
    'wsj_0187.pos','wsj_0195.pos','wsj_0196.pos'])

sentence = treebank_chunk.chunked_sents('wsj_0154.pos')[0]

def super_chunk(tagged_sentence):
    """Takes in a POS-tagged sentence and returns a super-chunked tree"""
    #groups identical consecutives POS tokens to ease parsing
    sentence = merge_sentence(tagged_sentence)
    #gets indices (start,end) of all chunks from all qualifying rules
    matches = [rule.match(sentence) for rule in rules if rule.match(sentence)]
    
    #Removes overlapping chunks by deleting the right overlapping chunk(s)
    matches = [range(s,e+1) for (s,e) in [val for subl in matches for val in subl]]
    for i in range(len(matches)-1,0,-1):
        if set(matches[i]).intersection(set([val for subl in matches[:i] for val in subl])):
            junk = matches.pop(i)
    matches = [(item[0],item[-1]) for item in matches]
    matches = [actual_index(start,end,sentence) for (start,end) in matches]
    
    #Creates a SNP subtree of items [start:end] at index start
    matches.sort()
    matches.reverse()
    for (start,end) in matches:
        tagged_sentence[start:end] = [Tree('SNP',tagged_sentence[start:end])]
    return tagged_sentence


def actual_index(start,end,sentence):
    """Takes 2 indices and POS-merged sentence and returns corresponding
    indices in the original sentence"""
    return (sum([num for (pos,num) in sentence[:start]]),\
            sum([num for (pos,num) in sentence[:end]]))
    
def merge_sentence(sent):
    """Takes in a chunked sentence and returns a counted grouping of
    similar consecutive POS tokens"""
    merge = [('**',0)]
    for i in range(len(sent)):
        if isinstance(sent[i],Tree):
            if [pos for (token,pos) in sent[i][:]].count('NNP'):
                #This detects NPs for places, people and organizations
                if merge[-1][0]=='PPO': merge[-1] = ('PPO',merge[-1][1]+1)
                else: merge.append(('PPO',1))
            else:
                if merge[-1][0]=='NP': merge[-1] = ('NP',merge[-1][1]+1)
                else: merge.append(('NP',1))
        else:
            if merge[-1][0]==sent[i][1]: merge[-1] = (merge[-1][0],merge[-1][1]+1)
            else: merge.append((sent[i][1],1))
            
    return merge[1:]

class Rule(object):
    """Implements rules structure and methods used in super-chunking"""
    def __init__(self,rule):
        self.rule = rule #rule is an equivalent of a regular expression sequence

    def get_starts(self,sentence):
        """Returns all possible rule starting points from the sentence"""
        starts = []
        r_index=-1
        r_start = self.rule[0][0]
        for (pos,count) in sentence:
            r_index+=1
            if r_start == pos: starts.append(r_index)

        return starts

    def match(self,sentence):
        """Takes in a POS-processed chunked sentence and returns a tuple of indices
        (start,end) of a matched superchunk rule within the sentence"""
        starts = self.get_starts(sentence)
        matches=[]
        for r_index in starts:
            index = r_index
            for i in range(len(self.rule)):
                if index >= len(sentence) and sum([num for (pos,num) in self.rule[i:]])>0:
                    break #Sentence ran out before satisfying rule
                if self.rule[i][0] != sentence[index][0] and self.rule[i][1]>0:
                    break #Required rule token/tag missing in the sentence
                if self.rule[i][0] != sentence[index][0] and self.rule[i][1]==0:
                    if i==len(self.rule)-1: #Missing optional tags can be skipped
                        matches.append((r_index,index))
                    pass
                else:
                    index+=1 #Rule tag found in sentence, proceed in rule and sentence
                    if i==len(self.rule)-1:
                        matches.append((r_index,index))
        return matches
            

           
        #PPO = NPs representing people, places and organizations
rules = [Rule([('PPO',1),(',',0),('IN',0),('CC',0),('NP',1),('JJ',0),('IN',0),(',',0),('CC',0),\
               ('NP',1),('CC',0),('IN',0),(',',0),('PPO',1)]),\
         Rule([('PPO',1),('IN',0),(',',0),('CC',0),('NP',1),('IN',0),(',',0),('CC',0),('NP',1),\
               ('IN',0),('NP',1),('CC',0),(',',0),('IN',0),('NP',1)]),\
         Rule([('PPO',1),(',',0),('IN',0),('CC',0),('PPO',1),(',',0),('IN',0),('CC',0),('PPO',1),\
               (',',0),('IN',0),('CC',0),('PPO',1)]),\
         Rule([('PPO',1),('IN',0),(',',0),('CC',0),('NP',1),('IN',0),(',',0),('CC',0),('NP',1),\
               ('IN',0),(',',0),('CC',0),('NP',1)]),\
         Rule([('PPO',1),('IN',0),(',',0),('CC',0),('PPO',1),('IN',0),(',',0),('CC',0),('NP',1),\
               ('IN',0),(',',0),('CC',0),('NP',1)]),\
         Rule([('PPO',1),('IN',0),(',',0),('CC',0),('PPO',1),('IN',0),(',',0),('CC',0),('NP',1)]),\
         Rule([('PPO',1),('IN',0),(',',0),('CC',0),('NP',1),('IN',0),(',',0),('CC',0),('NP',1)]),\
         Rule([('PPO',1),(',',0),('IN',0),('NP',1),('JJ',0),('IN',0),(',',0),('CC',0),('PPO',1),\
               ('CC',0),('IN',0),(',',0),('PPO',1)]),\
         Rule([('PPO',1),(',',0),('IN',0),('NP',1),('JJ',0),('IN',0),(',',0),('CC',0),('NP',1),\
               ('CC',0),('IN',0),(',',0),('NP',1)]),\
         Rule([('PPO',1),(',',0),('IN',0),(',',0),('CC',0),('PPO',1),('IN',0),(',',0),('CC',0),\
               ('PPO',1)]),\
         Rule([('PPO',1),(',',0),('IN',0),('CC',0),('PPO',1),(',',0),('IN',0),('CC',0),('PPO',1),\
               (',',0),('IN',0),('CC',0),('PPO',1)]),\
         Rule([('NP',1),(',',0),('IN',0),('CC',0),('PPO',1),(',',0),('IN',0),('CC',0),('PPO',1)]),\
         Rule([('PPO',1),(',',0),('IN',0),('CC',0),('NP',1),(',',0),('IN',0),('CC',0),('PPO',1)]),\
         Rule([('PPO',1),(',',0),('IN',0),('CC',0),('NP',1),('JJ',1)]),\
         Rule([('NP',1),(',',0),('IN',0),('CC',0),('PPO',1)]),\
         Rule([('PPO',1),(',',0),('IN',0),('CC',0),('NP',1)]),\
         Rule([('PPO',1),(',',0),('IN',0),('CC',0),('PPO',1)]),\
         #Rule([('NP',1),(',',0),('IN',0),('CC',0),('NP',1)]),\
         Rule([('PPO',1)])]
