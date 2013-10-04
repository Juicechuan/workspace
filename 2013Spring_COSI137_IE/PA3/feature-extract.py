#!usr/bin/python

"""Extract the feature from the trainning file"""
import sys
import string
from nltk import metrics,stem,tokenize,tree
from util import Document,Pair,Entity
import copy

def extract_contextual(postagged_file):
    """extract the contextual information as lists"""
    raw_data = open(postagged_file,'r')
    sentence_list = []

    for rline in raw_data.readlines():
        if rline.strip():
            tagged_tokens = rline.split()
            sentence = [tuple(w.split("_")) for w in tagged_tokens]
            sentence_list.append(sentence)

    raw_data.close()
    return sentence_list

def extract_syntax(parsed_file):
    """get the parsed tree"""
    parsed_data = open(parsed_file,'r')
    tree_list = []

    for l in parsed_data.readlines():
        if l.strip():
            parsed_sentence = tree.Tree.parse(l.strip())
            tree_list.append(parsed_sentence)

    parsed_data.close()
    return tree_list

def load_data(input_file):
    
    raw_data = open(input_file,'r')

    doc_list = []
    doc = Document()
    for rline in raw_data.readlines():
        if rline.strip():
            entry = rline.split()
            docID = entry[0]
            if docID != doc.docID:
                #import pdb
                #if doc.docID!='':
                #    pdb.set_trace()
                doc_list.append(doc)
                doc = Document(docID)
                first = Entity(entry[1],(entry[2],entry[3]),entry[4],entry[5])
                second = Entity(entry[6],(entry[7],entry[8]),entry[9],entry[10])
                pair = Pair(first,second)
                if len(entry) == 12:
                    pair.set_label(entry[11])
                doc.add_pair(pair)
            else:
                first = Entity(entry[1],(entry[2],entry[3]),entry[4],entry[5])
                second = Entity(entry[6],(entry[7],entry[8]),entry[9],entry[10])
                pair = Pair(first,second)
                if len(entry) == 12:
                    pair.set_label(entry[11])
                doc.add_pair(pair)
                
    doc_list.append(doc)
    return doc_list
                
def output_features(output_file,feature_list):
    output_data = open(output_file,'w')
    
    for w in feature_list:
        label = w[0]
        if label != '':
            output_data.write(label)
        feature_vector = w[1]
        for key,value in feature_vector.items():
            output_data.write((" %s=%s")%(key,value))
        output_data.write("\n")
    
    output_data.close()

def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    doc_list = load_data(input_file)
    feature_list = []
    for doc in doc_list[1:]:
        postagged_file = "data/postagged-files/"+doc.docID+".raw.pos"
        parsed_file = "data/postagged-files/"+doc.docID+".raw.sen.parsed"
        pos_tagged_sentences = extract_contextual(postagged_file)
        parsed_sentences = extract_syntax(parsed_file)
        print doc.docID+"\n"
        for pair in doc.pair_list:
            feature_dict = {}
            feature_dict["distance"] = distance_feature(pair)
            feature_dict["i-pronoun"] = pronoun_feature(pair.first,pos_tagged_sentences)
            feature_dict["j-pronoun"] = pronoun_feature(pair.second,pos_tagged_sentences)
            feature_dict["string-match"] = string_match(pair,pos_tagged_sentences)
            feature_dict["pro_str"] = pro_str(pair,pos_tagged_sentences)
            feature_dict["pn_str"] =  pn_str(pair,pos_tagged_sentences)
            feature_dict["DEF-NP"] = definite_NP(pair.second,pos_tagged_sentences)
            feature_dict["DEM-NP"] = demonstrative_NP(pair.second,pos_tagged_sentences)
            feature_dict["NUM"] = number_agree(pair,pos_tagged_sentences)
            feature_dict["semclass"] = semclass(pair)
            feature_dict["proper_name"] = proper_name(pair,pos_tagged_sentences)
            feature_dict["alias"] =  alias(pair,pos_tagged_sentences)
            feature_dict["tree-distance"] = tree_distance(pair,parsed_sentences)
            feature_dict["both_pronoun"] = both_pronoun(pair,pos_tagged_sentences)
            feature_dict["GPE-match"] = GPE_match(pair)
            #feature_dict["np_prp"] = np_prp(pair,pos_tagged_sentences)
            #feature_dict["i-preDT"] = previous_DT(pair.first,pos_tagged_sentences)
            #feature_dict["j-preDT"] = previous_DT(pair.second,pos_tagged_sentences)
#            feature_dict["i-depth"] = depth(pair.first,parsed_sentences)
#            feature_dict["i-subject"] = fuzzy_subject(pair.first,pos_tagged_sentences)
            feature_dict["j-depth"] = depth(pair.second,parsed_sentences)
            feature_dict["appositive"] = appositive(pair,parsed_sentences)
            feature_dict["span_np"] = span_np(pair,parsed_sentences)
#            feature_dict["gender"] = gender(pair,pos_tagged_sentences)

            feature_list.append((pair.label,feature_dict))

    output_features(output_file,feature_list)


