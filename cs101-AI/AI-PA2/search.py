# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util
_DEBUG=False 
class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first
  [2nd Edition: p 75, 3rd Edition: p 87]
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm 
  [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"
  #print "Start:", problem.getStartState()
  #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  #print "Start's successors:", problem.getSuccessors(problem.getStartState())

  startState = problem.getStartState()
  frontier = util.Stack()
  frontier.push(startState)
  explored_set = []
  solution = {}
  solution[startState]=[]
  while frontier.isEmpty() == False:
	current = frontier.pop()
	#isGoal test
	if problem.isGoalState(current):
		return solution[current]
	#add to the explored set	
	explored_set.append(current)
	#record path
	successors = problem.getSuccessors(current)
	for i in range(0,len(successors)):	
		child_state = successors[i][0]
		child_action = successors[i][1]
		solution[child_state] = solution[current][:]
		solution[child_state].append(child_action)
		if child_state not in explored_set and child_state not in frontier.list:
			if problem.isGoalState(child_state):
				return solution[child_state]
			frontier.push(child_state)

  util.raiseNotDefined()

def breadthFirstSearch(problem):
  """
  Search the shallowest nodes in the search tree first.
  [2nd Edition: p 73, 3rd Edition: p 82]
  """
  "*** YOUR CODE HERE ***"
  startState = problem.getStartState()
  if problem.isGoalState(startState):
  	return []
  frontier = util.Queue()
  frontier.push(startState)
  path = util.Queue()
  explored_set = []
  solution = {}
  solution[startState]=list()
  while frontier.isEmpty() == False:
  	current = frontier.pop()
        #print current
	explored_set.append(current)
	successor = problem.getSuccessors(current)
	for i in range(0,len(successor)):
		child_state = successor[i][0]
		child_action = successor[i][1]
		solution[child_state] = solution[current][:]
		solution[child_state].append(child_action)
		if child_state not in explored_set and child_state not in frontier.list:
			if problem.isGoalState(child_state):
				return solution[child_state]
			frontier.push(child_state)
#  util.raiseNotDefined()
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  if _DEBUG == True: 
  	import pdb 
        pdb.set_trace() 
  startState = problem.getStartState()
  frontier = util.PriorityQueue()
  frontier.push(startState,0)
  explored_set = []
  solution = {}
  solution[startState]=list()
  while frontier.isEmpty() == False:
  	current = frontier.pop()
	if problem.isGoalState(current):
		return solution[current]
	if current in explored_set:
		continue
	explored_set.append(current)
	successors = problem.getSuccessors(current)
	#print successors
	#suc_pos = [p[0] for p in successors]
	for i in range(0,len(successors)):
		path = solution[current][:]
		path.append(successors[i][1])
		if (successors[i][0] not in explored_set) and (successors[i][0] not in frontier.heap):
			solution[successors[i][0]] = path
			frontier.push(successors[i][0],problem.getCostOfActions(solution[successors[i][0]]))
		elif successors[i][0] in frontier.heap:	
			cost = problem.getCostofActions(path)
			if cost < problem.getCostofActions(solution[successors[i][0]]):				
				solution[successors[i][0]]=path
				frontier.push(successors[i][0],cost)
  util.raiseNotDefined()

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  startState = problem.getStartState()
  frontier = util.PriorityQueue()
  frontier.push(startState,heuristic(startState,problem))
  explored_set = []
  solution = {}
  solution[startState]=list()
  cost={}
  path = []
  cost[startState]=0
  while frontier.isEmpty() == False:
  	current = frontier.pop()
	if problem.isGoalState(current):
		return solution[current]
	if current in explored_set:
		continue
	explored_set.append(current)
	successors = problem.getSuccessors(current)
	#print successors
	#suc_pos = [p[0] for p in successors]

	h_cost = heuristic(current,problem)
	for successor in successors:
		child_state = successor[0]
		child_action = successor[1]
		child_cost = successor[2]
		
		path = solution[current][:]
		path.append(child_action)
		cost_cur = cost[current] + child_cost
		if _DEBUG == True: 
  			import pdb 
        		pdb.set_trace() 
		#consistent check
		new_h_cost = heuristic(child_state,problem)
		if h_cost - new_h_cost > successor[2]:
       			print "consistency problem", h_cost, new_h_cost, successor[0]
		if (child_state not in explored_set) and (child_state not in frontier.heap):
			solution[child_state] = path
			cost[child_state] = cost_cur
			f_cost_cur = cost[child_state]+ heuristic(child_state,problem)
			frontier.push(child_state,f_cost_cur)
		elif child_state in frontier.heap:	
			f_cost_cur = cost_cur + heuristic(child_state,problem)
			f_cost_old = cost[child_state] + heuristic(child_state,problem)
			if f_cost_cur < f_cost_old:				
				solution[child_state]=path
				frontier.push(child_state,f_cost_cur)
  #util.raiseNotDefined()
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
