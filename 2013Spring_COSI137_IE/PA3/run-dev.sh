#!/bin/sh

python feature-extract.py data/coref-trainset.gold coref-trainset.feature
python feature-extract.py data/coref-devset.notag coref-devset.feature

./mallet-maxent-classifier.sh -train  -model=models/coref-head-model -gold=coref-trainset.feature
./mallet-maxent-classifier.sh -classify  -model=models/coref-head-model -input=coref-devset.feature > coref-devset.tagged

python coref-evaluator.py data/coref-devset.gold coref-devset.tagged
