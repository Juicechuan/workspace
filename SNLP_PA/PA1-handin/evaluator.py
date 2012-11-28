"""Evaluator functions

You will have to implement more evaluator functions in this class.
We will keep them all in this file.
"""

def split_train_test(classifier, instance_list, proportions, func_id,limits):
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
	if len(proportions) != 2:
		raise ValueError("Proportion must be a list of length 2. Got %s." % proportions)
	
	half_ins = (int)(len(instance_list)*0.5)
	train_factor = (int)(half_ins*proportions[0])
	train_dataset = instance_list[:train_factor] + instance_list[-train_factor:]
	test_dataset = instance_list[train_factor:half_ins] + instance_list[half_ins:-train_factor]
	
	correct=0.
	correct_pos=0.
	correct_neg=0.
	classifier.train(train_dataset,func_id,limits)
	
	for ins in test_dataset:
		if classifier.classify_instance(ins) ==	ins.label:
			correct += 1
	#print 'Hi'
	
	accuracy = correct/len(test_dataset)	

	print 'The number of train set is ' + repr(len(train_dataset))+'.\n' \
	      'The number of test set is ' + repr(len(test_dataset))+'.\n'\
	      'The classification accuracy we got is %.3f%%. \n'%(accuracy*100)
	       
	return accuracy
