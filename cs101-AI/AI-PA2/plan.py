"""
plan.py
author=Chuan Wang,Chen Xing
"""

import search
from random import choice
import copy
_DEBUG = False
import itertools

class Fluent(object):
    """
    Represents a fluent in a planning problem.
    """
    def __init__(self, name, *variables):
        """
        Takes a function name and 0 or more variables and makes a fluent with that
        name and those variables.
        """
        self.name = name
        self.variables = list(variables)

    def bind(self, variable_mapping):
        """
        Takes a dictionary mapping variable names to new values, and returns a version
        of the fluent with those variables replaced with those values.
        """
        new_variables = []
        for variable in self.variables:
            if variable in variable_mapping:
                new_variables.append(variable_mapping[variable])
            else:
                new_variables.append(variable)
        return Fluent(self.name, *new_variables)

    """
    The following "magic methods" just help make sure that Fluents work well with
    python's built-in functions. You can likely ignore them.
    """

    def __repr__(self):
        invocation = [self.name]
        invocation.extend(self.variables)
        return "Fluent" + str(tuple(invocation))
   
    def __str__(self):
        return self.name + str(self.variables)

    def __eq__(self, other_fluent):
        return str(self) == str(other_fluent)

    def __hash__(self):
        return hash(str(self))


class Action(object):
    """
    Represents an action schema in a planning problem.
    """
    def __init__(self, name, preconditions,
                 add_list, delete_list, *variables):
        """
        Takes a function name, a list of positive precondition fluents,
        an add list, a delete list, and 0 or mor variables, and creates
        an action schema with those values.
        """
        self.name = name
        self.preconditions = preconditions
        self.add_list = add_list
        self.delete_list = delete_list
        self.variables = list(variables)

    def bind(self, variable_mapping):
        """
        Takes a dictionary mapping variable names to new values, and returns a version
        of the fluent with those variables replaced with those values.
        """
        newAction = Action(self.name, self.preconditions, self.add_list,
                           self.delete_list, *self.variables)
        newAction.preconditions = [pp.bind(variable_mapping)
                              for pp in self.preconditions]
        newAction.add_list = [add.bind(variable_mapping) for
                         add in self.add_list]
        newAction.delete_list = [delete.bind(variable_mapping) for
                            delete in self.delete_list]
        newAction.variables = [self.bind_variable(variable, variable_mapping) for
                               variable in self.variables]
        return newAction

    def bind_variable(self, variable, variable_mapping):
        if variable in variable_mapping:
            return variable_mapping[variable]
        else:
            return variable

    def specify(self, *variables):
        """
        Takes a list of variables and binds those variables to the variables of the
        action in order. More user-friendly than calling bind directly because you
        don't have to worry about the variable names, just the order of the values.
        """
        
        if len(variables) == 1 and type(variables[0]) is not str:
            variables = variables[0]
        mapping = {}
        for var, obj in zip(self.variables, variables):
            mapping[var] = obj
        return self.bind(mapping)

    """
    The following "magic methods" just help make sure that States work well with
    python's built-in functions. You can likely ignore them.
    """

    def __str__(self):
        return self.name + str(self.variables)

    def __eq__(self, other_action):
        return str(self) == str(other_action)

    def __hash__(self):
        return hash(str(self))
      
      

class State(object):
    """
    Represents a state in a planning problem.
    """
    def __init__(self, fluent_set):
        """
        Takes a list (or tuple or set) of Fluents that hold in the state.
        Closed world assumption means all other Fluents do not hold.
        """
        self.fluent_set = set(fluent_set)

    def is_valid(self, action):
        """
        Given an action, checks to see if the preconditions of the action hold in
        the state.
        """
        for precondition in action.preconditions:
            if precondition not in self.fluent_set:
                return False
        return True

    def apply_action(self, action):
        """
        Given an action, returns the state resulting from performing that action in
        the state.
        """
        new_state = State(self.fluent_set)
        for fluent in action.delete_list:
            if fluent in new_state.fluent_set:
                new_state.fluent_set.remove(fluent)
        for fluent in action.add_list:
            new_state.fluent_set.add(fluent)
        return new_state

    """
    The following "magic methods" just help make sure that States work well with
    python's built-in functions. You can likely ignore them.
    """

    def __str__(self):
        return str(tuple([str(fluent) for fluent in self.fluent_set]))

    def __eq__(self, other_state):
        return self.fluent_set == other_state.fluent_set

    def __hash__(self):
        return hash(str(self))
               

