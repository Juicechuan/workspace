"""This file contains all the may or may not be useful feature functions."""
import re
from nltk import tree
import copy
import nltk

pronouns = ["PRP","PRP$","WP","WP$"]
propernouns = ["NNP","NNPS"]
nouns = ["NN","NNS","NNP","NNPS","NP"]


def get_WB(pair,pos_tagged_sentences):
    """check if there is no word between mentions"""
    pre_end = pair.first.offsets[1]
    next_start = pair.second.offsets[0]

    if pair.first.sentenceID == pair.second.sentenceID: #actually not necessary
        senID = pair.first.sentenceID
        if pre_end == next_start:
            return 0

        if abs(next_start - pre_end) == 1:
            return pos_tagged_sentences[senID][pre_end][0]

        fwb = pos_tagged_sentences[senID][pre_end][0]
        wbl = pos_tagged_sentences[senID][next_start-1][0]
        wbo = ''.join([item[0] for item in pos_tagged_sentences[senID][pre_end+1:next_start-1]])
        
        return tuple((fwb,wbo,wbl))

def get_BM1F(pair,pos_tagged_sentences):
    pre_start = pair.first.offsets[0]
    senID = pair.first.sentenceID
    if pre_start-1 >= 0:
        return pos_tagged_sentences[senID][pre_start-1][0]
    return "NA"

def get_BM1L(pair,pos_tagged_sentences):
    pre_start = pair.first.offsets[0]
    senID = pair.first.sentenceID
    if pre_start-2 >= 0:
        return pos_tagged_sentences[senID][pre_start-2][0]
    return "NA"

def get_AM2F(pair,pos_tagged_sentences):
    next_end = pair.second.offsets[1]
    senID = pair.second.sentenceID
    if next_end < len(pos_tagged_sentences[senID]):
        return pos_tagged_sentences[senID][next_end][0]
    return "NA"

def get_AM2L(pair,pos_tagged_sentences):
    next_end = pair.second.offsets[1]
    senID = pair.second.sentenceID
    if next_end+1 < len(pos_tagged_sentences[senID]):
        return pos_tagged_sentences[senID][next_end][0]
    return "NA"

def get_ET12(pair):
    return pair.first.type+"-"+pair.second.type

def getNumMB(pair,ne_dict,pos_tagged_sentences):
    m1 = pair.first.offsets[0]
    m2 = pair.second.offsets[0]
    senID = pair.first.sentenceID
    num = 0

    for i in range(m1+1,m2):
        if (senID,i) in ne_dict.values():
           num+=1
    return num

def getNumWB(pair,pos_tagged_sentences):
    return abs(pair.second.offsets[0]-pair.first.offsets[0])


def get_chunksent(tree):
    """derive the shallow chunk information from the full parsed tree"""
    def filter(stree):
        return stree.node == "NP" and "NP" not in [child.node for child in stree]
    NP_phrases = [t.pos() for t in tree.subtrees(filter)]
    chunk_sent = [(word,pos,"O") for (word,pos) in tree.pos()]
    for p,k in enumerate(tree.pos()):
        for np_phrase in NP_phrases:
            if k in np_phrase:
                if np_phrase.index(k) == 0:
                    chunk_sent[p] = (k[0],k[1],"B")
                else:
                    chunk_sent[p] = (k[0],k[1],"I")
    return chunk_sent
            
def get_CPHB(pair,chunk_sent):
    m1_index = pair.first.offsets[0]
    m2_index =  pair.second.offsets[0]
    #senID = pair.first.sentenceID

    #tree = parsed_sentences[senID]
    #chunk_sent = get_chunksent(tree)
    phrases = []
    
    for chunk in chunk_sent[m1_index+1:m2_index]:
        if chunk[2] == "O":
            if NP_phrase != []:
                phrases.append(NP_phrase)
            NP_phrase = []    
        else:
            NP_phrase.append((chunk[0],chunk[1]))
    chunk_pheads_between = []
    for phr in phrases:
        #find the first noun in NP 
        for tok in phr:
            if re.match("N.*",tok[1]):
                chunk_pheads_between.append(tok[0])
                break
            
    if len(chunk_pheads_between) == 0:
        return 0
    elif len(chunk_pheads_between) == 1:
        return chunk_pheads_between[0]
    else:
        cphbf = chunk_pheads_between[0]
        cphbl = chunk_pheads_between[len(chunk_pheads_between)-1]
        cphbo = ''.join(chunk_pheads_between[1:len(chunk_pheads_between)-1])

        return (cphbf,cphbo,cphbl)
            
def get_PTP(pair,parsed_sentences):

    m1_index = pair.first.offsets[0]
    m2_index = pair.second.offsets[0]
    senID = pair.first.sentenceID
    
    tree = parsed_sentences[senID]
    if m2_index >= len(tree.leaves()):
        m2_index -=1
    path1 = list(tree.leaf_treeposition(m1_index))
    path2 = list(tree.leaf_treeposition(m2_index))

    phrase_labels = []
    n = 0
    share_path = []
    for i,j in zip(path1,path2):
        if i == j:
            n+=1
            share_path.append(i)
        else:
            break
    sub_path1 = path1[n:]
    sub_path2 = path2[n:]
    def get_labels(stree,path):
        subtree = copy.deepcopy(stree)
        labels = [subtree.node]
        for i in path:
            if isinstance(subtree[i],nltk.tree.Tree):
                labels.append(subtree[i].node)
                temp = subtree[i]
                subtree = temp
        return tuple((subtree,labels))
    subtree = get_labels(tree,share_path)[0]
    path1_labels = get_labels(subtree,sub_path1)[1]
    path2_labels = get_labels(subtree,sub_path2)[1]
    path1_labels.reverse()
    path2_labels.reverse()
    if path1_labels[-1] == path2_labels[0]:
        return list(set(path1_labels[:]+path2_labels[1:]))
    else:
        ValueError("Path cannot connect:%s,%s" % (path1_labels,path2_labels ))





    
    
