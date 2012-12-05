"""
 Data structures useful for implementing Algorithm
"""

class Stack:
  "A container with a last-in-first-out (LIFO) queuing policy."
  def __init__(self,seq):
    self.list = seq
    
  def push(self,item):
    "Push 'item' onto the stack"
    self.list.append(item)

  def pop(self):
    "Pop the most recently pushed item from the stack"
    return self.list.pop()

  def isEmpty(self):
    "Returns true if the stack is empty"
    return len(self.list) == 0
    
class Buffer:
	"""A queue which always pop out the first element"""
	def __init__(self, seq):
		self.list = seq
	
	def pop():
		self.list.remove(self.list[0])
	
	def isEmpty(self):
		return len(self.list) == 0
		
		
	def __eq__(self,other_stack):
		return self.list == other_stack.list