class Backward_State(State):
    """
    Represents a state in a backward planning problem.
    """
    
    def __init__(self, fluent_set):
        """
        Takes a list (or tuple or set) of Fluents that hold in the state.
        Closed world assumption means all other Fluents do not hold.
        """
        State.__init__(self, fluent_set)

    def is_valid(self, action):
        """
        Given an action, checks to see if the addlist of the action exits in
        the state's fluent set.
        """
        for fluent in action.add_list:
            if fluent in self.fluent_set:
                return True
        return False

    def apply_action(self, action):
        """
        Given an action, returns the state resulting from performing that action in
        the state.
        """
        new_state = Backward_State(self.fluent_set)
        for fluent in action.add_list:
            if fluent in new_state.fluent_set:
                new_state.fluent_set.remove(fluent)
        for fluent in action.delete_list:
            new_state.fluent_set.add(fluent)
        return new_state



"""
The following three functions are syntactic sugar to make defining planning
problems a little more convenient.  You shouldn't need to understand or modify them.
"""

def make_fluent(fluent_string):
    fl_name = fluent_string.split("(")[0]
    fl_variables = fluent_string.split("(")[1].strip(")")
    fl_variables = [variable.strip() for variable in fl_variables.split(",")]
    return Fluent(fl_name, *fl_variables)

def make_action(name, preconditions, addlist, deletelist):
    ac_name = name.split("(")[0]
    ac_variables = name.split("(")[1].strip(")")
    ac_variables = [variable.strip() for variable in ac_variables.split(",")
                    if len(variable.strip()) > 0]
    preconditions = [make_fluent(precondition.strip()) for precondition
                     in preconditions.split(";")
                     if len(precondition.strip()) > 0]
    add_list = [make_fluent(add.strip()) for add in addlist.split(";")
                if len(add.strip()) > 0]
    delete_list = [make_fluent(delete.strip()) for delete
                   in deletelist.split(";") if len(delete.strip()) > 0]
    return Action(ac_name, preconditions, add_list, delete_list, *ac_variables)

def make_state(state_string):
    state_fluents = [make_fluent(fl_string.strip()) for fl_string
                     in state_string.split(";")]
    return State(state_fluents)


"""
Sample planning problem encoding using the functions above.  Problem is the flat-fixing
problem from the textbook.
"""
car_initial_state = make_state("""Tire(Flat);
                              Tire(Spare);
                              At(Flat,Axle);
                              At(Spare,Trunk)""")
car_goal_state = make_state("""At(Spare,Axle)""")
car_actions = {"Remove": make_action(name="Remove(obj,loc)",
                         preconditions="At(obj,loc)",
                         addlist="""At(obj,Ground);
                                 Clear(loc)""",
                         deletelist="At(obj,loc)"),
            "PutOn": make_action(name="PutOn(t,Axle)",
                                 preconditions="""Tire(t);
                                               At(t,Ground);
                                               Clear(Axle)""",
                                 addlist="At(t,Axle)",
                                 deletelist="At(t,Ground)"),
           "LeaveOvernight": make_action(name="LeaveOvernight()",
                                         preconditions="",
                                         addlist="""Clear(Axle);
                                                    Clear(Trunk)""",
                                         deletelist="""At(Spare,Ground);
                                                       At(Spare,Axle);
                                                       At(Spare,Trunk);
                                                       At(Flat,Ground);
                                                       At(Flat,Axle);
                                                       At(Flat,Trunk)""")}
