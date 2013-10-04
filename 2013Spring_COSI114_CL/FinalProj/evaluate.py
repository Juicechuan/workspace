#!/usr/bin/python
#compute the accuracy of an NE tagger

#usage: evaluate-head.py [gold_file][output_file]

import sys, re
import nltk.metrics
import nltk
import collections

if len(sys.argv) != 3:
    sys.exit("usage: evaluate-head.py [gold_file][output_file]")

#gold standard file
goldfh = open(sys.argv[1], 'r')
#system output
testfh = open(sys.argv[2], 'r')

gold_tag_list = []
#gold_word_list = []
test_tag_list = []

emptyline_pattern = re.compile(r'^\s*$')

gold_tags_for_line = []
#gold_words_for_line = []
test_tags_for_line = []

for gline in goldfh.readlines():
    if emptyline_pattern.match(gline):
        if len(gold_tags_for_line) > 0:
            gold_tag_list.append(gold_tags_for_line)
        gold_tags_for_line = []
        #gold_word_list.append(gold_words_for_line)
        #gold_words_for_line = []
    else:
        parts = gline.split()
        #print parts
        gold_tags_for_line.append(parts[-1])
        #gold_words_for_line.append(parts[0])

for tline in testfh.readlines():
    if  emptyline_pattern.match(tline):
        if len(test_tags_for_line) > 0:
            test_tag_list.append(test_tags_for_line)
        test_tags_for_line = []
    else:
        parts = tline.split()
        #print parts
        test_tags_for_line.append(parts[-1])

#dealing with the last line
if len(gold_tags_for_line) > 0:
    gold_tag_list.append(gold_tags_for_line)

if len(test_tags_for_line) > 0:
    test_tag_list.append(test_tags_for_line)


B_test_total = 0
B_gold_total = 0
B_correct = 0

refsets = collections.defaultdict(set)
testsets = collections.defaultdict(set)

#print gold_tag_list
#print test_tag_list

for i in range(len(gold_tag_list)):
    #print gold_tag_list[i]
    #print test_tag_list[i]
    for j in range(len(gold_tag_list[i])):
        refsets[gold_tag_list[i][j]].add(len(gold_tag_list)*i+j)
        testsets[test_tag_list[i][j]].add(len(gold_tag_list)*i+j)
            
print 'B-SNP precision:',nltk.metrics.precision(refsets['B-SNP'], testsets['B-SNP'])
print 'B-SNP recall:', nltk.metrics.recall(refsets['B-SNP'], testsets['B-SNP'])
print 'B-SNP F-measure:', nltk.metrics.f_measure(refsets['B-SNP'], testsets['B-SNP'])
print 'I-SNP precision:', nltk.metrics.precision(refsets['I-SNP'], testsets['I-SNP'])
print 'I-SNP recall:', nltk.metrics.recall(refsets['I-SNP'], testsets['I-SNP'])
print 'I-SNP F-measure:', nltk.metrics.f_measure(refsets['I-SNP'], testsets['I-SNP'])
print 'O precision:', nltk.metrics.precision(refsets['O'], testsets['O'])
print 'O recall:', nltk.metrics.recall(refsets['O'], testsets['O'])
print 'O F-measure:', nltk.metrics.f_measure(refsets['O'], testsets['O'])
            
    
