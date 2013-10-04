
def get_CPHB(pair,parsed_sentences):
    m1_index = pair.first.offsets[0]
    m2_index = pair.second.offsets[0]
    senID = pair.first.sentenceID
    
    tree = parsed_sentences[senID]
    if m2_index+1 < len(tree):
        dominate_path = tree.treeposition_spanning_leaves(m1_index,m2_index+1)
    else:
        dominate_path = tree.treeposition_spanning_leaves(m1_index,m2_index)
    subtree = copy.deepcopy(tree)
    for i in list(dominate_path):
        temp = subtree[i]
        if isinstance(temp,str):
            break
        subtree = temp
    #filter out the lowest NP tree
    def filter(stree):
        return stree.node == "NP" and "NP" not in [child.node for child in stree]
    
    chunk_pheads_between = []
    for t in subtree.subtrees(filter):
        NPchunk = t.pos()
        head_phrase = ""
        #get the first Noun in NP chunk as head
        for token in NPchunk:
            if re.match("N.*",token[1]):
                head_phrase = token[0]
                chunk_pheads_between.append(head_phrase)
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

def get_CPHBM1(pair,parsed_sentences):

    m1_index = pair.first.offsets[0]
    m2_index = pair.second.offsets[0]
    senID = pair.first.sentenceID
    
    tree = parsed_sentences[senID]
    dominate_path = tree.treeposition_spanning_leaves(0,m1_index)
    subtree = copy.deepcopy(tree)
    for i in list(dominate_path):
        temp = subtree[i]
        if isinstance(temp,str):
            break
        subtree = temp
    #filter out the lowest NP tree
    def filter(stree):
        return stree.node == "NP" and "NP" not in [child.node for child in stree]
    
    chunk_pheads_before = []

    for t in subtree.subtrees(filter):
        NPchunk = t.pos()
        head_phrase = ""
        #get the first Noun in NP chunk as head
        for token in NPchunk:
            if re.match("N.*",token[1]):
                head_phrase = token[0]
                chunk_pheads_before.append(head_phrase)
                break
    if len(chunk_pheads_before)>1:
        return (chunk_pheads_before[-1],chunk_pheads_before[-2])
    elif len(chunk_pheads_before) == 1:
        return (chunk_pheads_before[-1],"NA")
    elif len(chunk_pheads_before) == 0:
        return ("NA","NA")

def get_CPHAM2(pair,parsed_sentences):

    m1_index = pair.first.offsets[0]
    m2_index = pair.second.offsets[0]
    senID = pair.first.sentenceID
    
    tree = parsed_sentences[senID]
    if m2_index+1 < len(tree.leaves()):
        dominate_path = tree.treeposition_spanning_leaves(m2_index+1,len(tree.leaves()))
    else:
        return ("NA","NA")
    subtree = copy.deepcopy(tree)
    for i in list(dominate_path):
        temp = subtree[i]
        if isinstance(temp,str):
            break
        subtree = temp
    #filter out the lowest NP tree
    def filter(stree):
        return stree.node == "NP" and "NP" not in [child.node for child in stree]
    
    chunk_pheads_after = []
    for t in subtree.subtrees(filter):
        NPchunk = t.pos()
        head_phrase = ""
        #get the first Noun in NP chunk as head
        for token in NPchunk:
            if re.match("N.*",token[1]):
                head_phrase = token[0]
                chunk_pheads_after.append(head_phrase)
                break
    if len(chunk_pheads_after)>1:
        return (chunk_pheads_after[0],chunk_pheads_after[1])
    elif len(chunk_pheads_after) == 1:
        return (chunk_pheads_after[0],"NA")
    elif len(chunk_pheads_after) == 0:
        return ("NA","NA")