car_object_list = ["Flat", "Spare", "Axle", "Ground", "Trunk"]


"""
To get the action Remove(Spare,Trunk), you would use the statement:
    rm_action = car_actions["Remove"].specify("Spare","Trunk")

To get the state that is produced when you perform this action in the initial state:
    rm_state = car_initial_state.apply_action(rm_action)
"""

#for test
#print car_actions.keys()
rm_action = car_actions["PutOn"].specify("Spare")
#print rm_action.__str__()
if car_initial_state.is_valid(rm_action):
    rm_state = car_initial_state.apply_action(rm_action)
    #print rm_state.__str__()


    
#definitions of the monkey/banana problem and the going-out problem go here

going_initial_state = make_state("""At(Agent,Home);
                                    Worn(LeftFoot, LeftSlipper);
                                    Worn(RightFoot, RightSlipper);
                                    Clear(Torso);
                                    FitOn(LeftFoot,LeftShoe);
                                    FitOn(RightFoot,RightShoe);
                                    FitOn(Torso,Sweater);
                                    FitOn(Torso,Jacket);
                                    FitOn(Torso,LightSportsJersey)""")

going_goal_state = make_state("""At(Agent,Outside)""")
								
going_actions = {"Remove": make_action(name="Remove(x,y)",
				       preconditions="Worn(x,y)",
                                       addlist="Clear(x)",
                                       deletelist="Worn(x,y)"),
				"PutOn": make_action(name="PutOn(x,y)",
                                                     preconditions="""Clear(x);FitOn(x,y)""",
                                                     addlist="Worn(x,y)",
                                                     deletelist="Clear(x)"),
				"GoOutside": make_action(name="GoOutside(Agent,x)",
                                                         preconditions="""Worn(Torso,x);
                                                                        Worn(LeftFoot,LeftShoe);
                                                                        Worn(RightFoot,RightShoe)""",
                                                         addlist="At(Agent,Outside)",
                                                         deletelist="At(Agent,Home)")}
going_object_list = ["Agent", "LeftFoot", "LeftShoe", "RightFoot", "RightShoe", "LeftSlipper", "RightSlipper", "Torso", "Sweater", "Jacket", "LightSportsJersey" ]

monkey_initial_state = make_state("""At(Monkey, A);
                                        At(Bananas, B);
                                        At(Box, C);
                                        Height(Monkey, Low);
                                        Height(Box, Low);
                                        Height(Bananas, High);
                                        Pushable(Box);
                                        Climbable(Box)""")

monkey_goal_state = make_state("""Have(Monkey, Bananas)""")

monkey_actions = {"Go": make_action(name="Go(x, y)",
                                    preconditions="At(Monkey, x)",
                                    addlist="At(Monkey, y)",
                                    deletelist="At(Monkey, x)"),
                  "Push": make_action(name="Push(b, x, y)",
                                      preconditions="""At(Monkey, x);
                                                         Pushable(b);
                                                         At(b, x);
                                                         Height(Monkey, Low);
                                                         Height(b, Low)""",
                                      addlist="""At(Monkey, y);
                                                   At(b, y)""",
                                      deletelist="""At(Monkey, x);
                                                      At(b, x)"""),
                  "ClimbUp": make_action(name="ClimbUp(Box, x)",
                                         preconditions="""At(Monkey, x);
                                                            At(Box, x);
                                                            At(Bananas, x);
                                                            Climbable(Box)""",
                                         addlist="""On(Monkey, Box);
                                                      Height(Monkey, High)""",
                                         deletelist="Height(Monkey, Low)"),
                  "Grasp": make_action(name="Grasp(Bananas, x)",
                                       preconditions="""Height(Monkey, High);
                                                          Height(Bananas, High);
                                                          At(Monkey, x);
                                                          At(Bananas, x)""",
                                       addlist="Have(Monkey, Bananas)",
                                       deletelist=""),
                  "ClimbDown": make_action(name="ClimbDown(Box)",
                                           preconditions="""On(Monkey, Box);
                                                              Height(Monkey, High)""",
                                           addlist="Height(Monkey, Low)",
                                           deletelist="""On(Monkey, Box);
                                                           Height(Monkey, High)"""),
                  "UnGrasp": make_action(name="UnGrasp(Bananas)",
                                         preconditions="Have(Monkey, Bananas)",
                                         addlist="",
                                         deletelist="Have(Monkey, Bananas)")}
