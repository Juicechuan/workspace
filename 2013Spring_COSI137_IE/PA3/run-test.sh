#!/bin/sh

#python feature-extract.py data/coref-trainset.gold coref-trainset.feature
python feature-extract.py data/coref-testset.notag coref-testset.feature

#./mallet-maxent-classifier.sh -train  -model=models/coref-head-model -gold=coref-trainset.feature
./mallet-maxent-classifier.sh -classify  -model=models/coref-head-model -input=coref-testset.feature > coref-testset.tagged

python coref-evaluator.py data/coref-testset.gold coref-testset.tagged
