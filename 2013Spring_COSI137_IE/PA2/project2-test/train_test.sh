#!/bin/sh
#crf_learn -c 1.5 base+feature1+2_nl.tpl train_feature1+2_nl.gold base+feature1+2_nl.model
crf_test -m base+feature1+2_nl.model test_feature1+2_nl.raw > test_feature1+2_nl.result
python ../evaluate-head.py test.gold test_feature1+2_nl.result 