monkey_object_list = ["A", "B", "C", "High", "Low", "Monkey", "Box", "Bananas"]

#mb_action = mb_actions["Push"].specify("A","B")
#print mb_action.__str__()

class Plan(object):
    """Define a Plan class for Partial Order Planning"""
    
    def __init__(self, init_state, goal_state, actions, object_list):
        """initial plan: initialize the plan with START and FINISH action
            and an open condition set with all the preconditions of FINISH action in it.
            here we represent the causal link as tuple(actionA,actionB,condition);
            order constraints actionA < actionB as (actionA,actionB);
            open precondition set as a dictionary {actionName: corresponding unsatisfied preconditions}."""
        self.success = True
        self.action_set = set()
        self.object_list = object_list
        self.actions = actions

        self.START = Action(name="START", preconditions=[], add_list=init_state.fluent_set, delete_list=[])
        self.action_set.add(self.START)

        self.FINISH = Action(name="FINISH", preconditions=goal_state.fluent_set, add_list=[], delete_list=[])
        self.action_set.add(self.FINISH)
        
        self.order_constraint_set = set()
        self.order_constraint_set.add((self.START, self.FINISH))
        #print self.order_constraint_set
        self.causal_link_set = set()
        self.open_precondition_set = {self.FINISH:set(self.FINISH.preconditions)}
        
    def transitive_closure(self, order_set):
        """return a transitive closure for the given order constraint set"""
        closure = set(order_set)
        #print closure
        while True:
            new_relations = set((x, w) for x, y in closure for q, w in closure if q == y)
            closure_until_now = closure | new_relations

            if closure_until_now == closure:
                break
            closure = closure_until_now

        return closure
    
    def add_clink(self, actionA, actionB, condition):
        """add a causal link tuple(actionA,actionB,condition) """
        self.causal_link_set.add((actionA, actionB, condition))
    
    def add_order_constraint(self, actionA, actionB):
        """add a order constraint actionA < actionB, if it forms a cycle then return False"""
        if (actionB, actionA) not in self.order_constraint_set:
            self.order_constraint_set.add((actionA, actionB))
            self.order_constraint_set = self.transitive_closure(self.order_constraint_set)
            return True
        else:
            return False
    def add_action(self, action):
        """add a new action in the plan's action set."""
        self.action_set.add(action)
    
    def add_open_precondition(self, action):
        """add an (unsatisfied) open precondition for the action."""
        self.open_precondition_set[action] = set(action.preconditions)
    
    def remove_open_precondition(self, action, condition):
        """remove an (unsatisfied) open precondition for the action."""
        self.open_precondition_set[action].remove(condition)
        
    def resolve_threats(self, actionA):
        """resolve the conflicts caused by the new action added.
        adding the order constraints by putting the possible conflictive actionA before the casual link or after it"""

        for clink in self.causal_link_set:
            if clink[2] in actionA.delete_list:
                #promote and demote
               if self.add_order_constraint(actionA, clink[0]) or self.add_order_constraint(clink[1], actionA):
                   continue
               else:
                   #fail
                   return False
        return True
    def resolve_threats_clink(self, clink):
        """resolve the conflicts caused by the new causal link added. Using the same rules with resolve_threats"""
        for action in list(self.action_set):
            if clink[2] in action.delete_list:
                if self.add_order_constraint(action, clink[0]) or self.add_order_constraint(clink[1], action):
                    continue
                else:
                    return False
        return True
        
    def assignments_generator(self, ac_variables):
        """generate the possible assignments for the list of variables given"""
        position = 0
        assigned_list = []
        assigned_num = 0
        #variable_list = list(ac_variables)
    
        for variable in ac_variables:
            if variable in self.object_list:
                assigned_list.append((variable, position))
                assigned_num += 1
            position += 1
            
        pools = map(tuple, (self.object_list,)) * (len(ac_variables) - assigned_num)
        result = [[]]
        for pool in pools:
            result = [x + [y] for x in result for y in pool]
        for prod in result:
            for assigned in assigned_list:
                prod.insert(assigned[1], assigned[0])
            yield tuple(prod)


    def choose_action(self, actionB):
        """choose action to satisfy the open precondition on actionB.
            return the corresponding plan and action if the plan is consistent."""
        condition_set = self.open_precondition_set[actionB]
        
        for condition in condition_set:
            for actionA in self.action_set:
                #if the action in the plan's action set has the condition as effect
                new_plan = copy.deepcopy(self)
                if condition in actionA.add_list:
                    new_plan.add_clink(actionA, actionB, condition)
                    if new_plan.add_order_constraint(actionA, actionB):
                        new_plan.add_open_precondition(actionA)
                        new_plan.remove_open_precondition(actionB, condition)
                        if new_plan.resolve_threats(actionA) and new_plan.resolve_threats_clink((actionA, actionB, condition)):
                            yield tuple((new_plan, actionA))
            
            for action_name in self.actions.keys():
                #print self.actions[action_name].variables
                for assignment in self.assignments_generator(self.actions[action_name].variables):
                    new_plan = copy.deepcopy(self)
                    actionA = self.actions[action_name].specify(assignment)
                    #if the new action has the condition as effect
                    if actionA not in new_plan.action_set and condition in actionA.add_list:
                        new_plan.add_clink(actionA, actionB, condition)
                        if new_plan.add_order_constraint(actionA, actionB) and new_plan.add_order_constraint(self.START, actionA) and new_plan.add_order_constraint(actionA, self.FINISH):
                            new_plan.add_open_precondition(actionA)
                            new_plan.add_action(actionA)
                            new_plan.remove_open_precondition(actionB, condition)
                            if new_plan.resolve_threats(actionA) and new_plan.resolve_threats_clink((actionA, actionB, condition)):
                                yield tuple((new_plan, actionA))

            #no action from the plan and no new action by instantiating an operator that has condition as an effect
            #self.choose_action(plan,actionB)
            pass

    def __str__(self):
        return "action_set:" + str([a.__str__() for a in self.action_set]) + "\n" \
                + "casual_link:" + str([(m.name, n.name, t.__str__()) for m, n, t in self.causal_link_set]) + "\n" \
                + "preconditions:" + str([(x.__str__(), self.open_precondition_set[x]) for x in self.open_precondition_set.keys()]) + "\n"\
                + "order_constraint_set:" + str([(str(x.name) + str(x.variables), str(y.name) + str(y.variables)) for x, y in self.order_constraint_set]) + "\n" \