pronouns = ["PRP","PRP$","WP","WP$"]
propernouns = ["NNP","NNPS"]
nouns = ["NN","NNS","NNP","NNPS","NP"]
stemmer = stem.lancaster.LancasterStemmer()
def distance_feature(pair):
    return abs(eval(pair.first.sentenceID)-eval(pair.second.sentenceID))

def get_POS(entity,pos_tagged_sentences):
    sentenceID = eval(entity.sentenceID)
    sentence = pos_tagged_sentences[sentenceID]
    #print sentence
    #print entity.str
    #print entity.type
    #print eval(entity.offsets[0])
    pos = sentence[eval(entity.offsets[0])][1]
    return pos

def get_previous_POS(entity,pos_tagged_sentences):
    sentenceID = eval(entity.sentenceID)
    sentence = pos_tagged_sentences[sentenceID]
    if eval(entity.offsets[0]) > 1:
        pos_1 = sentence[eval(entity.offsets[0])-1][1]
        pos_2 = sentence[eval(entity.offsets[0])-2][1]
        return [pos_2,pos_1]
    elif eval(entity.offsets[0]) == 1:
        return [sentence[eval(entity.offsets[0])-1][1]]
    else:
        return ["None"]
    
def pronoun_feature(entity,pos_tagged_sentences):
    pos = get_POS(entity,pos_tagged_sentences)
    return pos in pronouns 

def both_pronoun(pair,pos_tagged_sentences):
    return pronoun_feature(pair.first,pos_tagged_sentences) and pronoun_feature(pair.second,pos_tagged_sentences)

def normalize1(str):
    words = str.lower().strip().split("_")
    return ' '.join([stemmer.stem(w) for w in words])

def normalize(s):
    for p in string.punctuation:
        s = s.replace(p, '')
        
    return s.lower().strip()
    
def string_match(pair,pos_tagged_sentences):
    str1 = pair.first.str
    str2 = pair.second.str
    
    #1.stem
    #2.edit distance
    #return metrics.edit_distance(normalize(str1),normalize(str2)) <= max_dist
    return normalize(str1)==normalize(str2)

def GPE_match(pair):
    str1 = pair.first.str
    str2 = pair.second.str

    if pair.first.type == "GPE" and pair.second.type == "GPE":
        return stemmer.stem(normalize(str1)) == stemmer.stem(normalize(str2))
    else:
        return "unknown"

def pro_str(pair,pos_tagged_sentences):
    str1 = pair.first.str
    str2 = pair.second.str
    
    pos1 = get_POS(pair.first,pos_tagged_sentences)
    pos2 = get_POS(pair.second,pos_tagged_sentences)

    if pos1 in pronouns or pos2 in pronouns:
        return normalize(str1)==normalize(str2)
    else:
        return "NA"

def pn_str(pair,pos_tagged_sentences):
    str1 = pair.first.str
    str2 = pair.second.str
    
    pos1 = get_POS(pair.first,pos_tagged_sentences)
    pos2 = get_POS(pair.second,pos_tagged_sentences)

    if pos1 in propernouns or pos2 in propernouns:
        return normalize(str1)==normalize(str2)
    else:
        return "NA"
    
def definite_NP(entity,pos_tagged_sentences):
    sentenceID = eval(entity.sentenceID)
    sentence = pos_tagged_sentences[sentenceID]
    current = eval(entity.offsets[0])
    if current > 1:
        return sentence[(current-1)][0] == "the" or sentence[(current-2)][0].lower() == "the"
    elif current == 1:
        return sentence[(current-1)][0].lower() == "the"
    else:
        return False

def previous_DT(entity,pos_tagged_sentences):
    previous_POS = get_previous_POS(entity,pos_tagged_sentences)
    if "DT" in previous_POS:
        return True
    else:
        return False
    
def demonstrative_NP(entity,pos_tagged_sentences):

    demonstratives = ["this", "that", "these", "those"]
    sentenceID = eval(entity.sentenceID)
    sentence = pos_tagged_sentences[sentenceID]
    current = eval(entity.offsets[0])
    
    if current > 1:
        return sentence[(current-1)][0] in demonstratives or sentence[(current-2)][0].lower() in demonstratives
    elif current == 1:
        return sentence[(current-1)][0].lower() in demonstratives
    else:
        return False

def get_num(str,pos):
    if pos in ["NN","NNP"]:
        return "S"
    elif pos in ["NNS","NNPS"]:
        return "P"
    elif pos in ["PRP","PRP$"]:
        if normalize(str) in ["he","his","she","her","it","its"]:
            return "S"
        elif normalize(str) in ["they","their"]:
            return "P"
    else:
        return "NA"


def number_agree(pair,pos_tagged_sentences):

    str1 = pair.first.str
    str2 = pair.second.str
    
    pos1 = get_POS(pair.first,pos_tagged_sentences)
    pos2 = get_POS(pair.second,pos_tagged_sentences)

    type1 = get_num(str1,pos1)
    type2 = get_num(str2,pos2)
    
    if type1 == "NA" or type2 == "NA":
        return True
    
    return type1 == type2

