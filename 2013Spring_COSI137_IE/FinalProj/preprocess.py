import xml.etree.ElementTree as et
import sys
import nltk
import re
import copy

def parse_xmlfile(xmlfile):
    """parse tml file in the xml format 
       TODO:
       1)get the span of the event or time
       2)
    """
    tree = et.parse(xmlfile)
    root = tree.getroot()
    doc = []
    sent = []
    
    event_list = {}
    event_instance_list = {}
    time_list = {}
    rel_list = {}

    if root[0].tag == 'TIMEX3':  #actually not necessary
        attrib = root[0].attrib.copy()
        tid = attrib.pop('tid')
        time_list[tid] = attrib
        
    sent = nltk.word_tokenize(root[0].tail[root[0].tail.find("\n\n")+2:])
    if len(sent) >=2 and sent[-2] == "Inc" and sent[-1] == ".":
        sent = sent[:-1]
        sent[-1] = "Inc."
    elif len(sent) >=2 and sent[-2] == "Co" and sent[-1] == ".":
        sent = sent[:-1]
        sent[-1] = "Co."
    elif len(sent) >=2 and sent[-2] == "Corp" and sent[-1] == ".":
        sent = sent[:-1]
        sent[-1] = "Corp."
    for child in root[1:]:
        start = len(sent)
        sentNo = len(doc)
        if child.text != None: #the event or timex3 tag
            tag_text = nltk.word_tokenize(child.text)
            end = start + len(tag_text)
            sent += tag_text
            if child.tag == 'TIMEX3':
                attrib = child.attrib.copy()
                tid = attrib.pop('tid')
                attrib['span'] = (sentNo,start,end)
                time_list[tid] = attrib 
            elif child.tag == 'EVENT':
                attrib = child.attrib.copy()
                eid = attrib.pop('eid')
                attrib['span'] = (sentNo,start,end)
                event_list[eid] = attrib
            #handle the tail text
            untag_text = child.tail
#            import pdb
#            if untag_text.find("a lot of money on that")!=-1: pdb.set_trace()
#            if untag_text!=None and untag_text.find("\n\n") != -1:
#                ut = untag_text[:untag_text.find("\n\n")]
#                if ut.find(". \n") != -1:
#                    sent += nltk.word_tokenize(ut[:ut.find(". \n")])
#                    doc.append(sent)
#                
#                    sent = nltk.word_tokenize(ut[ut.find(". \n")+3:])
#                    doc.append(sent)
#                else:
#                    sent += nltk.word_tokenize(untag_text[:untag_text.find("\n\n")])
#                    doc.append(sent)
                #new sent
#                ut1 = untag_text[untag_text.find("\n\n")+2:]
#                if ut1.find(". \n") != -1:
#                    sent = nltk.word_tokenize(ut1[:ut1.find(". \n")])
#                    doc.append(sent)
#                
#                    sent = nltk.word_tokenize(ut1[ut1.find(". \n")+3:])
#                else:
#                    sent = nltk.word_tokenize(untag_text[untag_text.find("\n\n")+2:])
#            elif untag_text!=None and untag_text.find(". \n") != -1:
#                sent += nltk.word_tokenize(untag_text[:untag_text.find(". \n")])
#                doc.append(sent)
#                
#                ut = untag_text[untag_text.find(". \n")+3:]
#                while ut.find(". \n")!=-1:
#                    sent = nltk.word_tokenize(ut[:ut.find(". \n")])
#                    doc.append(sent)
#                    ut = ut[ut.find(". \n")+3:]
                    
