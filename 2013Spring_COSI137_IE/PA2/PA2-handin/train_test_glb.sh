#!/bin/sh
python feature_extract.py train.gold train_feature1+2_nl_glb.gold
python feature_extract.py test.raw test_feature1+2_nl_glb.raw

crf_learn -c 10 base+feature1+2_nl_glb.tpl train_feature1+2_nl_glb.gold base+feature1+2_nl_glb.model
crf_test -m base+feature1+2_nl_glb.model test_feature1+2_nl_glb.raw > test_feature1+2_nl_glb.result
python ../evaluate-head.py test.gold test_feature1+2_nl_glb.result