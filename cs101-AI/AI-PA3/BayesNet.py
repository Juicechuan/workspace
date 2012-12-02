"""
    Bayesian Network. 
    Variable Elimination algorithm implementation.
    class DiscreteCPT is the input data wrapping class, 
    which is from http://homes.soic.indiana.edu/classes/spring2012/csci/b553-hauserk/bayesnet.py.
    and based on code for Bayesian networks by Stuart Russell (http://aima-python.googlecode.com)
"""""
# import numpy as np
import copy
import itertools

class DiscreteCPT(object):
    """A conditional probability table for a variable with discrete values."""
    def __init__(self, vals, probTable):
        """vals is a list of discrete values the variable can assume.
        probTable should be a dictionary whose keys are tuples representing
        possible combinations of values for all the conditions; the corresponding
        value for each key is a list giving the probabilities corresponding
        to each of the values in vals.
        
        If the variable has no conditions -- that is, the node has no parents
        in the network -- probTable may be a list giving the
        prior distribution over the values in val.
        
        Ex 1:  candy = DiscreteCPT(['Lemon', 'Lime', 'Cherry'], [0.4,0.2,0.4])
        gives us a discrete variable representing the probability of various
        flavors of candy drawn from a bin.  This has no conditions.  Lemon
        and Cherry have probabilities of 40%, and Lime has a probability of
        20%.
        
        Ex 2:  candy = DiscreteCPT(['Lime', 'Cherry'],
                    {('b1',): [1.0, 0.0], 
                    ('b2',): [0.75, 0.25], 
                    ('b3',): [0.5, 0.5],
                    ('b4',): [0.25, 0.75],
                    ('b5',): [0.0, 1.0]})
        gives us a discrete variable representing the probability of flavors of
        candy, conditioned on which bin we draw the candy from.  (See B351 class
        slides for an illustration.)  Here bin 1 is composed of 100% lime
        candies, and bin 4 is composed of 25% Lime and 75% Cherry."""
        
        self.myVals = vals
        if isinstance(probTable, list) or isinstance(probTable, tuple):
            self.probTable = {(): probTable}
        else:
            self.probTable = probTable
            
    def values(self):
        """Returns the list of values the variable can take."""
        return self.myVals
    
    def prob_dist(self, parentVals):
        """Returns a dictionary giving a value:probability mapping for each
        value the variable can assume, given a tuple with values for all the
        conditions.
        
        Ex:  Uses the CPT defined in example 2 from __init__().
            candyProb3 = candy.prob_dist( ('b3',) )
        returns this dict:
            {'Lime': 0.5, 'Cherry': 0.5}
        """
        if isinstance(parentVals, list):
            parentVals = tuple(parentVals)
        return dict([(self.myVals[i], p) for i, p in \
                    enumerate(self.probTable[parentVals])])


class BayesNode:
    """Represent a node in the Bayesian Network, which contains the variable's name and the conditional probability distribution(cpt)."""
    def __init__(self, variable_name, parents, cpt):
            """"""
            self.variable_name = variable_name
            self.parents = parents
            self.cpt = cpt
    def variables(self):
            """return all the variables involved in the Bayes Node"""
            vlist = []
            vlist.append(self.variable_name)
            for p in self.parents:
                    vlist.append(p)
            return vlist
        
class Factor:
    """this class stores the dependent variables and probability table"""
    def __init__(self, variables, table={}):
        self.vars = variables
        self.table = table
        
    def remove_variable(self, var):
        """remove the var from the variables"""
        self.vars.remove(var)
    
    def set_table(self, table):
        self.table = table
    
    def normalize(self):
        """normalize the distribution of the probability so that it sums to 1"""
        sum = 0.0
        for i in self.table:
            sum += self.table[i]
        for i in self.table:
            self.table[i] = self.table[i]/sum

        print self.vars
        print self.table

class BayesNet(object):
    """implementation of Bayes Network"""
    def __init__(self, nodes=[]):
        """initialize the Bayes Network with a list of Bayes Nodes"""
        self.variables = [n.variable_name for n in nodes]
        self.vars = dict([(n.variable_name, n) for n in nodes])
        self.nodes = nodes
        
    def elimination_ask(self, X, e, order=reversed):
        """implement the variable elimination algorithm based on the figure 14.11 on the text book"""
        factors = []
        for varname in self.variables:
            f = self.make_factor(varname, e)
            factors.append(f)
#        for f in factors:
#            print f.vars,f.table
        for varname in order(self.variables):
            if self.is_hidden(varname, X, e):
                factors = self.sum_out(varname, factors)
    
