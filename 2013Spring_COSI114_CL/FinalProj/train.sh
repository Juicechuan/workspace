#!/bin/sh

crf_learn -c 10 features.tpl features.train features.model
crf_test -m features.model features.raw > features.result
python ./evaluate.py features.test features.result