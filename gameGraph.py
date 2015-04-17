
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

__author__ = """Aric Hagberg (hagberg@lanl.gov)"""

import pygraphviz as pgv

"""A=pgv.AGraph()

A.add_node("matches : 2, level = 0, utility =1000, player = MAX, move = 0, path = [2], parent = None")
n=A.get_node("matches : 2, level = 0, utility =1000, player = MAX, move = 0, path = [2], parent = None");
n.attr['label']='2'
A.add_edge("matches : 2, level = 0, utility =1000, player = MAX, move = 0, path = [2], parent = None","matches : 1, level = 1, utility =1, player = MIN, move = 1, path = [1], parent = [matches : 2, level = 0, utility =1000, player = MAX, move = 0, path = [2], parent = None]")
A.add_edge(1,0)
A.add_edge(2,0)


print(A.string()) # print to screen
print("Wrote simple.dot")
A.write('simple.dot') # write to simple.dot

B=pgv.AGraph('simple.dot') # create a new graph from file
B.layout() # layout with default (neato)
B.draw('simple.png') # draw png
print("Wrote simple.png")"""



def printGraph(startnode,g, filename):

	filedot = filename + ".dot"
	fileps = filename + ".png"
	nodeQueue=[]
	A=pgv.AGraph(strict=False,directed=True)
	nodeQueue = nodeQueue + [startnode]	
	
	while len(nodeQueue):
		node = nodeQueue.pop(0)
		if node.level == 6:
			break
		for child in node.children:
			nodeQueue = nodeQueue + [child]
		if node.level >= 1:
			A.add_edge(str(node.parent), str(node))	
			e=A.get_edge(str(node.parent), str(node))
			e.attr['label'] = str(node.move)
		A.add_node(str(node))
		n = A.get_node(str(node))
		if node.level == 0:
			n.attr['label'] = str(node.matches) 
		else:
			n.attr['label'] = str(node.matches) + "/" + str(node.utility)
		if node.chosen == 1:
			n.attr['style'] = 'filled'
			n.attr['fillcolor'] = 'green'
			
	A.write(filedot) # write to simple.dot

	B=pgv.AGraph(filedot) # create a new graph from file
	B.layout(prog='dot') # layout with default (neato)
	B.draw(fileps) # draw png
	print("Wrote to ps file")
	





def printMoore(headMoore,filename):
	
	filedot = filename + ".dot"
	fileps = filename + ".png"
	nodeQueue=[]
	A=pgv.AGraph(directed=True)
	nodeQueue = nodeQueue + [headMoore]	
	
	while len(nodeQueue):
		node = nodeQueue.pop(0)
		for child in node.toStates:
			nodeQueue = nodeQueue + [child]
			if node is not headMoore:
				A.add_edge(str(node), str(child))	
				e=A.get_edge(str(node), str(child))
				e.attr['label'] = str(child.inputValue)
			A.add_node(str(child))
			n = A.get_node(str(child))
			if child.value == 100:
				n.attr['label'] = "WIN"
			else:
				n.attr['label'] = str(child.value)			
	

	A.write(filedot) # write to simple.dot

	B=pgv.AGraph(filedot) # create a new graph from file
	B.layout(prog='dot') # layout with default (neato)
	B.draw(fileps) # draw png
	print("Wrote to ps file")
	

	


