"""Hidden Markov Model sequence tagger

"""
from base_classifier import BaseClassifier
import util
import numpy
import math
_DEBUG = False
class HMM(BaseClassifier):

	def __init__(self):
		"""the word_tag_codebook stores each entry of word and tag"""
		self.label_codebook = util.label_codebook
		self.feature_codebook = util.feature_codebook
		#self.word_tag_codebook = util.word_tag_codebook
	def _collect_counts(self, instance_list):
		"""Collect counts necessary for fitting parameters

		This function should update self.transition_count_table
		and self.feature_count_table based on this new given instance
		
		1) separately counts the occurrences of words and tags and populate the feature_count_table 
		2) also populate the transition_count_table by recording the transition I->B with increment of transition_count_table[I][B]
		Returns None
		"""
		pass
		self.init_count = numpy.zeros(self.label_codebook.size())
		#for the calculation of beta values
		self.termination_count = numpy.zeros(self.label_codebook.size())
		self.transition_count_table = numpy.zeros((self.label_codebook.size(),self.label_codebook.size()))
		self.feature_count_table = numpy.zeros((self.feature_codebook.size(),self.label_codebook.size()))
		
		for ins in instance_list:
			self.init_count[self.label_codebook.get_index(ins.label[0])] +=1
			self.termination_count[self.label_codebook.get_index(ins.label[-1])] +=1
			for index in range(0,len(ins.label)-1):
				self.transition_count_table[self.label_codebook.get_index(ins.label[index+1]),self.label_codebook.get_index(ins.label[index])]+=1
				self.feature_count_table[self.feature_codebook.get_index(ins.data[index][0]),self.label_codebook.get_index(ins.label[index])]+=1
				self.feature_count_table[self.feature_codebook.get_index(ins.data[index][1]),self.label_codebook.get_index(ins.label[index])]+=1
			index = len(ins.label)-1
			#print len(ins.label)
			#print index
			self.feature_count_table[self.feature_codebook.get_index(ins.data[index][0]),self.label_codebook.get_index(ins.label[index])]+=1
			self.feature_count_table[self.feature_codebook.get_index(ins.data[index][1]),self.label_codebook.get_index(ins.label[index])]+=1
	def train(self, instance_list):
		"""Fit parameters for hidden markov model

		Update codebooks from the given data to be consistent with
		the probability tables 

		Transition matrix and emission probability matrix
		will then be populated with the maximum likelihood estimate 
		of the appropriate parameters

		1) compute the transition probability and emission probability based on the counts 
		2) also compute the init_pro (the probability from beginning to t=1) and termination_pro (probability from t=T to end)
		3) smoothing the probability table by adding one
		Returns None
		"""
		#self.transition_count_table = numpy.zeros((1,1))
		#self.feature_count_table = numpy.zeros((1,1))
		self._collect_counts(instance_list)
		#TODO: estimate the parameters from the count tables
		self.init_pro = self.init_count/self.init_count.sum()
		self.termination_pro = self.termination_count/self.termination_count.sum()
		self.transition_matrix = numpy.zeros((self.label_codebook.size(),self.label_codebook.size()))
		self.emission_matrix = numpy.zeros((self.feature_codebook.size(),self.label_codebook.size()))
		#for smoothing 
		self.transition_count_table +=1.
		self.feature_count_table +=1.
		self.transition_matrix = self.transition_count_table/numpy.sum(self.transition_count_table,0)
		self.emission_matrix = self.feature_count_table/(numpy.sum(self.feature_count_table,0)/2)
	def classify_instance(self, instance):
		"""Viterbi decoding algorithm

		Wrapper for running the Viterbi algorithm
		We can then obtain the best sequence of labels from the backtrace pointers matrix
		
		1)based on the populated trellis and the backtrace_pointers find the best sequence of label 
	
		Returns a list of label indices e.g. [0, 1, 0, 3, 4]
		"""
		trellis,backtrace_pointers = self.dynamic_programming_on_trellis(instance, False)
		max_last_seq = numpy.argmax(trellis[len(instance.data)-1])
		k = max_last_seq
		best_sequence = []
		best_sequence.insert(0,k)
		for i in reversed(range(1,len(instance.data))):
			best_sequence.insert(0,backtrace_pointers[i][k])
			k = backtrace_pointers[i][k]
		return best_sequence

	def compute_observation_loglikelihood(self, instance):
		"""Compute and return log P(X|parameters) = loglikelihood of observations"""
		trellis = self.dynamic_programming_on_trellis(instance, True)
		loglikelihood = math.log(trellis[len(instance.data)-1].sum())
		
		return loglikelihood

	def dynamic_programming_on_trellis(self, instance, run_forward_alg=True):
		"""Run Forward algorithm or Viterbi algorithm

		This function uses the trellis to implement dynamic
		programming algorithm for obtaining the best sequence
		of labels given the observations

		1)for the condition where we needs two observation features(word and tag) calculating the emission probability(b_j(o_j))(the observation_prob_vector) by multiply word probability and tag probability which are stored in the emission matrix.
		2)populate the trellis with alpha values for foward algorithm just use the sum function to sum up one column of alpha values and for viterbi using argmax instead and also store the backtrace pointer

		Returns tuple with trellis filled up with the forward probabilities 
		and backtrace pointers for finding the best sequence
		"""
		#TODO:Initialize trellis and backtrace pointers 
		trellis = numpy.zeros((len(instance.data),self.label_codebook.size()))
		backtrace_pointers = numpy.zeros((len(instance.data),self.label_codebook.size()))
		#TODO:Traverse through the trellis here
		#observation_prob_vector = self.emission_matrix[self.feature_codebook.get_index(instance.data[0][0]),:]*self.emission_matrix[self.feature_codebook.get_index(instance.data[0][1]),:]
		observation_prob_vector = self.emission_matrix[self.feature_codebook.get_index(instance.data[0][1]),:]
		if run_forward_alg == True:
			#the first element of the alpha values
			trellis[0]=self.init_pro*observation_prob_vector
			for i in range(1,len(instance.data)):
				#observation_prob_vector = self.emission_matrix[self.feature_codebook.get_index(intance.data[i][0]),:]*self.emission_matrix[self.feature_codebook.get_index(intance.data[i][1]),:]
				observation_prob_vector = self.emission_matrix[self.feature_codebook.get_index(intance.data[i][0]),:]
				trellis[i]=(trellis[i-1]*self.transition_matrix).sum(1)*observation_prob_vector
			return trellis
		else:
			trellis[0]=self.init_pro*observation_prob_vector
			#backtrace_pointers[0] = ('START','START','START')
			for i in range(1,len(instance.data)):
				#observation_prob_vector = self.emission_matrix[self.feature_codebook.get_index(instance.data[i][0]),:]*self.emission_matrix[self.feature_codebook.get_index(instance.data[i][1]),:]
				observation_prob_vector = self.emission_matrix[self.feature_codebook.get_index(instance.data[i][1]),:]
				#here is an important place,we have to select the max then multiply the emission probability
				#if _DEBUG==True:
					#import pdb
					#pdb.set_trace()
				alpha_list = trellis[i-1]*self.transition_matrix
				trellis[i]=(alpha_list).max(1)*observation_prob_vector
				backtrace_pointers[i]=numpy.argmax(alpha_list,1)		

			return (trellis, backtrace_pointers)

	def train_semisupervised(self, unlabeled_instance_list, labeled_instance_list=None):
		"""Baum-Welch algorithm for fitting HMM from unlabeled data (EXTRA CREDIT)

		The algorithm first initializes the model with the labeled data if given.
		The model is initialized randomly otherwise. Then it runs 
		Baum-Welch algorithm to enhance the model with more data.

		1)If there is no labeled data provided, the function will first create a uniform HMM
		2)in E-step after get the forward and backward values,using the equation in the slides to expect the estimated counts of features and emission
		2)in M-step using the expected counts to updata the models feature_count_table and emission_count_table

		Returns None
		"""
		if labeled_instance_list is not None:
			self.train(labeled_instance_list)
		else:
			#TODO: initialize the model randomly
			#create a uniform HMM by initializing the pi,A matrix and B matrix
			self.init_pro = [1./self.label_codebook.size() for i in range(0,self.label_codebook.size())]
			self.termination_pro = self.init_pro[:]
			init_transition = numpy.ones((self.label_codebook.size(),self.label_codebook.size()))		
			self.transition_matrix = init_transition/init_transition.sum(0)
			init_emission = numpy.ones((self.feature_codebook.size(),self.label_codebook.size()))
			self.emission_matrix = init_emission/(init_emission.sum(0)/2.)
			old_logprob = 0.
			iteration = 0
			#converged = False
			max_iterations = 1000
		while iteration < max_iterations:
			#E-Step
			logprob = 0.
			#prob  =0.
			self.expected_transition_counts = numpy.zeros((self.label_codebook.size(),self.label_codebook.size()))
			self.expected_feature_counts = numpy.zeros((self.feature_codebook.size(),self.label_codebook.size()))
			for instance in unlabeled_instance_list:
				(alpha_table, beta_table) = self._run_forward_backward(instance)
				#TODO: update the expected count tables based on alphas and betas
				#also combine the expected count with the observed counts from the labeled data
				#calculate gamma which is the probability for observation at certain position in certain state
				#compute the probability of the sequence
				T = len(instance.data)
				prob = (alpha_table[T-1]*self.termination_pro).sum()
				#print prob
				#if prob == 0.:
					#continue
				logprob += math.log(prob)
				gamma = alpha_table*beta_table/prob
				self.init_count += gamma[0]
				self.termination_count+= gamma[T-1]
				for index in range(0,T-1):
					self.expected_feature_counts[self.feature_codebook.get_index(instance.data[index][0]),:] += gamma[index]
					self.expected_feature_counts[self.feature_codebook.get_index(instance.data[index][1]),:] += gamma[index]
					observation_vector = self.emission_matrix[self.feature_codebook.get_index(instance.data[index+1][0]),:]*self.emission_matrix[self.feature_codebook.get_index(instance.data[index+1][1]),:]
					Xi = alpha_table[index]*self.transition_matrix*observation_vector*beta_table[index+1]/prob
					self.expected_transition_counts+=Xi
				index = T-1
				self.expected_feature_counts[self.feature_codebook.get_index(instance.data[index][0]),:] += gamma[index]
				self.expected_feature_counts[self.feature_codebook.get_index(instance.data[index][1]),:] += gamma[index]
			#M-Step
			#TODO: reestimate the parameters
			self.init_pro = self.init_count/self.init_count.sum()
			self.termination_pro = self.termination_count/self.termination_count.sum()
			#update the model's feature count table and transition count table and also do some smoothing
			self.feature_count_table +=0.001+0.999* self.expected_feature_counts
			self.transition_count_table += 0.001+0.999*self.expected_transition_counts
			self.transition_matrix = self.transition_count_table/numpy.sum(self.transition_count_table,0)
			self.emission_matrix = self.feature_count_table/(numpy.sum(self.feature_count_table,0)/2)
			
			if self._has_converged(old_logprob, logprob):
				break
			old_logprob = logprob
			iteration +=1
			print iteration

	def _has_converged(self, old_likelihood, likelihood):
		"""Determine whether the parameters have converged or not (EXTRA CREDIT)

		Returns True if the parameters have converged.	
		"""
		
		if abs(old_likelihood-likelihood) < math.log(1e-6):
			return True
		else:
			return False

	def _run_forward_backward(self, instance):
		"""Forward-backward algorithm for HMM using trellis (EXTRA CREDIT)
	
		Fill up the alpha and beta trellises (the same notation as 
		presented in the lecture and Martin and Jurafsky)
		You can reuse your forward algorithm here

		return a tuple of tables consisting of alpha and beta tables
		"""
		#TODO: implement forward backward algorithm right here
		alpha_table = numpy.zeros((len(instance.data),self.label_codebook.size()))
		beta_table = numpy.zeros((len(instance.data),self.label_codebook.size()))
		#TODO:Traverse through the trellis here
		observation_prob_vector = self.emission_matrix[self.feature_codebook.get_index(instance.data[0][0]),:]*self.emission_matrix[self.feature_codebook.get_index(instance.data[0][1]),:]
		#the first element of the alpha values
	       	alpha_table[0]=self.init_pro*observation_prob_vector
		T = len(instance.data)
		beta_table[T-1] = self.termination_pro
		for i in range(1,T):
			observation_prob_vector_alpha = self.emission_matrix[self.feature_codebook.get_index(instance.data[i][0]),:]*self.emission_matrix[self.feature_codebook.get_index(instance.data[i][1]),:]
			observation_prob_vector_beta = self.emission_matrix[self.feature_codebook.get_index(instance.data[T-i][0]),:]*self.emission_matrix[self.feature_codebook.get_index(instance.data[T-i][1]),:]
			alpha_table[i]=(alpha_table[i-1]*self.transition_matrix).sum(1)*observation_prob_vector_alpha
			beta_table[T-i-1]=(beta_table[T-i]*self.transition_matrix*observation_prob_vector_beta).sum(1)

		return (alpha_table, beta_table)

	def to_dict(self):
		"""Convert HMM instance into a dictionary representation

		The implementation of this should be in sync with from_dict function.
		You should be able to use these two functions to convert the model into
		either representation (object or dictionary)
		"""
		model_dict = {
			'label_alphabet': label_codebook.to_dict(),
			'feature_alphabet': feature_codebook.to_dict()
		}
		return model_dict

	@classmethod
	def from_dict(model_dict):
		"""Convert a dictionary into HMM instance
		
		The implementation of this should be in sync with to_dict function.
		"""
		return HMM()