class PlanningProblem(search.SearchProblem):
    """
    Defines a search problem for planning, as in the previous assignment.
    """

    def __init__(self, start_state, goal_state, actions, object_list):
        """
        A planning problem is defined by the start state, the goal state, and
        the actions that can be performed to get from one to the other. Because
        of the closed world assumption, a list of objects in the world is not
        strictly necessary, but you may find it convenient to have when implementing
        the necessary algorithms.
        """
        
        #Your code here!
        self.start_state = start_state
        self.goal_state = goal_state
        self.actions = actions
        self.object_list = object_list
        pass

    def getStartState(self):
        """
        Returns the start state for the search problem 
        """
        #Your code here!
        return self.start_state
        pass

    def isGoalState(self, state):
        """
        Returns True if and only if the state is a valid goal state
        """
        #Your code here!
        isGoal = self.goal_state.fluent_set.issubset(state.fluent_set)
        return isGoal
        #pass
#    def convert(self, action):
#        ac_variables = []
#        
#        for m in action.preconditions:
#            ac_variables += m.variables
#        for m in action.add_list:
#            ac_variables += m.variables
#        for m in action.delete_list:
#            ac_variables += m.variables
#
#        ac_variables += action.variables
#        return list(set(ac_variables))
    
    def assignments_generator(self, ac_variables):
        """to-do"""
        position = 0
        assigned_list = []
        assigned_num = 0
        variable_list = list(ac_variables)
	
        for variable in variable_list:
            if variable in self.object_list:
                assigned_list.append((variable, position))
                assigned_num += 1
            position += 1
        		
        pools = map(tuple, (self.object_list,)) * (len(ac_variables) - assigned_num)
        result = [[]]
        for pool in pools:
            result = [x + [y] for x in result for y in pool if y not in x]
        for prod in result:
            for assigned in assigned_list:
                prod.insert(assigned[1], assigned[0])
            #print prod
            yield tuple(prod)
        
    def getSuccessors(self, state):
        """
        For a given state, this should return a list of triples, 
        (successor, action, stepCost), where 'successor' is a 
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental 
        cost of expanding to that successor (always 1 for this assignment)
        """
        #Your code here!
        successors = []
        stepCost = 1
	#import itertools
        for action_name in self.actions.keys():
            #print self.actions[action_name].variables
            ac_variables = self.actions[action_name].variables
            for assignment in itertools.product(self.object_list, repeat=len(ac_variables)):
                action = self.actions[action_name].specify(assignment)
                if state.is_valid(action):
                    successor = state.apply_action(action)
                    #print action.__str__()
                    #print successor
                    successors.append((successor, action, 1))
        return successors
        #pass