def semclass(pair):
    if pair.first.type == "PER" and pair.second.type == "PER":
        return True
    elif (pair.first.type != "PER" or pair.second.type !="PER") and pair.first.type!= pair.second.type:
        return False
    else:
        return "Unknown"
#    if pair.first.type == pair.second.type:
#        return pair.first.type
#    else:
#        return "NA"

def proper_name(pair,pos_tagged_sentences):
    pos1 = get_POS(pair.first,pos_tagged_sentences)
    pos2 = get_POS(pair.second,pos_tagged_sentences)
    if pos1 in propernouns and pos2 in propernouns:
        return True
    else:
        return False

def alias(pair,pos_tagged_sentences):
    str1 = pair.first.str
    str2 = pair.second.str

    type1 = pair.first.type
    type2 = pair.second.type
    
    pos1 = get_POS(pair.first,pos_tagged_sentences)
    pos2 = get_POS(pair.second,pos_tagged_sentences)

    if type1 == type2:
        if type1 in ["PER","GPE"] and pos1 not in ["PRP,PRP$,WP,WP$"] and pos2 not in ["PRP,PRP$,WP,WP$"]:
            if str1 in str2.split("_") or str2 in str1.split("_"):
                return True
            else:
                return False
        else:
            return "unknown"
    else:
        return False

def tree_distance(pair,parsed_sentences):
    
    #within the same tree
    if pair.first.sentenceID == pair.second.sentenceID:
        index1 = eval(pair.first.offsets[0])
        index2 = eval(pair.second.offsets[0])
        #print index1,index2
        #print pair.first.str,pair.second.str
        tree = parsed_sentences[eval(pair.first.sentenceID)]
        
        #print tree1,tree2
        path1 = list(tree.leaf_treeposition(index1))
        path2 = list(tree.leaf_treeposition(index2))

        n = 0
        for i,j in zip(path1,path2):
            if i == j:
                n+=1
            else:
                break

        tree_distance = len(path1)+len(path2)-2*n
        return tree_distance
    else:
        return "unknown"

def depth(entity,parsed_sentences):
    
    index = eval(entity.offsets[0])
    
    #print index1,index2
    #print pair.first.str,pair.second.str
    tree = parsed_sentences[eval(entity.sentenceID)]

    #print tree1,tree2
    path = list(tree.leaf_treeposition(index))
    return len(path)

def appositive(pair,parsed_sentences):
    
    if pair.first.sentenceID == pair.second.sentenceID:
        index1 = eval(pair.first.offsets[0])
        index2 = eval(pair.second.offsets[0])
        #print index1,index2
        #print pair.first.str,pair.second.str
        tree = parsed_sentences[eval(pair.first.sentenceID)]

        #print tree1,tree2
        path1 = list(tree.leaf_treeposition(index1))
        path2 = list(tree.leaf_treeposition(index2))
        if index1 < index2:
            dominate_path = tree.treeposition_spanning_leaves(index1,index2+1)
        else:
            dominate_path = tree.treeposition_spanning_leaves(index2,index1+1)
        dept = len(dominate_path)
        subtree = copy.deepcopy(tree)
        #print index1,index2
        #print dominate_path
        for i in list(dominate_path):
            temp = subtree[i]
            subtree = temp
        #print subtree
        if subtree.node == 'NP':
            if subtree[path1[dept]].node == 'NP' and subtree[path2[dept]].node == 'NP':
                if path1[dept] == (path2[dept] - 2) and subtree[path1[dept]+1].node == ',':
                    return True
                if path1[dept] == (path2[dept] + 2) and subtree[path1[dept]-1].node == ',':
                    return True
    
    return False

def get_gender(str):
    if str in ["he","his"]:
        return "M"
    elif str in ["she","her"]:
        return "F"
    else:
        return "X"

def gender(pair,pos_tagged_sentences):
    pos1 = get_POS(pair.first,pos_tagged_sentences)
    pos2 = get_POS(pair.second,pos_tagged_sentences)

    str1 = normalize(pair.first.str)
    str2 = normalize(pair.second.str)
    
    if pos1 in pronouns and pos2 in pronouns:
        g1 = get_gender(str1)
        g2 = get_gender(str2)

        if g1 == "X" or g2 == "X":
            return "unknown"
        else:
            return g1 == g2
    else:
        return "unknown"

def span_np(pair,parsed_sentences):
    
    if pair.first.sentenceID == pair.second.sentenceID and pair.first.type in nouns and pair.second.type in nouns:
        index1 = eval(pair.first.offsets[0])
        index2 = eval(pair.second.offsets[0])
        #print index1,index2
        #print pair.first.str,pair.second.str
        tree = parsed_sentences[eval(pair.first.sentenceID)]

        #print tree1,tree2

        if index1 < index2:
            dominate_path = tree.treeposition_spanning_leaves(index1,index2+1)
        else:
            dominate_path = tree.treeposition_spanning_leaves(index2,index1+1)

        subtree = copy.deepcopy(tree)
        for i in list(dominate_path):
            temp = subtree[i]
            subtree = temp

        return subtree.node

    return "unknown"


    
if __name__ == "__main__":
    main()
