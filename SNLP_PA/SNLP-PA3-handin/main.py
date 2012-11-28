import nltk
import numpy as np
from maxent import MaxEnt
from helper import Instance
import util
import evaluator

ME = MaxEnt()

def load_instance(filepath):
	ins_list=[]
	filelist = get_ipython().getoutput(u'ls '+filepath)
	for filename in filelist:
		f = open(filepath+filename,'r')
		tokens=[]
		data=np.zeros(0,dtype=np.int)
		#read each line
		for l in f:
			tokens += nltk.regexp_tokenize(l,pattern="\w+")
		data = np.array(util.del_dup(tokens))
		if filepath[-4:-1] == 'neg':
			ins = Instance(filename,0,data,tokens)	
		elif filepath[-4:-1] == 'pos':
			ins = Instance(filename,1,data,tokens)
		else: 
			raise Exception, "Wrong path!"
		ins_list.append(ins)
	f.close()
    	return ins_list

instance_list = load_instance('txt_sentoken/neg/')
instance_list += load_instance('txt_sentoken/pos/')

#prop = [0.2,0.8]

#accuracy = evaluator.split_train_test(ME,instance_list,prop)
#print ME.parameters

CM = evaluator.k_fold_cross_validation(ME,instance_list,7)
CM.print_out()
   