class BackwardPlanningProblem(search.SearchProblem):
    """
    Defines a search problem starting from the goal and working backward
    to the start.
    """

    def __init__(self, start_state, goal_state, actions, object_list):
        #Your code here!
        pass
	self.start_state = start_state
	self.goal_state = goal_state
	self.actions = actions
	self.object_list = object_list

    def getStartState(self):
        """return the goal state as start state"""
        #Your code here!
	return Backward_State(self.goal_state.fluent_set)
        pass

    def isGoalState(self, state):
        """check if reach goal"""
        #Your code here!
        isGoal = state.fluent_set.issubset(self.start_state.fluent_set)
        #isGoal = self.start_state.fluent_set.issubset(state.fluent_set)
        return isGoal
    
#    def convert(self, action):
#        ac_variables = []
#        
#        for m in action.preconditions:
#            ac_variables += m.variables
#        for m in action.add_list:
#            ac_variables += m.variables
#        for m in action.delete_list:
#            ac_variables += m.variables
#
#        ac_variables += action.variables
#        return list(set(ac_variables))

    def assignments_generator(self, ac_variables):
        """to-do"""
        position = 0
        assigned_list = []
        assigned_num = 0
	    #variable_list = list(ac_variables)
	

        for variable in ac_variables:
            if variable in self.object_list:
                assigned_list.append((variable, position))
                assigned_num += 1
            position += 1
                
        pools = map(tuple, (self.object_list,)) * (len(ac_variables) - assigned_num)
        result = [[]]
        for pool in pools:
            result = [x + [y] for x in result for y in pool]
        for prod in result:
            for assigned in assigned_list:
                prod.insert(assigned[1], assigned[0])
            yield tuple(prod)


    def getSuccessors(self, state):
        """
        Relevant successors only, please!
        args:
             state -- Backward_State type
        return:
             list of tuples(Backward_State, action, Stepcost)
        """
        #Your code here!
	successors = []
	#assignment_list = []
	#for fluent in state.fluent_set:
	#	assignment_list = list(set(assignment_list)|set(fluent.variables))
	#assignment_list = list(set(assignment_list)&set(self.object_list))

 	for action_name in self.actions.keys():
            #print self.actions[action_name].variables
            ac_variables = self.actions[action_name].variables
            for assignment in itertools.product(self.object_list,repeat=len(ac_variables)):	
		action = self.actions[action_name].specify(assignment)	
                if state.is_valid(action):
                    #print action
                    new_state = state.apply_action(action)
                    successor = Backward_State(set(action.preconditions) | new_state.fluent_set)
                    successors.append((successor, action, 1))
        #for s in successors:
            #print s[0]
	return successors
        pass

        
    
