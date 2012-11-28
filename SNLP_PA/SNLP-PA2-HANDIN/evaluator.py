"""Evaluator functions

You will have to implement more evaluator functions in this class.
We will keep them all in this file.
"""

def split_train_test(classifier, instance_list, proportions):
	"""Perform random split train-test

	Train on x proportion of the data and test the model on 1-x proportion
	return the performance report

	Args :
		classifier - a subclass of BaseClassifier
		instance_list - dataset to perform cross-validation on
		proportions - a list of two numbers. sum(proportions) == 1
			proportions[0] is the train proportion
			proportions[1] is the test proportion

	Returns :
		Accuracy rate
	"""
	train_len = (int)(proportions[0]*len(instance_list))
	test_len = (int)(proportions[1]*len(instance_list))
	train_set = instance_list[:train_len]
	test_set = instance_list[-test_len:]
	classifier.train(train_set)
	total_size = 0.
	correct_count = 0.
	for ins in test_set:
		label_list = ins.label
		predict_label = classifier.classify_instance(ins)
		total_size += len(label_list)
		for i,j in zip(label_list,predict_label):
			if classifier.label_codebook.get_index(i) == j:
				correct_count+=1
	accuracy=correct_count/total_size
	return accuracy

	if len(proportions) != 2:
		raise ValueError("Proportion must be a list of length 2. Got %s." % proportions)
	pass

def test_classifier(classifier, test_data):
	"""Evaluate the classifier given test data

	Evaluate the model on the test set and returns the evaluation
	result in a confusion matrix

	Returns:
		Confusion matrix
	"""
	confusion_matrix = ConfusionMatrix(classifier.label_codebook)
	for instance in test_data:
		prediction = classifier.classify_instance(instance)
		confusion_matrix.add_data(prediction, instance.label)
	return confusion_matrix	

import numpy
class ConfusionMatrix(object):

	def __init__(self, label_codebook):
		self.label_codebook = label_codebook
		num_classes = label_codebook.size()
		self.matrix = numpy.zeros((num_classes,num_classes))

	def add_data(self, prediction_list, true_answer_list):
		for	prediction, true_answer in zip(prediction_list, true_answer_list): 
			self.matrix[prediction, self.label_codebook.get_index(true_answer)] += 1

	def compute_precision(self):
		"""Returns a numpy.array where precision[i] = precision for class i""" 
		precision = numpy.zeros(self.label_codebook.size())
		for i in range(0,self.label_codebook.size()):
			precision[i] = self.matrix[i,i]/self.matrix[i].sum()
		return precision

	def compute_recall(self):
		"""Returns a numpy.array where recall[i] = recall for class i""" 
		recall = numpy.zeros(self.label_codebook.size())
		for i in range(0,self.label_codebook.size()):
			recall[i] = self.matrix[i,i]/self.matrix.sum(0)[i]
		return recall

	def compute_f1(self):
		"""Returns a numpy.array where f1[i] = F1 score for class i
	
		F1 score is a function of precision and recall, so you can feel free
		to call those two functions (or lazily load from an internal variable)
		But the confusion matrix is usually quite small, so you don't need to worry
		too much about avoiding redundant computation.
		""" 
		f1 = numpy.zeros(self.label_codebook.size())
		precision = self.compute_precision()
		recall = self.compute_recall()
		f1 = 2*precision*recall/(precision+recall)
		return f1

	def compute_accuracy(self):
		"""Returns accuracy rate given the information in the matrix"""
		correct_counts = 0.
		for i in range(0,self.label_codebook.size()):
			correct_counts += self.matrix[i][i]
		accuracy = correct_counts/self.matrix.sum()

		return accuracy

	def print_out(self):
		"""Printing out confusion matrix along with Macro-F1 score"""
		#header for the confusion matrix
		header = [' '] + [self.label_codebook.get_label(i) for i in xrange(self.label_codebook.size())]
		rows = []
		#putting labels to the first column of rhw matrix
		for i in xrange(self.label_codebook.size()):
			row = [self.label_codebook.get_label(i)] + [str(self.matrix[i,j]) for j in xrange(len(self.matrix[i,]))]
			rows.append(row)
		print "row = predicted, column = truth"
		print matrix_to_string(rows, header)

		# computing precision, recall, and f1
		precision = self.compute_precision()
		recall = self.compute_recall()
		f1 = self.compute_f1()
		for i in xrange(self.label_codebook.size()):
			print '%s \tprecision %f \trecall %f\t F1 %f' % (self.label_codebook.get_label(i), 
				precision[i], recall[i], f1[i])
		print 'accuracy rate = %f' % self.compute_accuracy()
	

def matrix_to_string(matrix, header=None):
	"""
	Return a pretty, aligned string representation of a nxm matrix.

	This representation can be used to print any tabular data, such as
	database results. It works by scanning the lengths of each element
	in each column, and determining the format string dynamically.

	the implementation is adapted from here
	mybravenewworld.wordpress.com/2010/09/19/print-tabular-data-nicely-using-python/

	Args:
		matrix - Matrix representation (list with n rows of m elements).
		header -  Optional tuple or list with header elements to be displayed.

	Returns:
		nicely formatted matrix string
	"""

	if isinstance(header, list):
		header = tuple(header)
	lengths = []
	if header:
		lengths = [len(column) for column in header]

	#finding the max length of each column
	for row in matrix:
		for column in row:
			i = row.index(column)
			column = str(column)
			column_length = len(column)
			try:
				max_length = lengths[i]
				if column_length > max_length:
					lengths[i] = column_length
			except IndexError:
				lengths.append(column_length)

	#use the lengths to derive a formatting string
	lengths = tuple(lengths)
	format_string = ""
	for length in lengths:
		format_string += "%-" + str(length) + "s "
	format_string += "\n"

	#applying formatting string to get matrix string
	matrix_str = ""
	if header:
		matrix_str += format_string % header
	for row in matrix:
		matrix_str += format_string % tuple(row)

	return matrix_str


