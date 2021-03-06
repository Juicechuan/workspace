# -*- coding: utf-8 -*-
"""Maximum entropy classifier 

A standard implementation of maximum entropy classifier.
"""
import numpy
from scipy.optimize import fmin_l_bfgs_b
from scipy.misc import logsumexp

from base_classifier import BaseClassifier
from helper import Alphabet
#import math

class MaxEnt(BaseClassifier):

	def __init__(self):
		"""Initialize the model

		label_codebook, feature_codebook, parameters must be
		assigned properly in order for the model to work.

		parameters and codebooks will be handled in the train function
		"""
		super(MaxEnt, self).__init__()
		self.label_codebook = Alphabet()
		self.feature_codebook = Alphabet()
		#self.gaussian_prior_variance = 1
		self.parameters = []	
		self.gaussian_prior_variance = 1.0

	def compute_observed_counts(self, instance_list):
		"""Compute observed feature counts

		It should only be done once because it's parameter-independent.
		The observed feature counts are then stored internally.
		Note that we are fitting the model with the intercept terms
		so the count of intercept term is the count of that class.
		
		fill the feature_counts table with observed counts
		"""
		#the data and label in instance both use sparse vector
		self.feature_counts = numpy.zeros((self.feature_codebook.size() + 1) * self.label_codebook.size())
		for instance in instance_list:	
			Y_index = (self.feature_codebook.size()+1)*instance.label
			self.feature_counts[Y_index] +=1
			#instance.data is numpy array
			indices = Y_index + instance.data +1 
			self.feature_counts[indices] +=1
		
		#print self.feature_counts[:self.feature_codebook.size()+1]
		#print self.feature_counts[self.feature_codebook.size()+1:]

	def compute_expected_feature_counts(self,instance_list):
		"""Compute expected feature counts

		E(feature|X) = sum over i,y E(feature(Xi,yi)|Xi)
					 = sum over i,y feature(Xi,yi) P(Y=yi|Xi)
		We take advantage of inference function in this class to compute
		expected feature counts, which is only needed for training.
		
		computing the expected feature counts by adding up all the expectation counts of all feature.
		return expected feature counts table
		"""
		expected_feature_counts = numpy.zeros(len(self.parameters))
		for instance in instance_list:
			posterior = self.compute_label_unnormalized_loglikelihood_vector(instance.data)
			posterior = numpy.exp(posterior-logsumexp(posterior))
			for label in range(0,self.label_codebook.size()):
				Y_index = label*(self.feature_codebook.size() + 1)
				expected_feature_counts[Y_index] += posterior[label]
				indices = Y_index + instance.data + 1
				expected_feature_counts[indices] += posterior[label]
		return expected_feature_counts

	def classify_instance(self, instance):
		"""Applying the model to a new instance

		Returns:
		       label with the maximum probability 
		"""
		vector = self.compute_posterior_distribution(instance)
		#print vector
		pre_label_index = numpy.argmax(vector) 		
		return pre_label_index

	def compute_posterior_distribution(self, instance):
		"""Compute P(Y|X)
		
		Return a vector of the same size as the label_codebook
		the vector contains the unnormalized likelihood vector since we only use them for finding the most probable label, so we don't have
		to normalized it.
		"""
		sparse_vector = numpy.array([self.feature_codebook.get_index(i) for i in instance.data if self.feature_codebook.has_label(i)])
		posterior_distribution = numpy.zeros(self.label_codebook.size())
		posterior_distribution = numpy.exp(self.compute_label_unnormalized_loglikelihood_vector(sparse_vector))
		return posterior_distribution

	def compute_label_unnormalized_loglikelihood_vector(self,sparse_feature_vector):
		"""Compute unnormalized log score from log-linear model

		log P(Y|X) is proportional to feature vector * parameter vector
		But we use a sparse vector representation, so we need to use
		index tricks that numpy allows us to do.
		
		for each label compute the unnormalized loglikelihood (sum of lambdas) given the sparse_feature_vector
		Returns:
		       a vector of scores according to different y(label)
		"""
		loglikelihood_score_vector = numpy.zeros(self.label_codebook.size())
	
		for label in range(0,self.label_codebook.size()):
			Y_index = label*(self.feature_codebook.size() + 1)
			indices = Y_index + sparse_feature_vector + 1
			if len(indices)!=0:
				loglikelihood_score_vector[label] = self.parameters[Y_index] + sum(self.parameters[indices])
			else:
				loglikelihood_score_vector[label] = self.parameters[Y_index]
			
		return loglikelihood_score_vector


	def objective_function(self, parameters):
		"""Compute negative (log P(Y|X,lambdas) + log P(lambdas))

		The function that we want to optimize over. Here I use Gaussian distribution(mean=0.0 sigma=1.0) prior to model P(lambda)
		Args:
		     parameters updated by the training procedure
		Returns:
		     negtive total likelihood
		"""
		total_loglikelihood = 0.0
		numerator = 0.0
		denominator = 0.0
		#prior = 0.0
		#self.gaussian_prior_variance = 1.0
		prior = sum([i**2/(2*self.gaussian_prior_variance**2) for i in parameters])
		self.parameters=numpy.array(parameters)
		# Compute the loglikelihood here
		loglikelihood_score_vector = numpy.zeros(self.label_codebook.size())
		for instance in self.training_data:
			Y_index = instance.label*(self.feature_codebook.size() + 1) 
			indices = Y_index + instance.data + 1
			numerator += (parameters[Y_index]+sum(parameters[indices]))
			score_vector = self.compute_label_unnormalized_loglikelihood_vector(instance.data)
			#print score_vector
			denominator += logsumexp(score_vector)
		#print numerator
		#print denominator
		total_loglikelihood = numerator - denominator - prior
		print  - total_loglikelihood
		return - total_loglikelihood


	def gradient_function(self, parameters):
		"""Compute gradient of negative (log P(Y|X,lambdas) + log P(lambdas)) wrt lambdas

		With some algebra, we have that
		gradient wrt lambda i = observed_count of feature i - expected_count of feature i - lambda i / gaussian_prior_variance^2
		The first term is computed before running the optimization function and is a constant.
		The second term needs inference to get P(Y|X, lambdas) and is a bit expensive.
		The third term is from taking the derivative of log gaussian prior
		
		Returns:
			a vector of gradient
		"""
		self.parameters = numpy.array(parameters)
		#print self.parameters
		#print parameters
		gradient_vector = numpy.zeros(len(parameters))
		observed_count_vector = self.feature_counts
		expected_count_vector = self.compute_expected_feature_counts(self.training_data)
		dprior = numpy.array([i/self.gaussian_prior_variance**2 for i in parameters])
		# compute gradient here
		gradient_vector = observed_count_vector - expected_count_vector - dprior 
		return - gradient_vector


	def train(self, instance_list):
		"""Find the optimal parameters for maximum entropy classifier

		We setup an instance of MaxEnt to use as an inference engine
		necessary for parameter fitting. MaxEnt instance and training set
		are stored internally in the trainer just so we can avoid putting in
		extra arguments into the optimization function.
		We leave the actual number crunching and search to fmin_bfgs function.
		There are a few tunable parameters for the optimization function but
		the default is usually well-tuned and sufficient for most purposes.

		Arg:
			instance_list: each instance.data should be a string feature vectors
				This function will create a sparse feature vector representation
				based on the alphabet.

		Returns:
			Maximum entropy classifier with the parameters (MAP estimate from the data
			and Gaussian prior)
		"""
		assert(len(instance_list) > 0)
		######################################
		# Do any further processing right here e.g populate codebook
		# making sparse vectors, etc.
		self.label_codebook.add('neg')
		self.label_codebook.add('pos')
		for index,instance in enumerate(instance_list):
			sparse_vector = numpy.zeros(0,dtype=numpy.int)
			for feature in instance.data:
				if not self.feature_codebook.has_label(feature):
					self.feature_codebook.add(feature)
					sparse_vector = numpy.append(sparse_vector,self.feature_codebook.get_index(feature))
				else:
					sparse_vector = numpy.append(sparse_vector,self.feature_codebook.get_index(feature))		
					
			instance_list[index].data = sparse_vector

		##################
		self.parameters = numpy.zeros((self.feature_codebook.size() + 1) * self.label_codebook.size())
		self.training_data = instance_list
		self.compute_observed_counts(instance_list)
		num_labels = self.label_codebook.size()
		num_features = self.feature_codebook.size()
		init_point = numpy.zeros(num_labels * (num_features + 1))
		optimal_parameters, _, _ = fmin_l_bfgs_b(self.objective_function, init_point, fprime=self.gradient_function)
		print optimal_parameters
		self.parameters = optimal_parameters

	def to_dict(self):
		model_dict = {
			'label_alphabet': self.label_codebook.to_dict(),
			'feature_alphabet': self.feature_codebook.to_dict(),
			'parameters': self.parameters.tolist(),
		}
		return model_dict

	@classmethod
	def from_dict(cls, model_dictionary):
		model_instance = MaxEnt()
		model_instance.label_codebook = Alphabet.from_dict(model_dict['label_alphabet'])
		model_instance.feature_codebook = Alphabet.from_dict(model_dict['feature_alphabet'])
		model_instance.p_x_given_y_table = numpy.array(model_dict['parameters'])

		return model_instance