#                sent = nltk.word_tokenize(ut)
#            elif untag_text!=None and untag_text.find(".\" \n") != -1:
#                sent += nltk.word_tokenize(untag_text[:untag_text.find(".\" \n")])
#                doc.append(sent)
#                
#                sent = nltk.word_tokenize(untag_text[untag_text.find(".\" \n")+4:])
#            elif untag_text!=None:
#                tail_words = nltk.word_tokenize(untag_text)
#                if len(tail_words) !=0 and tail_words[-1] == "anti-":
#                    sent += tail_words[:-1]
#                else:
#                    sent += tail_words
            if untag_text != None:
                if untag_text.find("\n") != -1:
                    sent += nltk.word_tokenize(untag_text[:untag_text.find("\n")].strip())
                    doc.append(sent)
                    ut = untag_text[untag_text.find("\n"):].lstrip()
                    while ut!=None and ut.find("\n") != -1:
                        sent = nltk.word_tokenize(ut[:ut.find("\n")].strip())
                        doc.append(sent)
                        ut = ut[ut.find("\n"):].lstrip()
                    if ut != None:
                        sent = nltk.word_tokenize(ut)
                else:
                    tail_words = nltk.word_tokenize(untag_text)
                    if len(tail_words) !=0 and tail_words[-1] == "anti-":
                        sent += tail_words[:-1]
                    else:
                        sent += tail_words
        else:  #the makeinstance, tlink or slink tag
            if child.tag == 'MAKEINSTANCE':
                attrib = child.attrib.copy()
                eiid = attrib.pop('eiid')
                event_instance_list[eiid] = attrib
            elif child.tag == 'TLINK' or child.tag == 'SLINK':
                attrib = child.attrib.copy()
                relType = attrib.pop('relType')
                key = '_'.join([v for v in attrib.values()])
                rel_list[key] = relType

                
    return (event_list,event_instance_list,rel_list,doc)

def get_trees(filename):
    """get the corresponding tree"""
    filepath =  "data/wsj_subset/treebank_wsj/"+filename
    f = open(filepath,'r')
    tree_list = []
    bracketed_sent = ""

    for l in f.readlines():
        if l.strip():
            if (l.strip()[:4] == "( (S" or l.strip()[:3] == "((S" )and bracketed_sent != "":
                tree = nltk.tree.Tree.parse(bracketed_sent)
                tree_list.append(tree)
                bracketed_sent =  l.strip()
            else:
                bracketed_sent += l.strip()
    tree = nltk.tree.Tree.parse(bracketed_sent)
    tree_list.append(tree)
    return tree_list

def get_eid(eiid,event_instance_list):
    """get the eventID given the eiid """
    return event_instance_list[eiid]["eventID"]

def leaf_tag_path(tree,index,sent,tag=True):
    """get the tags along the path the index-th position in the tree.
       using dfs
    """
    if index < 0: raise IndexError('index must be non-negative')

    stack = [(tree,())]
    while stack:
        value,tag_path = stack.pop()
        if not isinstance(value,nltk.tree.Tree):
            if index == 0: return tag_path
            else: 
               if value in sent: index -= 1
        else:
            for i in range(len(value)-1,-1,-1):
                if tag:
                    stack.append((value[i],tag_path+(value.node,)))
                else:
                    stack.append((value[i],tag_path+(i,)))
    return tag_path
    raise IndexError('index must be less than or equal to len(tree):')

def output_tr(tree):
    if not isinstance(tree,nltk.tree.Tree):
        return tree
    else:
        childstr = " ".join(output_tr(c) for c in tree)
        return '(%s %s)'%(tree.node,childstr)


interest_class = ["BEFORE","INCLUDES","AFTER","IS_INCLUDED","DURING","SIMULTANEOUS","IDENTITY","MODAL","EVIDENTIAL"]
def output_treeKernel_feature(instances,train):
    if train:
        wf = open("event_tk_feature.train",'w')
    else:
        wf = open("event_tk_feature.test",'w')
    n=0
    for fv in instances:
        if fv['relType'] in interest_class:
            if train:
                wf.write(("%s |BT| %s |ET|\n")%(fv["relType"],fv["tree_repr"]))
            else:
                if fv["relType"] in ["AFTER","BEFORE"]:
                    wf.write("BEFORE\n")
                elif fv["relType"] in ["IS_INCLUDED","INCLUDES", "DURING","SIMULTANEOUS","IDENTITY"]:
                    wf.write("SIMUL\n")
                elif fv["relType"] == "MODAL":
                    wf.write("MODAL\n")
                elif fv["relType"] == "EVIDENTIAL":
                    wf.write("EVIDENTIAL\n")
                else:
                    raise ValueError("Wrong Type!")
            n+=1
    wf.close()
    print "Number of Instances: "+str(n)


