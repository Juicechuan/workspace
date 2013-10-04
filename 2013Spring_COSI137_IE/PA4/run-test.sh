#!/bin/sh

python feature-extract.py data/rel-trainset.gold rel-trainset.feature
python feature-extract.py data/rel-testset.raw rel-testset.feature

./mallet-maxent-classifier.sh -train  -model=models/rel-head-model -gold=rel-tr\
ainset.feature
./mallet-maxent-classifier.sh -classify  -model=models/rel-head-model -input=re\
l-testset.feature > rel-testset.tagged

python relation-evaluator.py data/rel-testset.gold rel-testset.tagged