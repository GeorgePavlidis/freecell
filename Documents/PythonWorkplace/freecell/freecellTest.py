
#!  /usr/bin/python
"""""""""""""""""""""""""""""""""""""""""""""""""""
this program find the solution to the game FreeCell 
with algorithms:
	- Depth first search
    - Breadth first search
    - Best first search
    - A*
Input:
   -Searching method 
   -input file 

   -output file
"""""""""""""""""""""""""""""""""""""""""""""""""""
import sys
import copy
import time
from collections import deque
STACK_LENGTH=8
N=0
method={
'depth': 1,	# Constants denoting the four algorithms
'breadth': 2,
'best': 3,
'astar': 4
}

suit={
'D':1, #diamonds (red)
'C':2,#clubs (black)
'H':3, #hearts (red)
'S':4, # spades (black)
}
#####################
## DATA STRUCTURE ###
#####################
search_frontier=[] # front set
node_tree=[] # all the tree
visited=[] # close set
root=None
#####################


def readData(importFile):
	# In this Function we read the import file and create the root node
	with open(importFile,"r+") as import_file:
		stack=[]
		fr=[]
		f=[]
		global N
		for line in import_file:
			line=line[:len(line)-1]
			stack.append(line.split(' '))
			N=len(stack[len(stack)-1])+N
		for i in range(0,4):
			f.append(-1)
		N=int(N/4)
		global STACK_LENGTH
		STACK_LENGTH=len(stack)
		root=Node(None,stack,fr,f,0,None)
		search_frontier.append(root)
		node_tree.append(root)


def heuristic(node):
	m=0
	for i in node.foundation:
		m=m+i+1
	return N*4-m


def insert_frontier(node):
	for i in range(0,len(search_frontier)):
		if(node.heuristic<search_frontier[i].heuristic):
			search_frontier.insert(i,node)
			return True
	search_frontier.append(node)




# this  function check if this action can be realized 
#Input:
#   note : the current note from whch the function can take the tables and make the necessary checks
#   i : the card that you want to move come from freecell table or if i is list the card is at the i[len(i)-1] posision and come from stacks 
#   loc : the location in which you want to put the card
#        -[0:STACK_LENGTH-1] is one of the stacks
#        -STACK_LENGTH i the table of freecell
#        -STACK_LENGTH+1 of the table of foundation
#   
#Output:
#   True -- if can 
#   False --if cannot
#
############################################################
def canMove(node,i, loc):
	if type(i)==str:
		card=i
	else :
		card=i[len(i)-1]
	nub=int(card[1:])# the number of card
	cur_suit=suit.get(card[0])# the suit of card
	if loc==STACK_LENGTH:
		if len(node.FreeCells)<4:
			return True
		else:
			return False
	elif loc==STACK_LENGTH+1:
		for i in range (1,5):
			if cur_suit==i:
				if node.foundation[i-1]+1==nub:
					return True
				else:
					return False
	else:
		if node.stack[loc]==[]:
			if type(i)==str:
				return False
			elif len(i)==1:
				return False
			return True
		if (not suit.get(node.stack[loc][len(node.stack[loc])-1][0])%2==cur_suit%2) and int(node.stack[loc][len(node.stack[loc])-1][1:])-1==nub:
			return True
		else:
			return False

class Node():
	def __init__(self,parent,stack,FreeCells,foundation,depth,move):
		self.children=0
		self.parent =parent 
		self.stack=stack#[size=[8], type String
		self.FreeCells=FreeCells #list with free cards size=[4], type String
		self.foundation=foundation # the final position of cards size=[4],type int
		self.depth=depth
		self.move=move# the difference between this node and its parent --the movement that brought us here--
		self.heuristic=0
	
	def __repr__(self):
		if(self.move==None):
			return 'None'
		string=(self.move +' d: '+ str(self.depth)+ ' h: '+ str(self.heuristic))
		return string
 