class POPlanningProblem(search.SearchProblem):
    """
    Defines a search problem over partially ordered plans.
    """
    def __init__(self, start_state, goal_state, actions, object_list):
        #Your code here!
        self.start_plan = Plan(start_state, goal_state, actions, object_list)
        self.actions = actions
        self.object_list = object_list
        pass

    def getStartState(self):
        """
        Remember, this is a plan, not a world-state!
        """
        #Your code here!
        return self.start_plan
        pass

    def isGoalState(self, plan):
        #Your code here!
        for action in plan.open_precondition_set.keys():
            if len(plan.open_precondition_set[action]) != 0:
                return False
        return True
        pass

    def getSuccessors(self, plan):
        """
        In the (successor, action, stepcost) triple, the successor
        should be the new plan, the action should also be the new
        plan, and the stepcost should be 1. The stepcost does not make
        much sense, but that doesn't matter for the purposes of this assignment.
        """
        #Your code here!
        successors = []
        #new_plan = copy.deepcopy(plan)
        for actionB in plan.open_precondition_set.keys():
            for new_action in plan.choose_action(actionB):
                if _DEBUG == True: 
                    import pdb 
                    pdb.set_trace()
                successor_plan, actionA = new_action
                successors.append((successor_plan, successor_plan, 1))
                
        return successors
                                                     
#                                 
#print "forward flat fix \n"                                                  
#flat_fixing_problem = PlanningProblem(car_initial_state,car_goal_state,car_actions,car_object_list)
#solution = search.breadthFirstSearch(flat_fixing_problem)
#for action in solution:
#    print action


print "\n"                                 
print "Forward Monkey bananas problem\n"                         
monkey_banana_problem = PlanningProblem(monkey_initial_state,monkey_goal_state,monkey_actions,monkey_object_list)
solution = search.breadthFirstSearch(monkey_banana_problem)
for action in solution:
	print action
#
#print "\n"
#print "Backward flat fix problem\n"
#flat_fix_backward = BackwardPlanningProblem(car_initial_state,car_goal_state,car_actions,car_object_list)
#solution1 = search.breadthFirstSearch(flat_fix_backward)
##print solution1
#for action in solution1:
#	print action    


#monkey_banana_problem = BackwardPlanningProblem(monkey_initial_state,monkey_goal_state,monkey_actions,monkey_object_list)
#solution = search.breadthFirstSearch(monkey_banana_problem)
#for action in solution:
#	print action
#        
#print "\n"
#print "forward going \n"
#going_problem = PlanningProblem(going_initial_state,going_goal_state,going_actions,going_object_list)
#solution2 = search.breadthFirstSearch(going_problem)
#for ac in solution2:
#    print ac

#print "Partial ordering planning flat fix problem\n"
#flat_fix_pop = POPlanningProblem(car_initial_state, car_goal_state, car_actions, car_object_list)
#partial_plan = search.breadthFirstSearch(flat_fix_pop)
#for p in partial_plan:
#    print p


