from helper import Alphabet
import numpy

class HMM(object):
    
    def __init__(self,label,obs):
        """initialize the model codebook"""
        self.label = label
        self.obs = self._collect_counts(obs)

    def _collect_counts(self,obs):
        dic = Alphabet()
        for ob in obs:
            dic.add(ob)
        return dic
    
    def load_model(self,init_prob,tm,em):
        """load the predefined parameters of the HMM model"""
        self.init_prob = numpy.array(init_prob)
        self.transition_matrix = numpy.array(tm)
        self.emission_matrix = numpy.array(em)

    def populate_trellis(self,instance,run_forward=True):
        """fill in the trellis of HMM model"""
        trellis = numpy.zeros((len(instance),len(self.label)))
        backtrace_pointers = numpy.zeros((len(instance),len(self.label)))
        obs_prob = self.emission_matrix[self.obs.get_index(instance[0])]
        
        if run_forward==True:
            trellis[0] = self.init_prob*obs_prob
            for i in range(1,len(instance)):
                obs_prob = self.emission_matrix[self.obs.get_index(instance[i])]
                alpha = trellis[i-1]*self.transition_matrix
                trellis[i] = alpha.sum(1)*obs_prob
                
            return trellis
        else:
            #the initial alpha value
            #import pdb
            #pdb.set_trace()
            trellis[0] = self.init_prob*obs_prob
            for i in range(1,len(instance)):
                obs_prob = self.emission_matrix[self.obs.get_index(instance[i])]
                alpha = trellis[i-1]*self.transition_matrix
                trellis[i] = (alpha).max(1)*obs_prob
                backtrace_pointers[i] = numpy.argmax(alpha,1)

            return (trellis,backtrace_pointers)

    def classify_instance(self,instance):
        trellis,backtrace_pointers = self.populate_trellis(instance,False)
        max_last_seq = numpy.argmax(trellis[len(instance)-1])
        k =  max_last_seq
        best_seq = []
        best_seq.insert(0,k)
        for i in reversed(range(1,len(instance))):
            best_seq.insert(0,backtrace_pointers[i][k])
            k = backtrace_pointers[i][k]
        return best_seq

def main():
    labels = [0,1]
    obs = ["A","C","G","T"]
    hmm = HMM(labels,obs)

    init_prob = [0.5,0.5]
    tm = [[0.96,0.1],[0.04,0.9]]
    em = [[0.4,0.2],[0.1,0.3],[0.1,0.3],[0.4,0.2]]
    instance0 = list("ACGT")
    instance1 = list("ACATCGTCGGTAGT")

    hmm.load_model(init_prob,tm,em)
    print hmm.populate_trellis(instance0,True)
    print hmm.populate_trellis(instance1,False)
    print hmm.classify_instance(instance1)
    
if __name__ == "__main__":
    main()
