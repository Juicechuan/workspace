import json

class BaseClassifier(object):
	"""Many functions are classifier independent
	so we want them all to share the functionality"""


	def train(self, instance_list):
		"""Train the classifier based on the dataset"""
		raise NotImplementedError

	def classify_instance(self, instance):
		"""Returns the predicted label given the data in instance"""
		raise NotImplementedError

	def compute_log_unnormalized_score(self, instance):
		"""Compute log score for all values of Y"""
		raise NotImplementedError

	def save(self, model_file_name):
		"""save the model to a file"""
		var_name_to_value = self.to_dict()
		json.dump(var_name_to_value, open(model_file_name,'w'))

	def to_dict(self):
		"""if you want to serialize the classifier, this method and from_dict
		must be implemented"""
		raise NotImplementedError

	@classmethod
	def load(cls, model_file_name):
		"""load the classifier from a file"""
		model_dictionary = json.load(open(model_file_name))
		return cls.from_dict(model_dictionary)

	@classmethod
	def from_dict(cls, model_dictionary):
		"""if you want to serialize the classifier, this method and to_dict
		must be implemented"""
		raise NotImplementedError