feature_types = []
def output_one_class(one_class,output_fn,instances):
    class_file = open(output_fn,'w')

    def get_pf_features(dic,event):
        pf_feature_vector = []
        for key,value in dic.items():
            if key not in ["eventID","eiid","eid","span"]:
                feature_name = '_'.join([event,key,value])
                if feature_name in feature_types:
                    pf_feature_vector.append(feature_types.index(feature_name))
                else:
                    feature_types.append(feature_name)
                    pf_feature_vector.append(feature_types.index(feature_name))
        return pf_feature_vector

    for fv in instances:
        if fv['relType'] in interest_class:
            if fv['relType'] in one_class:
                class_file.write("1 |BT| %s |ET| "%(fv["tree_repr"]))
            else:
                class_file.write("-1 |BT| %s |ET| "%(fv["tree_repr"]))
            
            pf_vector = get_pf_features(fv["event1"],"e1")
            pf_vector_2 = get_pf_features(fv["event2"],"e2")
        
            l = (pf_vector+pf_vector_2)[:]
            l.sort()
            for i in l:
                class_file.write("%s:1 "%(i+1))
            class_file.write("\n")
            
def output_ova_tkpf(instances):
    """tree kernel with perfect feature vector"""
    output_one_class(["AFTER","BEFORE"],"before_cls/bf_tkpf_feature.train",instances)
    output_one_class(["IS_INCLUDED","INCLUDES", "DURING","SIMULTANEOUS","IDENTITY"],"simul_cls/sm_tkpf_feature.train",instances)
    output_one_class(["MODAL"],"modal_cls/md_tkpf_feature.train",instances)
    output_one_class(["EVIDENTIAL"],"evidential_cls/ed_tkpf_feature.train",instances)

def output_one_vs_all(instances):
    """one vs all for classes BEFORE,SIMULTANEOUS,MODAL,EVIDENTIAL """
    bf_f = open("before_cls/bf_tk_feature.train",'w')
    for fv in instances:
        if fv['relType'] in interest_class:
            if fv['relType'] == "AFTER" or fv['relType'] == "BEFORE":
                bf_f.write("1 |BT| %s |ET|\n"%(fv["tree_repr"]))
            else:
                bf_f.write("-1 |BT| %s |ET|\n"%(fv["tree_repr"]))
    bf_f.close()

    sm_f = open("simul_cls/sm_tk_feature.train",'w')
    for fv in instances:
        if fv['relType'] in interest_class:
            if fv['relType'] in ["IS_INCLUDED","INCLUDES", "DURING","SIMULTANEOUS","IDENTITY"]:
                sm_f.write("1 |BT| %s |ET|\n"%(fv["tree_repr"]))
            else:
                sm_f.write("-1 |BT| %s |ET|\n"%(fv["tree_repr"]))
    sm_f.close()

    md_f = open("modal_cls/md_tk_feature.train",'w')
    for fv in instances:
        if fv['relType'] in interest_class:
            if fv['relType'] == "MODAL":
                md_f.write("1 |BT| %s |ET|\n"%(fv["tree_repr"]))
            else:
                md_f.write("-1 |BT| %s |ET|\n"%(fv["tree_repr"]))
    md_f.close()

    ed_f = open("evidential_cls/ed_tk_feature.train",'w')
    for fv in instances:
        if fv['relType'] in interest_class:
            if fv['relType'] == "EVIDENTIAL":
                ed_f.write("1 |BT| %s |ET|\n"%(fv["tree_repr"]))
            else:
                ed_f.write("-1 |BT| %s |ET|\n"%(fv["tree_repr"]))
    ed_f.close()

