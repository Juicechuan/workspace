from helper import Alphabet
#global variables 
feature_codebook = Alphabet()
label_codebook = Alphabet()

def del_dup(seq):
	"""delete the duplicated occurrences in seq"""
	return {}.fromkeys(seq).keys()