#        for f in factors:
#            print f.vars,f.table
        return self.pointwise_product(factors).normalize()

    def pointwise_product(self, factors):
        """the pointwise product after the summing out step"""
        f = factors.pop()
        while len(factors) != 0:
            f1 = factors.pop()
            if f1.vars != []:
                f = self.pointwise_product_helper(f, f1)
        return f
        
    def is_hidden(self, var, X, e):
        return var != X and var not in e
        
    def event_values(self, e, vars):
        """return the variables' value which exist in the evidence
           if vars has no elements or has no elements exist in the evidence,
           it will return empty dictionary
        """
        return dict([(v, e[v]) for v in vars if v in e.keys()])
    
    def make_factor(self, varname, e):
        """return the factors initialized according to the known values in the evidence"""
        varnode = self.vars[varname]
    #         factor = copy.deepcopy(varnode)
        # vlist = varnode.variables()
    #         for var in e.keys():
    #             if var == varname:
    #                 #set CPT vals
    #                 factor.cpt.vals = [e[varname]]
    #                 factor.cpt.probTable = dict([(parentVal,factor.cpt.prob_dist(parentVal)[e[varname]]) for parentVal in factor.cpt.probTable.keys()])
    #         
    #         known_parent = self.event_values(e,factor.parents)        
    #         if known_parent != {}:#if known_parent == {}, it means that the variable has no parents or the parent is not in the evidence dictionary
    #             if len(known_parent)==len(factor.parents):#all parents appear in the evidence
    #                 parentVals = tuple([known_parent[var] for var in factor.parents])
    #                 factor.cpt.probTable = {parentVals:factor.cpt.prob_dist(parentVals)}
    #             else if len(known_parent) < len(factor.parents):#here we assume the there is only one known variable in evidence
    #                 for i,p in enumerate(factor.parents):
    #                     if p in known_parent.keys():
    #                         parentVals = [parentVal if parentVal[i]==known_parent[p] for parentVal in factor.cpt.probTable.keys()]
    #                         factor.cpt.proTable = dict([(parentVal,factor.cpt.prob_dist(parentVal)) for parentVal in parentVals])
        
        factor = Factor(varnode.variables(), {})
    
        if varname in e.keys():  # variables in the evidence
            factor.remove_variable(varname)
            factor.set_table(dict([(parentVal, varnode.cpt.prob_dist(parentVal)[e[varname]]) for parentVal in varnode.cpt.probTable.keys()]))
            return factor
            
        known_parent = self.event_values(e, varnode.parents)
        if known_parent != {}:  # parent variables in the evidence
            for i, p in enumerate(varnode.parents):
                if p in known_parent.keys():
                    factor.remove_variable(p)
                    parentVals = [parentVal for parentVal in varnode.cpt.probTable.keys() if parentVal[i] == known_parent[p]]
                    table = dict([(('T',) + self.new_values(parentVal,i), varnode.cpt.prob_dist(parentVal)['T']) for parentVal in parentVals])
                    table.update(dict([(('F',) + self.new_values(parentVal, i), varnode.cpt.prob_dist(parentVal)['F']) for parentVal in parentVals]))
                    factor.set_table(table)
                    return factor
                    
        # not any known values can be used, then return the factor corresponding to the original cpt
        parentVals = varnode.cpt.probTable.keys()
        table = dict([(('T',) + parentVal, varnode.cpt.prob_dist(parentVal)['T']) for parentVal in parentVals])
        table.update(dict([(('F',) + parentVal, varnode.cpt.prob_dist(parentVal)['F']) for parentVal in parentVals]))
        factor.set_table(table)
        return factor   
    
    def new_values(self,parentVal,i):
        """eliminate the ith variable in tuple parentVal"""
        new_parentVal = tuple([v for j,v in enumerate(list(parentVal)) if j != i])
        return new_parentVal

    def sum_out(self, var, factors):
        """get all factors over the joining variable
           build a new factor over the union of the variables involved
        """

        new_factor = None
        
        for factor in factors[:]:   #delete factor of hidden variables in list
            if var in factor.vars:
                if new_factor == None:
                    new_factor = copy.deepcopy(factor)
                    factors.remove(factor)
                    continue
                else:
                    new_factor = self.pointwise_product_helper(new_factor, factor)
                    factors.remove(factor)
        
        #print new_factor.vars,new_factor.table
        # do the sum out
        new_table = {}
        for i, v in enumerate(new_factor.vars):
            if v == var:
                for k in itertools.product('TF', repeat=len(new_factor.vars) - 1):
                    k1 = list(k)
                    k1.insert(i, 'T')
                    k2 = list(k)
                    k2.insert(i, 'F')
                    key = tuple(k1)
                    key1 = tuple(k2)
                    if key in new_factor.table.keys() and key1 in new_factor.table.keys():
                        new_table[k] = new_factor.table[key] + new_factor.table[key1]
        
        flag = False                
        for k in new_table:
            if new_table[k] != 1.0:
                flag = True
                break
        if flag:
            new_factor.set_table(new_table)
            new_factor.remove_variable(var)
        else:
            new_factor = Factor([],{():1.0})

        factors.append(new_factor)
        return factors
    
    def pointwise_product_helper(self, factor1, factor2):
        """do the binary pointwise product which is used in the sum out function."""
        same_var = []
        new_vars = factor1.vars[:]
        for var in factor2.vars:
            if var not in new_vars:
                new_vars.append(var)
            else:
                same_var.append(var)
                
        new_table = {}
        new_factor = Factor(new_vars, new_table)