def output_statistics(instances):
    
    stat_dict = {}
    for ins in instances:
        if ins['relType'] in interest_class:
            if ins["relType"] in stat_dict.keys():
                stat_dict[ins["relType"]]+=1
            else:
                stat_dict[ins["relType"]]=1
    print "---------------------\n"
    for key,value in stat_dict.items():
        print "class:%s num:%s\n"%(key,value)
        
    print "---------------------\n"
#def main():
import commands
file_dir_train = "data/train/"
file_dir_test = "data/test/"
filelist_train = commands.getoutput("ls "+file_dir_train).split()
filelist_test = commands.getoutput("ls "+file_dir_test).split()

def get_instances(file_dir,filelist):

    instances = []
    for f in filelist:
        input_file = file_dir+f
        print input_file
    #    import pdb
    #    if f == "wsj_0610.tml": pdb.set_trace()
        tree_file = input_file[-12:-4]+".mrg"
        event_list,event_instance_list,rel_list,doc = parse_xmlfile(input_file)
        trees = get_trees(tree_file)
        #check the each relation and find out the verb-clause syntactic construction
        for id,rel in rel_list.items():

            fid = id.split("_")[1]
            sid = id.split("_")[2]

            if fid[:2] == "ei" and sid[:2] == "ei":  #only find out the event-event relation
                eid1 = get_eid(fid,event_instance_list)
                eid2 = get_eid(sid,event_instance_list)

                event1 = event_list[eid1]
                event2 = event_list[eid2]

                span1 = event1["span"]
                span2 = event2["span"]

                if span1[0] == span2[0]:  #make sure they are in the same sentence
                    #print doc[span1[0]]
                    sent = doc[span1[0]]
                    tr = trees[span1[0]]

                    index1 = span1[1]
                    index2 = span2[1]
                    #print index1,index2
                    tree_tag_path1 = list(leaf_tag_path(tr,index1,sent))
                    tree_path1 = list(leaf_tag_path(tr,index1,sent,tag=False))

                    tree_tag_path2 = list(leaf_tag_path(tr,index2,sent))
                    tree_path2 = list(leaf_tag_path(tr,index2,sent,tag=False))

                #share_tag_path = []
                    n = 0
                # Find the first index where they mismatch
                    subtr = copy.deepcopy(tr)
                    for i in range(len(tree_tag_path1)):
                        if i == len(tree_tag_path2) or tree_path1[i] != tree_path2[i]:
                            n=i
                            break
                        subtr = subtr[tree_path1[i]]

                    if index1 < index2:
                        tree_tag_path1.reverse()
                        path = tree_tag_path1[1:-n]+tree_tag_path2[n+1:-1]
                    else:
                        tree_tag_path2.reverse()
                        path = tree_tag_path2[1:-n]+tree_tag_path1[n+1:-1]
    #                print path
                    path_str = ''.join(path)
                #check whether it is a verb-clause structure
                    if re.match("(VP|NP|PP)+(SBAR)?S(VP|NP|PP)*",path_str) != None:
                        feature_vector = {}
                        feature_vector["tree_repr"] = output_tr(subtr)
                        feature_vector["event1"] = dict(event1.items()+event_instance_list[fid].items())
                        feature_vector["event2"] = dict(event2.items()+event_instance_list[sid].items())
                        feature_vector["relType"] = rel
                        instances.append(feature_vector)
    return instances
instances_train = get_instances(file_dir_train,filelist_train)
instances_test = get_instances(file_dir_test,filelist_test)
        
#Experiment 1

#output_treeKernel_feature(instances_train,True)
#output_treeKernel_feature(instances_test,False)
#output_statistics(instances_train)
#output_statistics(instances_test)
#output_one_vs_all(instances_train)

#Experiment 2 add "perfect" feature
output_ova_tkpf(instances_train)
output_one_class(interest_class,"event_tkpf_feature.test",instances_test)
#if __name__ == "__main__":
#    main()
