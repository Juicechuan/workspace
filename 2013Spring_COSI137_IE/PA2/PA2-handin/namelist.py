
import re
import sys

def extract_FWL(train_gold_file):
    """Extract the FWL(Frequent Word List) from the gold training file"""
    raw_data = open(train_gold_file,'r')
    
    FWL_list = set()
    word_list = set()
    doc_dict = {}
    for rline in raw_data.readlines():
        if rline.strip():
            lex = rline.split()[1]
            if re.match('\w{3}\d{8}.\d{4}.\d{4}',lex):
                word_list.add(lex)
                doc_dict.update([(word,doc_dict[word]+1) if word in doc_dict.keys() else (word,1) for word in word_list])
                word_list = set()
            else:
                word_list.add(lex)
                
    for i,k in doc_dict.items():
        if k > 5:
            FWL_list.add(i)

    return FWL_list
    


