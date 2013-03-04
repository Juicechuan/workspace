from divide_sent import get_sent,pivot_sentence
from nltk.corpus import switchboard
import random

given_sen = ""
given_sen_list = []
new_sen_list = []
for discourse in switchboard.tagged_discourses():
    for turn in discourse:
        sent_list = get_sent(turn)
        for sent in sent_list:
            result = pivot_sentence(sent)
            if result[0] != []:
                given_sen = '<s>'+''.join(i[0]+" " for i in result[0])+'</s>'
            if result[2] != []:
                new_sen = '<s>' + result[1] + ' '.join(j[0] for j in result[2])

            given_sen_list.append(given_sen)
            new_sen_list.append(new_sen)


given_file_test = open("given_sentences.test",'w')
given_file_train =  open("given_sentences.train",'w')
new_file_test = open("new_sentences.test",'w')
new_file_train = open("new_sentences.train",'w')

for k in range(0,len(given_sen_list)/4):
    test_index = random.randint(0,3)
    for i in range(0,4):
        if k*4+i<len(given_sen_list):
            if i == test_index:
                given_file_test.write(new_sen_list[k*4+i])
            else:
                given_file_train.write(new_sen_list[k*4+i])

