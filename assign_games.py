"""Games, or Adversarial Search. (Chapter 5)
"""

from utils import *
import random
import sys
import gameGraph
#______________________________________________________________________________
# Minimax Search

childCount=0

def minimax_decision(state, game):
	"""Given a state in a game, calculate the best move by searching
	forward all the way to the terminal states. [Fig. 5.3]"""
	player = game.to_move(state)
    
	def max_value(state):
		"""print "in maxval"""
		if game.terminal_test(state):
			"""print "it is terminal"""
			state.utility = game.utility(state, player)
			return state.utility
		v = -infinity
		"""print "for state " + str(state.matches) + "  " + str(game.actions(state))"""
		for a in game.actions(state):
			"""print "calling result"""
			child = game.result(state, a, 0)
			"""print "state : " + str(state.matches) +" action : " + str(a) + " gives : " + str(child.matches)"""
			x = min_value(child)
			v = max(v, x)
		"""print "max utility of " + str(state) + str(v)"""
		state.utility = v
		"""print "Utility for" + str(state) +" is " + str(state.utility)"""
		return v

	def min_value(state):
		"""print "in minval"""
		if game.terminal_test(state):
			"""print "it is terminal"""
			state.utility = game.utility(state, player)
			return state.utility

		v = infinity
		"""print "for state " + str(state.matches) + " " + str(game.actions(state))"""
		for a in game.actions(state):
			"""print "calling result min"""
			child = game.result(state, a, 0)
			"""print "state : " + str(state.matches) +" action : " + str(a) + " gives : " + str(child.matches)"""
			x = max_value(child)
			v = min(v, x)      
		"""print "min utility of " + str(state) + str(v)"""
		state.utility = v
		"""print "Utility for" + str(state) +" is " + str(state.utility)"""
		return v

	# Body of minimax_decision:
	if( state.player == 'MAX'):
		return argmax(game.actions(state),
                  lambda a: min_value(game.result(state, a, 0)))

    #When MIN player starts first
	if( state.player == 'MIN'):
		return argmin(game.actions(state),
                  lambda a: max_value(game.result(state, a, 0)))


#______________________________________________________________________________

def alphabeta_full_search(state, game):

	player = game.to_move(state)

	def max_value(state, alpha, beta):
		if game.terminal_test(state):
			state.utility = game.utility(state, player) 
			return state.utility
		v = -infinity
		for a in game.actions(state):
			child = game.result(state, a, 0)
			x = min_value(child, alpha, beta)
			v = max(v, x)
			'print " v = " + str(v) + " beta = " + str(beta)'
			if v >= beta:
				"""print "*************pruned*********** max" + str(child)"""
				state.utility = v				
				return v
			alpha = max(alpha, v)
			"""print "alpha : " + str(alpha)"""
		state.utility = v
		return v

	def min_value(state, alpha, beta):
		if game.terminal_test(state):
			state.utility = game.utility(state, player) 
			return state.utility
		v = infinity
		for a in game.actions(state):
			child = game.result(state, a, 0)
			x = max_value(child,alpha,beta)
			v = min(v, x)
			"""print " v = " + str(v) + " alpha = " + str(alpha)"""
			if v <= alpha:
				"""print "*************pruned*********** min" + str(child)"""
				state.utility = v				
				return v
			beta = min(beta, v)
		state.utility = v
		return v


    # Body of alphabeta_search:
	if( state.player == 'MAX'):
		return argmax(game.actions(state),
                  lambda a: min_value(game.result(state, a, 0),
                                      -infinity, infinity))


	if( state.player == 'MIN'):
		return argmin(game.actions(state),
                  lambda a: max_value(game.result(state, a, 0),
                                      -infinity, infinity))


