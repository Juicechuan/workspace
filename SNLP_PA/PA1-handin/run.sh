#!/bin/bash
#run with selecting the 2000 most frequent features
echo 'run with selecting the 2000 most frequent features...' 
i=0
while (($i<10)) 
do
   ipython main.py 0 2000 >> results/record_freq_2000.txt
   i=$(($i+1))
done

#run with selecting the 2000 most frequent features and filtering the stopwords
echo 'run with selecting the 2000 most frequent features and filtering the stopwords'
i=0
while (($i<10)) 
do
   ipython main.py 1 2000 >> results/record_freq_stop_2000.txt
   i=$(($i+1))
done

#run with selecting the 4000 most frequent features
echo 'run with selecting the 4000 most frequent features...' 
i=0
while (($i<10)) 
do
   ipython main.py 0 4000 >> results/record_freq_4000.txt
   i=$(($i+1))
done

#run with selecting the 4000 most frequent features and filtering the stopwords
echo 'run with selecting the 4000 most frequent features and filtering the stopwords...'
i=0
while (($i<10)) 
do
   ipython main.py 1 4000 >> results/record_freq_stop_4000.txt
   i=$(($i+1))
done

#run with selecting the 6000 most frequent features
echo 'run with selecting the 6000 most frequent features...' 
i=0
while (($i<10)) 
do
   ipython main.py 0 6000 >> results/record_freq_6000.txt
   i=$(($i+1))
done

#run with selecting the 6000 most frequent features and filtering the stopwords
echo 'run with selecting the 6000 most frequent features and filtering the stopwords...'
i=0
while (($i<10)) 
do
   ipython main.py 1 6000 >> results/record_freq_stop_6000.txt
   i=$(($i+1))
done

