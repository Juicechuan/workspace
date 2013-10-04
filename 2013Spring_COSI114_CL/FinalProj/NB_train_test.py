from superchunk_reader import *
import nltk
import collections
import nltk.metrics

superchunks_train = SuperchunkCorpusReader(root="./data", fileids=r"train.snp")
superchunks_test = SuperchunkCorpusReader(root="./data", fileids=r"test.snp")


def load_sent(superchunks):
    sent_list = []
    for t in superchunks.chunked_sents():
        sent = []
        for x in tree2iob(t):
            if x[1] == ".":
                sent_list.append(sent)
                sent = []
            else:
                sent.append(x)
    return sent_list

def get_features(sent_list,train_or_test=True):
    featuresets = []
    if train_or_test:
        wf = open("features.train",'w')
    else:
        wf = open("features.test",'w')
        wf1 = open("features.raw",'w')

    for sent in sent_list:
        for i,w in enumerate(sent):
            features = {}
            word = w[0]
            pos_tag = w[1]
            chunk_tag = w[2]
            snp_tag = w[3]

            features["FirstWord"] =  (i==0)
            wf.write("%s %s %s %s %s\n"%(word,pos_tag,chunk_tag,features["FirstWord"],snp_tag))
            if not train_or_test:
                wf1.write("%s %s %s %s\n"%(word,pos_tag,chunk_tag,features["FirstWord"]))
            features["word"] = word
            features["pos_tag"] = pos_tag
            features["chunk_tag"] = chunk_tag
            
            
            if i > 1:
                features["pre2_word"] = sent[i-2][0]
            else:
                features["pre2_word"] = "NA"
            
            if i > 0:
                features["pre_word"] = sent[i-1][0]
            else:
                features["pre_word"] = "NA"
                    
            if i < len(sent) - 1:
                features["next_word"] = sent[i+1][0]
            else:
                features["next_word"] = "NA"

            if i < len(sent) - 2:
                features["next2_word"] = sent[i+2][0]
            else:
                features["next2_word"] = "NA"

            if i > 1:
                features["pre2_pos_tag"] = sent[i-2][1]
            else:
                features["pre2_pos_tag"] = "NA"

            if i > 0:
                features["pre_pos_tag"] = sent[i-1][1]
            else:
                features["pre_pos_tag"] = "NA"

            if i < len(sent) - 1:
                features["next_pos_tag"] = sent[i+1][1]
            else:
                features["next_pos_tag"] = "NA"

            if i < len(sent) - 2:
                features["next2_pos_tag"] = sent[i+2][1]
            else:
                features["next2_pos_tag"] = "NA"

            if i > 1:
                features["pre2_chunk_tag"] = sent[i-2][2]
            else:
                features["pre2_chunk_tag"] = "NA"

            if i > 0:
                features["pre_chunk_tag"] = sent[i-1][2]
            else:
                features["pre_chunk_tag"] = "NA"

            if i < len(sent) - 1:
                features["next_chunk_tag"] = sent[i+1][2]
            else:
                features["next_chunk_tag"] = "NA"

            if i < len(sent) - 2:
                features["next2_chunk_tag"] = sent[i+2][2]
            else:
                features["next2_chunk_tag"] = "NA"

            featuresets.append((features,snp_tag))
    wf.close()
    if not train_or_test:
        wf1.close()
    return featuresets


sent_list_train = load_sent(superchunks_train)
sent_list_test = load_sent(superchunks_test)

featuresets_train = get_features(sent_list_train,True)
featuresets_test = get_features(sent_list_test,False)

print 'Naive Bayes superchunker-----------------\n'

print 'train the Naive Bayes classifier...\n'
classifier = nltk.NaiveBayesClassifier.train(featuresets_train)
print 'The overall accuracy is:%s\n'%(nltk.classify.accuracy(classifier,featuresets_test))

refsets = collections.defaultdict(set)
testsets = collections.defaultdict(set)

for i, (feature, label) in enumerate(featuresets_test):
    refsets[label].add(i)
    observed = classifier.classify(feature)
    testsets[observed].add(i)

print 'B-SNP precision:',nltk.metrics.precision(refsets['B-SNP'], testsets['B-SNP'])
print 'B-SNP recall:', nltk.metrics.recall(refsets['B-SNP'], testsets['B-SNP'])
print 'B-SNP F-measure:', nltk.metrics.f_measure(refsets['B-SNP'], testsets['B-SNP'])
print 'I-SNP precision:', nltk.metrics.precision(refsets['I-SNP'], testsets['I-SNP'])
print 'I-SNP recall:', nltk.metrics.recall(refsets['I-SNP'], testsets['I-SNP'])
print 'I-SNP F-measure:', nltk.metrics.f_measure(refsets['I-SNP'], testsets['I-SNP'])
print 'O precision:', nltk.metrics.precision(refsets['O'], testsets['O'])
print 'O recall:', nltk.metrics.recall(refsets['O'], testsets['O'])
print 'O F-measure:', nltk.metrics.f_measure(refsets['O'], testsets['O'])