def alphabeta_full_search1(state, game):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Fig. 5.7], this version searches all the way to the leaves."""

    player = game.to_move(state)

    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a, 0), alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a, 0), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search:
    return argmax(game.actions(state),
                  lambda a: min_value(game.result(state, a, 0),
                                      -infinity, infinity))


def alphabeta_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a, 0),
                                 alpha, beta, depth+1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a, 0),
                                 alpha, beta, depth+1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state,depth: depth>d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    return argmax(game.actions(state),
                  lambda a: min_value(game.result(state, a, 0),
                                      -infinity, infinity, 0))

#______________________________________________________________________________
# Players for Games

def query_player(game, state):
    "Make a move by querying standard input."
    game.display(state)
    return num_or_str(raw_input('Your move? '))

def random_player(game, state):
    "A player that chooses a legal move at random."
    return random.choice(game.actions(state))

def alphabeta_player(game, state):
    return alphabeta_full_search(state, game)

def minimax_player(game,state):
    return minimax_decision(state,game)

def play_game(game, startState, *players):
    """Play an n-person, move-alternating game.
    >>> play_game(Fig52Game(), alphabeta_player, alphabeta_player)
    3
    """
    state = startState
    while True:
        for player in players:
            move = player(game, state)
            """print "player : " + state.player+ "move :" + str(move)"""
            state = game.result(state, move,0)
            state.chosen = 1
            if game.terminal_test(state):
				return game.utility(state, game.to_move(startState))


#______________________________________________________________________________
# Some Sample Games

class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def actions(self, state):
        "Return a list of the allowable moves at this point."
        abstract

    def result(self, state, move):
        "Return the state that results from making a move from a state."
        abstract

    def utility(self, state, player):
        "Return the value of this final state to player."
        abstract

    def terminal_test(self, state):
        "Return True if this is a final state for the game."
        return not self.actions(state)

    def to_move(self, state):
        "Return the player whose move it is in this state."
        return state.to_move

    def display(self, state):
        "Print or otherwise display the state."
        print state

    def __repr__(self):
        return '<%s>' % self.__class__.__name__


def pretty_print(oldstate, newstate, c):
	if c==-1:
		return
	oldstateStr = "C_" + str(oldstate['matches']) + "_" + str(oldstate['level']) + "_" + str(oldstate['path'][0]) + "_" + str(oldstate['move'])
	newstateStr = "C_" + str(newstate['matches']) + "_" + str(newstate['level']) + "_" + str(newstate['path'][0]) + "_" + str(newstate['move'])
	if c==1:
		print oldstateStr + "[label = " + str(oldstate['matches']) + ", style = \"filled\", fillcolor=\"green\"]"
		print newstateStr + "[label = " + str(newstate['matches']) + ", style = \"filled\", fillcolor=\"green\"]"	
	else:
		print oldstateStr + "[label = " + str(oldstate['matches']) + "]"
		print newstateStr + "[label = " + str(newstate['matches']) + "]"	
		print oldstateStr + " -- " + newstateStr + "[label = " + str(newstate['move']) + "]"


class AssignGame(Game):

    def actions(self, state):
	"""return 3 states.. -1...x(if state -x>=0)"""
	valid_actions=[]
	count=1
	temp=state.matches

	while ((state.matches-count)>=0 and count<=3):
		valid_actions=valid_actions+[count]
		count = count +1
	"""print "valid actions are "+ str(valid_actions)"""
	'valid_actions.reverse()'
	return valid_actions
        
    def result(self, state, move, c):
		global childCount
		'print "state is " + str(state)'
		if state.player is 'MAX': 
			player = 'MIN'
		else:
			player = 'MAX'
		
		newpath = state.path + [(state.matches-move)]
		parent = state
		newstate = Node((state.matches - move), state.level + 1, player, move, parent)
		childCount = childCount + 1
		"""print "children were "
		for child in state.children:
			print "child " + str(child)"""
		if c==0:
			state.children = state.children + [newstate]
		if c==1:		
			newstate.chosen=1
		"""print "children are "
		for child in state.children:
			print "child " + str(child)"""

		return newstate

    def utility(self, state, player):
	"""+1 if MAX is 0, -1 if MIN is 0"""
        if state.player == 'MAX':
            return +1
        else:
            return -1


    def terminal_test(self, state):
	"""leaf node, thats is state is zero"""
	if(state.matches == 0):
        	return True
	else:
		return False

    def to_move(self, state):
	if(state.player is 'MAX'):
		return 'MAX'
	else:
		return 'MIN'


class Fig52Game(Game):
    """The game represented in [Fig. 5.2]. Serves as a simple test case.
    >>> g = Fig52Game()
    >>> minimax_decision('A', g)
    'a1'
    >>> alphabeta_full_search('A', g)
    'a1'
    >>> alphabeta_search('A', g)
    'a1'
    """
    succs = dict(A=dict(a1='B', a2='C', a3='D'),
                 B=dict(b1='B1', b2='B2', b3='B3'),
                 C=dict(c1='C1', c2='C2', c3='C3'),
                 D=dict(d1='D1', d2='D2', d3='D3'))
    utils = Dict(B1=3, B2=12, B3=8, C1=2, C2=4, C3=6, D1=14, D2=5, D3=2)
    initial = 'A'

    def actions(self, state):
        return self.succs.get(state, {}).keys()

    def result(self, state, move):
        return self.succs[state][move]

    def utility(self, state, player):
        if player == 'MAX':
            return self.utils[state]
        else:
            return -self.utils[state]

    def terminal_test(self, state):
        return state not in ('A', 'B', 'C', 'D')

    def to_move(self, state):
        return if_(state in 'BCD', 'MIN', 'MAX')

class TicTacToe(Game):
    """Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""
    def __init__(self, h=3, v=3, k=3):
        update(self, h=h, v=v, k=k)
        moves = [(x, y) for x in range(1, h+1)
                 for y in range(1, v+1)]
        self.initial = Struct(to_move='X', utility=0, board={}, moves=moves)

    def actions(self, state):
        "Legal moves are any square not yet taken."
        return state.moves

    def result(self, state, move):
        if move not in state.moves:
            return state # Illegal move has no effect
        board = state.board.copy(); board[move] = state.to_move
        moves = list(state.moves); moves.remove(move)
        return Struct(to_move=if_(state.to_move == 'X', 'O', 'X'),
                      utility=self.compute_utility(board, move, state.to_move),
                      board=board, moves=moves)

    def utility(self, state, player):
        "Return the value to player; 1 for win, -1 for loss, 0 otherwise."
        return if_(player == 'X', state.utility, -state.utility)

    def terminal_test(self, state):
        "A state is terminal if it is won or there are no empty squares."
        return state.utility != 0 or len(state.moves) == 0

    def display(self, state):
        board = state.board
        for x in range(1, self.h+1):
            for y in range(1, self.v+1):
                print board.get((x, y), '.'),
            print

    def compute_utility(self, board, move, player):
        "If X wins with this move, return 1; if O return -1; else return 0."
        if (self.k_in_row(board, move, player, (0, 1)) or
            self.k_in_row(board, move, player, (1, 0)) or
            self.k_in_row(board, move, player, (1, -1)) or
            self.k_in_row(board, move, player, (1, 1))):
            return if_(player == 'X', +1, -1)
        else:
            return 0

    def k_in_row(self, board, move, player, (delta_x, delta_y)):
        "Return true if there is a line through move on board for player."
        x, y = move
        n = 0 # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1 # Because we counted move itself twice
        return n >= self.k

class ConnectFour(TicTacToe):
    """A TicTacToe-like game in which you can only make a move on the bottom
    row, or in a square directly above an occupied square.  Traditionally
    played on a 7x6 board and requiring 4 in a row."""

    def __init__(self, h=7, v=6, k=4):
        TicTacToe.__init__(self, h, v, k)

    def actions(self, state):
        return [(x, y) for (x, y) in state.moves
                if y == 0 or (x, y-1) in state.board]

__doc__ += random_tests("""
>>> play_game(Fig52Game(), random_player, random_player)
6
>>> play_game(TicTacToe(), random_player, random_player)
0
""")



class Node:
	"""Node of the game tree"""

	def __init__(self, matches, level, player, move, parent=None):
		self.matches = matches
		self.level = level
		self.player = player
		self.move = move
		self.path = [matches]
		self.parent = parent
		self.utility = 1000
		self.children = []
		self.chosen = 0

	def __str__(self):
		return "[matches : " + str(self.matches) + ", level = " + str(self.level) + ", utility =" + str(self.utility) + ", player = " + self.player + ", move = " + str(self.move) + ", chosen = " + str(self.chosen) + ", path = " + str(self.path) + ", parent = " + str(self.parent) + "]"

	def updateChosen(self):
		self.chosen=1

	def generateChildren(self, game):
		return [game.result(self, a, 0)
                for a in game.actions(self)]
	
	def run_minimax(self,g):
		'print "minimax MAX player staring first"'
		state = self
		'temp=minimax_decision(state,g)'
		while(state.matches > 0):
			temp=minimax_decision(state,g)
			'print state.player + " : " + str(state) + " : " + str(temp)' 
			state=g.result(state,temp, 1)
			'print "Chosen is " + str(state.chosen)'


	def play_twoplayer(self, game, *players):
   
		startState = self
		state = startState
		while True:
		    for player in players:
		        move = player(game, state)
		        """print "player : " + state.player+ "move :" + str(move)"""
		        state = game.result(state, move, 1)
		        state.updateChosen()
		        'print "Chosen is " + str(state) + " " +str(state.chosen)'				
		        if game.terminal_test(state):
					return game.utility(state, game.to_move(startState))

class Tree:

	def __init__(self, initialNode):
		self.initialNode = initialNode

	def generateTree(self, n, g):
		if g.terminal_test(n) == True:
			return
		else:
			for child in n.generateChildren(g):
				print str(child)
				self.generateTree(child,g)
		
	def printTree(self,n,g):
		if g.terminal_test(n) == True:
			"""print "terminal"""
			return
		else:
			for child in n.children:
				print str(child)
				self.printTree(child,g)
		


class MooreState:

	def __init__(self, value, inputValue=0):
		self.inputValue = inputValue
		self.value = value
		self.toStates = []
		self.parent = 0

	def __str__(self):
		return "Value = " + str(self.value) + "Input = " + str(self.inputValue) + "ToStates = " + str(self.toStates)

	

		