#        print factor1.vars,factor1.table.keys()
#        print factor2.vars,factor2.table.keys()
        for key1 in factor1.table.keys():
            for key2 in factor2.table.keys():
                for i, var1 in enumerate(factor1.vars):
                    for j, var2 in enumerate(factor2.vars):
                        #print i,j
                        #print var1,var2
                        #print key1,key2
                        if var1 == var2 and key1[i] == key2[j]:
                            new_key = key1 + tuple([key2[p] for p, v in enumerate(factor2.vars) if v != var1 ])
                            new_factor.table[new_key] = factor1.table[key1] * factor2.table[key2]
        return new_factor                

#definition of the burglar Bayesian Network
burglarNet = BayesNet(
        [ BayesNode('Burglary', [],
            DiscreteCPT(['T', 'F'], [0.001, 0.999])),
        BayesNode('Earthquake', [],
            DiscreteCPT(['T', 'F'], [0.002, 0.998])),
        BayesNode('Alarm', ['Burglary', 'Earthquake'],
            DiscreteCPT(['T', 'F'],
                {('T', 'T'):[0.95, 0.05],
                ('T', 'F'):[0.94, 0.06],
                ('F', 'T'):[0.29, 0.71],
                ('F', 'F'):[0.001, 0.999]})),
        BayesNode('JohnCalls', ['Alarm'],
            DiscreteCPT(['T', 'F'],
                {('T',):[0.9, 0.1],
                ('F',):[0.05, 0.95]})),
        BayesNode('MaryCalls', ['Alarm'],
            DiscreteCPT(['T', 'F'],
                {('T',):[0.7, 0.3],
                ('F',):[0.01, 0.99]})) ])


evidence = dict(JohnCalls='T', MaryCalls='T')
evidence1 = dict(JohnCalls='T')
evidence2 = dict(Burglary='T')


print "result for the query P(Burglary|JohnCalls='T',MaryCalls='T')"
burglarNet.elimination_ask('JohnCalls', evidence2)
print "\n"
print "result for the query P(Earthquake|JohnCalls='T')"
burglarNet.elimination_ask('Earthquake', evidence1)
print "\n"
print "result for the query P(JohnCalls|Burglary='T')"
burglarNet.elimination_ask('JohnCalls', evidence2)

# def elimination_ask(X, e, bn, order=reversed):
#     "[Fig. 14.11]"
#     factors = []
#     for var in order(bn.vars):
#         var_node = bn.get_variable_node(var)
#         factors.append(make_factor(var_node,var, e))
#         if is_hidden(var, X, e):
#             factors = sum_out(var, factors)
#     return pointwise_product(factors).normalize()
# 
# def is_hidden(var, X, e):
#     return var != X and var not in e

# def make_factor(var_node, var, e):
#    depend_var = []
#    factor_table = {}
#
#    if len(var_node.parents)==0:#no-parent
#        
#        if var not in e.keys():
#            depend_var.append(var)
#            factor_table[(True,)] = var_node.cpt[()]
#            factor_table[(False,)] = 1-var_node.cpt[()]
#        else:
#            if e[var]:
#                factor_table[(e[var],)] = var_node.cpt[()]
#            else:
#                factor_table[(e[var],)] = 1-var_node.cpt[()]
#        return tuple((depend_var,factor_table))
#
#    if len(var_node.parents)==1:#1-parent
#        parent = var_node.parents
#        if var not in e.keys():
#            depend_var.append(var)
#            if parent in e.keys():
#                factor_table[(True,e[parent])] = var_node.cpt[e[parent]]
#                factor_table[(False,e[parent])] = 1- var_node.cpt[e[parent]]
#            else:
#                depend_var.append(parent)
#                factor_table = dict([((True,key),value) for key,value in var_node.cpt.items()])
#                factor_table.update(dict([((False,key),1-value) for key,value in var_node.cpt.items()]))
#        else:
