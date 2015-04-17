import assign_games
import gameGraph

g=assign_games.AssignGame()

def compare_size(state):
	assign_games.childCount=0
	minimax = assign_games.minimax_decision(state,g)
	print "minimax children " + str(assign_games.childCount)
	assign_games.childCount=0
	alphabeta = assign_games.alphabeta_full_search(state,g)
	print "alphabeta children " + str(assign_games.childCount)

def run_alphabeta(n):
	while(n.matches>0):
		temp=assign_games.alphabeta_full_search(n,g)
		"""print state['player'] + " : " + str(temp) + " : " + str(state)"""
		n=g.result(n,temp,1)


def run_minimax(state):
	print "minimax MAX player staring first"
	while(state.matches > 0):
		temp=assign_games.minimax_decision(state,g)
		print state.player + " : " + str(state) + " : " + str(temp) 
		state=g.result(state,temp, 1)

	print "n = " + str(s) + " final state" + str(state)
	print "Winner :" + state.player

NoOfIterations=10.0

def perf_OO(n):
	gameValue = 0.0
	for i in range(int(NoOfIterations)):
		gameValue = gameValue + n.play_twoplayer(g, assign_games.minimax_player, assign_games.minimax_player)
	print "Game Value for two optimal players " + str(gameValue/NoOfIterations)

def perf_OO_AB(n):
	gameValue = 0.0
	for i in range(int(NoOfIterations)):
		gameValue = gameValue + n.play_twoplayer(g, assign_games.alphabeta_player, assign_games.alphabeta_player)
	print "Game Value for two alphabeta optimal players with n = " + str(n.matches) + " is " + str(gameValue/NoOfIterations)

def perf_OR(n):
	gameValue = 0.0
	print "start"
	for i in range(int(NoOfIterations)):
		print i
		gameValue = gameValue + assign_games.play_game(g, n, assign_games.alphabeta_player, assign_games.random_player)
		print gameValue
	print "done"
	print "Game Value for optimal player and random player with n = " + str(n.matches) + " is " + str(gameValue/NoOfIterations)

def perf_RO(n):
	gameValue = 0.0
	for i in range(int(NoOfIterations)):
		gameValue = gameValue + assign_games.play_game(g, n, assign_games.random_player, assign_games.alphabeta_player)
		print gameValue
	print "Game Value for random player and optimal player with n = " + str(n.matches) + " is " + str(gameValue/NoOfIterations)

def show_tree(n):
	print "Final Tree is "
	tree = assign_games.Tree(n)
	tree.printTree(n,g)

def moore_output(n):
	


	for child in n.children: 
		if (child.utility == 1):
			value = child.move
			mooreNode = assign_games.MooreState(value, n.move)
			'print "moore output " +str(mooreNode)'
			return mooreNode, child
	if n.children:
		mooreNode = assign_games.MooreState(1, n.move)
		return mooreNode, n.children[0]
	if n:
		mooreNode = assign_games.MooreState(100, n.move)
		return mooreNode, None		
	return None, None

def print_moore(startNode):
	"""print "Moore machine is """
	mooreNode = assign_games.MooreState(0,0)
	headMoore = mooreNode	
	mooreQueue = [{"node" : startNode, "parent" : mooreNode}]
	while len(mooreQueue):
		queueElement = mooreQueue.pop(0)
		mooreNode, newNode = moore_output(queueElement['node'])
		m = queueElement['parent']
		if mooreNode is not None:
			mooreNode.parent = m
			m.toStates = m.toStates + [mooreNode]
		"""print "children"
		print str(m)"""
		if newNode is not None:
			"""print str(newNode)"""
			for child in newNode.children:
				mooreQueue = mooreQueue + [{"node": child, "parent" : mooreNode}]
	return headMoore

def print_moore_second(startNode):
	mooreQueue = []
	mooreNode = assign_games.MooreState(0,0)
	headMoore = mooreNode	
	initialNode = assign_games.MooreState(0,0)
	mooreNode.toStates = mooreNode.toStates + [initialNode]
	for child in startNode.children:
		mooreQueue = mooreQueue + [{"node": child, "parent" : initialNode}]


	while len(mooreQueue):
		queueElement = mooreQueue.pop(0)
		mooreNode, newNode = moore_output(queueElement['node'])
		m = queueElement['parent']
		if mooreNode is not None:
			mooreNode.parent = m
			m.toStates = m.toStates + [mooreNode]
		if newNode is not None:
			for child in newNode.children:
				mooreQueue = mooreQueue + [{"node": child, "parent" : mooreNode}]
	return headMoore

				

while 1:
	try:
        	print "Choose 1-Minimax, 2-AlphaBeta, 3-Compare Size, 4-Performance, 5-MooreMachine"
        	options = raw_input('option > ')   # use input() on Python 3
        	s = raw_input('n > ')   # use input() on Python 3
    	except EOFError:
        	print
       		break
	s=int(s)
	temps=s
	
	n = assign_games.Node(s,0,'MAX',0,None)
	
	if options == "1":
		n.run_minimax(g);
		filename = "minimax" + str(s)
		gameGraph.printGraph(n,g, filename);
	if options == "2":
		run_alphabeta(n)
		filename = "alphabeta" + str(s)
		gameGraph.printGraph(n,g,filename);
	if options == "3":
		compare_size(n)
	if options == "4":
		perf_OO_AB(n)
		'perf_OR(n)'
		perf_RO(n)
	if options == "5":
		n.run_minimax(g);
		moore = print_moore(n)
		filename = "moore1_" + str(s)
		gameGraph.printMoore(moore, filename);
		moore = print_moore_second(n)
		filename = "moore2_" + str(s)
		gameGraph.printMoore(moore, filename);
		
	'compare_size(n)'
	"""run_alphabeta(n)
	run_minimax(n)"""
	"""perf_OO(n)
	perf_OO_AB(n)
	perf_OR(n)
	perf_RO(n)"""
	'perf_OO_AB(n)'
	'assign_games.alphabeta_full_search(n,g)'
	'gameGraph.printGraph(n,g);'
	'show_tree(n)'
	'perf_OO(n)'
	'show_tree(n)'
	"""moore = print_moore_second(n)
	gameGraph.printMoore(moore);"""
	



"""	s=temps
	print "minimax MIN player staring first"
	while(s):
		state=dict(matches=s, player='MIN', level=0, path=[s], move=0)
		while(state['matches']>0):
			temp=assign_games.minimax_decision(state,g)
			print state['player'] + " : " + str(state) + " : " + str(temp)
			state=g.result(state,temp, 1)

		print "n = " + str(s) + " final state" + str(state)
		print "Winner :" + state['player']
		s=s-1"""



