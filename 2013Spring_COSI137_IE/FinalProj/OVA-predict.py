import numpy

bf_cls_f = open("before_pf_cls.result",'r')
sm_cls_f = open("simul_pf_cls.result",'r')
md_cls_f = open("modal_pf_cls.result",'r')
ed_cls_f = open("evidential_pf_cls.result",'r')
labels = ["BEFORE","SIMUL","MODAL","EVIDENTIAL"]
predictions = []
#wf = open("test_prediction",'w')
#for the imbalanced data distribution, assign weights for the label with fewer instances
bias_weights = 0.1

for bf,sm,md,ed in zip(bf_cls_f,sm_cls_f,md_cls_f,ed_cls_f):
    score = numpy.array([bias_weights*eval(bf),bias_weights*eval(sm),eval(md),eval(ed)])
    label_index = numpy.argmax(score)
    label = labels[label_index]
    #    wf.write(label+"\n")
    predictions.append(label)
#wf.close()

gold_cls = open("event_tk_feature.test",'r')
cor_array = numpy.zeros(4)
gold_array = numpy.zeros(4)
pred_array = numpy.zeros(4)
scores = []

for p,g in zip(predictions,gold_cls.readlines()):
    g = g.strip()
    if p == g:
        cor_array[labels.index(p)]+=1.
        gold_array[labels.index(p)]+=1.
        pred_array[labels.index(p)]+=1.
    else:
        gold_array[labels.index(g)]+=1.
        pred_array[labels.index(p)]+=1.

for i in range(len(labels)):
    precision = cor_array[i]/pred_array[i]
    recall = cor_array[i]/gold_array[i]
    f1 = 2*precision*recall/(precision+recall)
#    scores.append((precision,recall,f1))
    print "Class:%s precision:%s recall:%s f1:%s\n"%(labels[i],precision,recall,f1)

