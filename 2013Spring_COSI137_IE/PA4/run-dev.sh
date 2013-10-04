#!/bin/sh

python feature-extract.py data/rel-trainset.gold rel-trainset.feature
python feature-extract.py data/rel-devset.raw rel-devset.feature

./mallet-maxent-classifier.sh -train  -model=models/rel-head-model -gold=rel-trainset.feature
./mallet-maxent-classifier.sh -classify  -model=models/rel-head-model -input=rel-devset.feature > rel-devset.tagged

python relation-evaluator.py data/rel-devset.gold rel-devset.tagged
