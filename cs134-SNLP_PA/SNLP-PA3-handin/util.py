
def del_dup(seq):
	"""delete the duplicated occurrences in seq"""
	return {}.fromkeys(seq).keys()