###\
# [0:STACK_LENGTH-1] put card to one of the stacks
# STACK_LENGTH+1 put card to foundation
# STACK_LENGTH put card to freecell
	def make_children(self, method):
		self.children=0
		for i in self.FreeCells:
			for j in range(0,STACK_LENGTH+2):
				if j==STACK_LENGTH:
					continue
				if canMove(self,i,j):
					newStack=copy.deepcopy(self.stack)
					newFreeCell=self.FreeCells[:]
					newFoundation=self.foundation[:]
					card=i
					newFreeCell.remove(card)
					if j==STACK_LENGTH+1:
						move='foundation '+ card
						newFoundation[suit.get(card[0])-1]=int(card[1:])
					else:
						if(newStack[j]==[]):
							move='newstack '+ card
						else:
							move='Stack '+ card +' '+ newStack[j][len(newStack[j])-1]
						newStack[j].append(card)
					newNode=Node(self,newStack,newFreeCell,newFoundation,self.depth+1,move)
					self.children+=1
					newNode.heuristic=heuristic(newNode)
					if(method==3 or method==4):
						if(method==4):
							newNode.heuristic=newNode.depth+newNode.heuristic
						insert_frontier(newNode)
					elif(method==1 or method==2):
						search_frontier.append(newNode)					


		for i in self.stack:
			if i==[]:
				continue
			for j in range(0,STACK_LENGTH+2):
				if canMove(self,i,j):
					newStack=copy.deepcopy(self.stack)
					newFreeCell=self.FreeCells[:]
					newFoundation=self.foundation[:]
					card=newStack[newStack.index(i)].pop()
					if j==STACK_LENGTH:
						move='freecell '+ card
						newFreeCell.append(card)
					elif j==STACK_LENGTH+1:
						move='foundation '+ card
						newFoundation[suit.get(card[0])-1]=int(card[1:])
					else:
						if(newStack[j]==[]):
							move='newstack '+ card
						else:
							move='Stack '+ card +' '+ newStack[j][len(newStack[j])-1]
						newStack[j].append(card)
					newNode=Node(self,newStack,newFreeCell,newFoundation,self.depth+1,move)
					self.children+=1
					newNode.heuristic=heuristic(newNode)
					if(method==3 or method==4):
						if(method==4):
							newNode.heuristic=newNode.depth+newNode.heuristic
						insert_frontier(newNode)
					elif(method==1 or method==2):
						search_frontier.append(newNode)					

	# this function check if this node is same with some privious nodes
	# and return true, otherwise return false
	#--------------------------------------
	#the function compare the last item of all stacks , the freecells table and the foundation
	#of this node with all privious
	def check_parents(self):
		for node in  visited:
			a=True
			a=self.foundation==node.foundation
			c=True
			c=self.FreeCells==node.FreeCells

			b=True
			for i in range(0,STACK_LENGTH):
				if(len(node.stack[i])==len(self.stack[i])):
					if(not node.stack[i]==[]):
						b=node.stack[i][len(node.stack[i])-1]==self.stack[i][len(self.stack[i])-1]
				else:
					b=False
					break
				
			if ( a and b and c):
#				print("helllloooooo!!!!!")
#				inp=input("Press Enter to check.")
#				if(inp=='d'):
#					node.toString()
#					print('--------------------------------')
#					self.toString()
#					print(len(node.FreeCells),' =',len(node.FreeCells)==len(self.FreeCells),'= ',len(self.FreeCells) )
#					inp=input("Press Enter to check.")
				return True
		return False

	# function to print all stuff about this node
	def toString(self):
		print('parent: ', self.parent)
		print('move :', self.move)
		print('depth: ', self.depth)
		print('total children: ', self.children)
		print("stacks:")
		for i in self.stack:
			print(i)
		print('FreeCells: ', self.FreeCells)
		print('Foundation: ',self.foundation)



def check_success(foundation):
	for i in foundation:
		if(not i==N-1):
			return False
	return True

def Solution(node):
	path=[]
	child=node
	while(not child.parent==None):
		path.append(child.move)
		child=child.parent
	else:
		path.append(child.parent)
	path.reverse()
	return path

def ExportFile(exportF,path):
	export_file=open(exportF,"w")
	export_file.write(str(len(path)-1)+'\n')
	for i in path[1:]:
		export_file.write(str(i)+'\n')
	export_file.close()

def Search(method):
	currentState=search_frontier[0]
	start_time = time.time()
	search_frontier.remove(currentState)
	while not check_success(currentState.foundation):
		if(not currentState.check_parents()):
			currentState.make_children(method)
			debug(0,currentState)
			visited.append(currentState)
		if(not search_frontier==[]):
			if(method==1): #DFS
				currentState=search_frontier.pop()	
			elif(method==2 or method==3 or method==4): #BFS or BestFS or Astar
				currentState=search_frontier[0]
				search_frontier.remove(currentState)
			print('s_f: ', len(search_frontier),' v:', len(visited) ,'|', currentState,'| time:',  time.time() - start_time)
			#debug(1, currentState)	
		else:
			return 'error'
	else:
		print('total time: ', time.time() - start_time)
		return Solution(currentState)


# this function help to debug the program
def debug(i,currentState):
	if(i==0):
		print(currentState)
		inp=input("Press Enter to terminate.")
		if(inp=='d'):
			currentState.toString()
			input("Press Enter to terminate.")
	elif i==1:
		if(len(currentState.depth)==28):
			inp=input("Press Enter to terminate.")
			if(inp=='d'):
				currentState.toString()
				print(currentState.check_parents())
				input("Press Enter to terminate.")



try:
	if not len(sys.argv)==4 :
		raise IndexError
	method=method.get(sys.argv[1])
	if(method==None):
		raise IndexError
	importF=sys.argv[2]
	exportF=sys.argv[3]
	readData(importF)
except IndexError:
	print ("freecell <method> <input-file> <output-file>")
	print ("where:\n ")
	print ("<method> = breadth|depth|best|astar")
	print ("<input-file> is a file containing a Nx4 cards randomly")
	print ("putting on ",STACK_LENGTH," rows and represent a random deal of cards in the game FreeCell .")
	print ("<output-file> is the file where the solution will be written.\n")
	sys.exit(2)
except FileNotFoundError:
	print  ('No such file or directory:',importF)
	sys.exit(2)

print(method)
path=Search(method)
print(path)
ExportFile(exportF, path)

# i=0
# start_time = time.time()
# elapsed_time=0
# while(i<1000):
# 	node_tree[00].make_children(method)
# 	if(i%100==0):
# 		print(i,node_tree[0].children, time.time() - start_time)
# 	i+=1
# elapsed_time = time.time() - start_time
# print('total nodes: ', len(node_tree),'and time :',elapsed_time)

