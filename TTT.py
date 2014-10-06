"""
A KevPaDa module for running real-valued and discrete-valued bidding Tic-Tac-Toe.

(c) 2013 Kevin Chen, Patrick Johnson, David Moon

"""

import math
import sys
import copy
import time

X='X'
O='O'
BLANK=' '

PURPLE = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'

DEBUG=True
def debug(string):
	""" A test/debugging method for printing. """
	if DEBUG: 
		print RED + string + ENDC

def green(string):
	print GREEN + string + ENDC

def flush():
	"""	The conventional ANSI method for clearing the terminal. """
	print chr(27) + "[2J"

def partitionByDistance():
	"""
	This method assumes that a file 'TTTLegalStates.txt' exists and contains
	all legal states, where each line contains two comma-delimited tokens and
	where the binary form of each token represents the state of a player's
	pieces on the board. The tokens are encoded in decimal as: x,o
	
	Suppose x is 111000000 and
	suppose o is 000110110. Then the bitwise OR of 
	the two is:  111110110.
	
	Since the bitwise OR of x and o  has two zeroes (i.e., the
	correponding TTT has two blanks squares), we say that state x,o 
	is "two away" from a full board.  For any pair of bitwise tokens
	that are "two away" from a full board, we write those tokens to a 
	file Distance2.  We do same thing for all k from 0 to 8, where
	k is the distance away from a full board.  We do not bother with 
	k = 9, as the only game state that satisfies this is the start state;
	hence, there is no 'Distance9' file.
		
	This partitions all legal states by their distance from a full state.
	This is useful because we must calculate Richman and discrete-Richman
	values backwards-recursively (that is, the Richman value of any state
	is determined by the Richman values of its child states.) With the states 
	partitioned by distance from a full state, and with the knowledge that any 
	child states of a given gamestate must be 1 closer to a full state, we can 
	systematically calculate the Richman values for all terminal nodes (that
	is, all states in Distance0), then for all states in Distance1, then in
	Distance2, and so on.
	
	"""
	debug(str(time.time()) + "\tPartitioning files by distance...")
	writers = [None for i in range(9)]
	for i in range(9):
		writers[i] = open("Distance" + str(i), "w")
		
	f = open("TTTLegalStates.txt", "r")
	lines = f.readlines()
	f.close()

	for line in lines:
		s=line.split(',')
		x=s[0]
		o=s[1]
		num=TTTGameNode.numMissing(int(x),int(o))
		if num == 9: continue
		writers[num].write(x + "," + o)

	for writer in writers: 
		writer.close()

		
def getNodes(i):
	""" 
	Returns a list of nodes read from a specified 'Distance_' file. 
	
	Each line in the specified file will contain two comma-delimited
	tokens in the form: 
	x,o
	where each token will be some non-negative integer written in
	decimal form. The bitwise representations of x and o encode
	the locations of X's pieces and the locations of O's pieces,
	respectively.  In particular, each bitwise representation consists
	of 9 bits that correspond to the 9 squares of a TTT board, and
	a 1-bit represents that there is a piece in the corresponding
	square.
	
	A list of TTTGameNodes, each generated from a line (i.e., a pair of bit
	representations), is returned once the file has been completely read.
	
	"""
	if i == 9:
		return [TTTGameNode()]
	
	w = open("Distance" + str(i), "r")
	nodeReps = w.readlines()
	w.close()
	
	nodes = []
	for nodeRep in nodeReps:
		xRep,oRep = nodeRep.split(",")
		board = TTTGameNode.generateBoard(int(xRep),int(oRep))
		node = TTTGameNode(board)
		nodes.append(node)
	return nodes




class TTTGameNode:

	"""
	A basic data structure that stores a TTT board state and facilitates
	generating legal moves, generating children states, checking if it is
	a win state, etc.

	"""
	
	def __init__(self, board=None):
		"""
		Constructs a TTTGameNode given a board (list of lists).
		If no board is given, the board defaults to blanks.
		INSTANCE VARIABLES:
		- board
		- xRep
		- oRep

		"""
		if not board:
			self.board = [[BLANK,BLANK,BLANK],[BLANK,BLANK,BLANK],[BLANK,BLANK,BLANK]]
		else:
			self.board = self._unsharedCopy(board)
		self.xRep,self.oRep = TTTGameNode.generateBitReps(self.board)

	def generateMove(self, nextNode):
		"""
		Returns a (row, column) tuple to get from this node to nextNode.
		nextNode is assumed to be a legal successor of this node.

		"""
		nextBoard = nextNode.getBoard()
		for row in range(3):
			for col in range(3):
				if self.board[row][col] != nextBoard[row][col]: 
					return row,col
		return 0,0
	
	def getXRep(self):
		"""
		Returns the 9-bit representation for X's pieces on the board.
		xRep, which is stored as an instance variable, is 111000000 for the 
		following board.

		 X | X | X  
		---+---+---
		 O | O |    
		---+---+---
		 O | O |    

		"""
		return self.xRep
	
	def getORep(self):
		"""
		Returns the 9-bit representation for O's pieces on the board.
		oRep, which is stored as an instance variable, is 000110110 for the 
		following board.
	       
		 X | X | X  
		---+---+---
		 O | O |    
		---+---+---
		 O | O |    

		"""
		return self.oRep

	def isWin(self,player):
		"""
		Returns true if this TTTGameNode's board is a win for the given player 
		(either an 'X' or 'O' char).

		"""
		board = self.board
		return     ((board[0][0] == board[0][1] == board[0][2] == player) \
				or  (board[1][0] == board[1][1] == board[1][2] == player) \
				or  (board[2][0] == board[2][1] == board[2][2] == player) \
				or  (board[0][0] == board[1][0] == board[2][0] == player) \
				or  (board[0][1] == board[1][1] == board[2][1] == player) \
				or  (board[0][2] == board[1][2] == board[2][2] == player) \
				or  (board[0][0] == board[1][1] == board[2][2] == player) \
				or  (board[0][2] == board[1][1] == board[2][0] == player))

	def getBoard(self):
		"""
		Returns a deep copy of the board.

		"""
		return self._unsharedCopy(self.board)

	def _unsharedCopy(self,inList):
		"""
		Returns a deep copy of something.
		If given a list, this _unsharedCopy function maps itself over all 
		elements of the given list. This is especially important for
		getBoard(), since the boards of new TTTGameNode objects must not point
		to the boards of any other TTTGameNode objects.

		"""
		if isinstance(inList, list):
			return list( map(self._unsharedCopy, inList) )
		return inList

	def isTerminal(self):
		"""
		Terminal states are either full or won.

		"""
		return self.isWin(X) or self.isWin(O) or self._isFull()
	
	def generateLegalMoves(self):
		"""
		Returns a list of possible next moves, where a move is a (row, column)
		tuple. If the current state is a terminal, the empty list is returned.
		This method is called in generateChildren(player).

		"""
		if self.isTerminal():
			return []
		legalMoves = []
		for row in range(3):
			for col in range(3):
				if self.board[row][col] == BLANK:
					legalMoves.append((row,col))
		return legalMoves

	def generateChild(self, player, (row,col)):
		"""
		Returns the node that results from making the move specified in
		the (row,col) tuple.
		player is a character, either 'X' or 'O'
		move is a tuple of the form (row, column).
		
		"""
		board = self.getBoard()
		board[row][col] = player
		return TTTGameNode(board)

	def generateChildren(self, player):
		"""
		Returns a list of all the possible next states / nodes.
		Note: TTTGameNode makes a deep copy of the passed board.
		
		"""
		children = []
		board = self.getBoard()
		for row,col in self.generateLegalMoves():
			board[row][col] = player
			children.append(TTTGameNode(board)) 
			board[row][col] = BLANK 
		return children

	def generateLastMoves(self):
		"""
		Returns a list of all possible moves that could have led
		to the current gamenode.
		
		"""
		board = self.getBoard()
		lastMoves = []
		for row in range(3):
			for col in range(3):
				if board[row][col] != BLANK:
					player = board[row][col]
					board[row][col] = BLANK
					if not self.isWin(board):
						lastMoves.append((row,col))
					board[row][col] = player
		return lastMoves			   

	def generateParent(self,lastMove):
		"""
		Given a legal lastMove, returns a parent that is the result
		of undoing lastMove.
		
		"""

		board = self.getBoard()
		row,col = lastMove
		board[row][col] = BLANK
		return TTTGameNode(board)


	def __hash__(self):
		return (hash(self.board[0][0]) ^ hash(self.xRep)) >> 1

	def __eq__(self,other):
		otherBoard = other.getBoard()
		for row in range(3):
			for col in range(3):
				if otherBoard[row][col] != self.board[row][col]:
					return False
		return True

	def __str__(self):
		return ' '+self.board[0][0]+' | '+self.board[0][1]+' | '+self.board[0][2]+' \n'+\
		       '---+---+---\n'+\
		       ' '+self.board[1][0]+' | '+self.board[1][1]+' | '+self.board[1][2]+' \n'+\
		       '---+---+---\n'+\
		       ' '+self.board[2][0]+' | '+self.board[2][1]+' | '+self.board[2][2]+' \n'

	@staticmethod
	def generateBoard(intX, intO):
		"""
		Returns the board (list of lists) reconstructed from the given tuple.
		intX is the X 9-bit representation.
		intO is the O 9-bit representation.
		For instance, the bit representations are
		111000000 for X and 000110110 for O in the following board:

		 X | X | X  
		---+---+---
		 O | O |    
		---+---+---
		 O | O |    

		"""
		board = [[BLANK,BLANK,BLANK],[BLANK,BLANK,BLANK],[BLANK,BLANK,BLANK]]
		# We mask the most signficant bit (i.e., the upper left board space) first
		mask = 0b100000000 
		for row in range(3):
			for col in range(3):
				# ((intX & 1) == 1) and ((intO & 1) == 1) are mutually exclusive.
				if intX & mask:
					board[row][col] = X
				elif intO & mask:
					board[row][col] = O
				# Shift the mask right to get the next bit/space for next iteration
				mask >>= 1 
		return board

	@staticmethod
	def generateBitReps(board):
		"""
		Returns a tuple of 9-bit representations (x,o).
		This method is private and only called in TTTGameNode's constructor.
		For instance, the X bit representation is 111000000 and
		the O bit representation is 000110110 for the following board:

		 X | X | X  
		---+---+---
		 O | O |    
		---+---+---
		 O | O |    

		"""
		intX = 0
		intO = 0
		mask = 0b100000000
		for row in range(3):
			for col in range(3):
				if board[row][col] == X:
					intX += mask
				elif board[row][col] == O:
					intO += mask
				mask >>= 1
		return (intX, intO)

	@staticmethod
	def numMissing(xRep,oRep):
		""" 
		Returns the number of blanks (zeroes) in the
		two given bit representations for X and O.

		"""
		bits = xRep | oRep
		count = 0
		for i in range(9):
			if (bits & 1) == 0: count += 1
			bits = bits >> 1
		return count

	def _isFull(self):
		"""
		Returns true if the board is full and the game has ended.
		
		"""
		for row in range(3):
			for col in range(3):
				if self.board[row][col] == BLANK: return False
		return True




class TTTDiscretePlayer:
	"""
	A perfect player of discrete-valued bidding Tic-Tac-Toe

	"""

	def __init__(self,player,totalChips):
		self.player = player
		self.opponent = PlayTTT.getOpponent(player)
		self.totalChips = totalChips

		# nodesToDiscreteRich is a list of dictionaries that hold
		# entries of the form
		#
		# gameNode : discrete-Richman value.
		#
		# The nodes are partitioned by their distance away from a
		# full state, such that nodesToDiscreteRich[k] carries all
		# entries with node-keys that are k steps away from a full
		# state.
		self.nodesToDiscreteRich = [{},{},{},{},{},{},{},{},{},{}]

		# nodesToMoveBid is a list of dictionaries that hold
		# entries of the form
		#
		# gameNode : (optimalMove, optimalBid),
		#
		# where optimalMove is of the form (row, col). The nodes 
		# are partitioned by their distance away from a full state
		self.nodesToMoveBid = [{},{},{},{},{},{},{},{},{},{}]

		self.generateStrategy()

	def getMoveBid(self,currentNode):
		numBlanks = TTTGameNode.numMissing(currentNode.getXRep(),currentNode.getORep())
		move,bid = self.nodesToMoveBid[numBlanks][currentNode]
		return move,bid

	def generateStrategy(self):

		"""
		This method populates nodesToDiscreteRich and nodesToMoveBid.

		"""

		debug(str(time.time()) + "\tGenerating strategy...")
		
		"""
		Having already created the necessary 'Distance_' files,
		we no longer need to call this line when generating
		strategy.  However, one does not have the 'Distance_' files,
		one must be sure to uncomment this line and run the program
		at least once.

		"""
		# partitionByDistance()

		"""
		BASE CASES:
		
		We first assign discrete-Richman values to all terminal nodes.
		All terminal nodes are guaranteed to be a win (for the agent),
		a draw, or a loss.  The theory defines the disrete-Richman value
		of any win state to be 0 (that is, you need 0 chips to win from
		that state), and the discrete-Richman value for any draw or loss
		to be k+1, where k is the total number of chips in play. 

		See the paper titled 'Discrete Bidding Games' by Develin and Payne 
		for more details.

		"""

		nodes0 = getNodes(0)

		for node in nodes0:
			if node.isWin(self.player):
				self.nodesToDiscreteRich[0][node] = 0.0
			else:
				self.nodesToDiscreteRich[0][node] = self.totalChips + 1.0

		"""
		BACKWARDS INDUCTION:

		Calculating discrete-Richman values is similar to calculating Richman
		values, but needs to check different cases to maintain discreteness.  As 
		these cases are technical and would take a good amount of space to
		explain, we again refer the reader to the paper 'Discrete Bidding Games'
		by Develin and Payne for a better explanation.  Having read that, the
		relatively brief documentation in the four cases toward the end of the loop
		below should suffice.

		"""
				
		for i in range(1,10):
			# Get all nodes that are i steps away from a full state
			nodes = getNodes(i)

			for node in nodes:

				# If the node is a win state for the agent, assign it 
				# a discrete-Richman value of 0.
				if node.isWin(self.player):
					self.nodesToDiscreteRich[i][node] = 0.0
					continue
				# Else if the node is a win state for the opponent, assign
				# a discrete-Richman value of k+1.
				elif node.isWin(self.opponent):
					self.nodesToDiscreteRich[i][node] = self.totalChips + 1.0
					continue

				# For the current node, find the minimum discrete-Richman
				# value of its children that the agent can move to, and the
				# maximum discrete-Richman value of its children that the
				# opponent can move to.  As well, store the child node that
				# corresponds to the minimum discrete-Richman value, so that
				# we can determine the optimal move.
					
				Fmax = -1.0
				Fmin = sys.maxint 
				myChildren = node.generateChildren(self.player)
				oppChildren = node.generateChildren(self.opponent)

				for myChild in myChildren:
					if Fmin > self.nodesToDiscreteRich[i-1][myChild]:
						Fmin = self.nodesToDiscreteRich[i-1][myChild]
						favoredChild = myChild

				for oppChild in oppChildren:
					Fmax = max(Fmax,self.nodesToDiscreteRich[i-1][oppChild])

				# Discrete-Richman values may or may not include the tie-breaking
				# chip *.  Conveniently, as the value of * is strictly positive but
				# strictly less than 1 (i.e. 0 < * < 1), we can encode these into
				# the discrete-Richman values as a decimal part of 0.5.  This may
				# be included in the final calculated value of the discrete-Richman
				# value of the current node depending on the cases mentioned above,
				# and can be seen in the value of epsilon.  FmaxVal and FminVal
				# store the underlying integer value of Fmax and Fmin, respectively.
				# Note that Payne and Develin denote underlying value of a discrete-
				# Richman value with absolute value bars.

				# Note that, in two of the cases, the optimal bid is appended with
				# a decimal part of 0.25.  This should not be thought of as part of
				# the value of the optimal bid, but rather as marker.  If the agent
				# makes a bid of the form n + 0.25, this means that the game engine
				# should check if the agent has the tie breaking chip at that moment.
				# If the agent does, then the agent will bet n (and use the tie
				# breaking chip if a tie arises); if the agent does not have the
				# tie breaking chip, then the agent will bet n+1.  

			    	
				FmaxVal = math.floor(Fmax)
				FminVal = math.floor(Fmin)
				Fsum = FmaxVal + FminVal

				# If Fsum is odd and Fmin \in \N*
				if (Fsum % 2 == 1) and FminVal < Fmin:
					epsilon = 1.0
					bid = math.floor(abs(FmaxVal-FminVal)/2.0) * 1.0
				# Else if Fsum is odd and Fmin \in \N
				elif (Fsum % 2 == 1) and FminVal == Fmin:
					epsilon = 0.5
					bid = math.floor(abs(FmaxVal-FminVal)/2.0) + 0.25
				# Else if Fsum is even and Fmin \in \N*
				elif (Fsum % 2 == 0) and FminVal < Fmin:
					epsilon = 0.5
					bid = max(0,abs(FmaxVal-FminVal)/2.0 - 0.75)
				# Else (i.e., if Fsum is even and Fmin \in \N)
				else:
					epsilon = 0.0
					bid = abs(FmaxVal-FminVal)/2.0

				self.nodesToDiscreteRich[i][node] = math.floor(Fsum/2.0) + epsilon
				self.nodesToMoveBid[i][node] = (node.generateMove(favoredChild), bid)



class TTTRealPlayer:
	"""
	A perfect player of real-valued bidding Tic-Tac-Toe

	"""

	def __init__(self,player):
		"""
		INSTANCE VARIABLES:
		- player (either 'X' or 'O')
		- opponent (the opposite of player)
		- nodesToRichman (maps states/nodes to Richman values)
		- nodesToMoveBid (maps states/nodes to (move,bid) tuples)

		"""
		self.player = player
		self.opponent = PlayTTT.getOpponent(player)

		# nodesToRichman is a list of dictionaries that hold
		# entries of the form
		#
		# gameNode : Richman value.
		#
		# The nodes are partitioned by their distance away from a
		# full state, such that nodesToDiscreteRich[k] carries all
		# entries with node-keys that are k steps away from a full
		# state.
		self.nodesToRichman = [{},{},{},{},{},{},{},{},{},{}]

		# nodesToMoveBid is a list of dictionaries that hold
		# entries of the form
		#
		# gameNode : (optimalMove, optimalBid),
		#
		# where optimalMove is of the form (row, col). The nodes 
		# are partitioned by their distance away from a full state.
		self.nodesToMoveBid = [{},{},{},{},{},{},{},{},{},{}]

		self.generateStrategy()

	def getMoveBid(self,currentNode):
		"""
		Returns the (move, bid) tuple for the specified node.
		In real-valued bidding, there is no tie breaker. In discrete-valued
		bidding, agentHasTieBreaker will be either true or false.

		"""
		numBlanks = TTTGameNode.numMissing(currentNode.getXRep(),currentNode.getORep())
		return self.nodesToMoveBid[numBlanks][currentNode]

	def generateStrategy(self):
		"""
		This method populates nodesToRichman and nodesToMoveBid

		"""

		debug(str(time.time()) + "\tGenerating strategy...")

		# No need to call again after the first time.
		# partitionByDistance()

		
		"""
		BASE CASES:
		
		We first assign Richman values to all terminal nodes.
		All terminal nodes are guaranteed to be a win (for the agent),
		a draw, or a loss.  The theory defines the Richman value
		of any win state to be 0 (that is, you need 0 chips to win from
		that state), and the discrete-Richman value for any draw or loss
		to be 1.

		See the paper titled 'Discrete Bidding Games' by Develin and Payne 
		for more details.

		"""

		nodes0 = getNodes(0);

		for node in nodes0:
			if node.isWin(self.player):
				self.nodesToRichman[0][node] = 0.0
			else:
				self.nodesToRichman[0][node] = 1.0

		"""
		BACKWARDS INDUCTION:

		For a given gamestate G, let Rmin(G) denote the minimum Richman 
		value of a child gamestate that the agent can move to, and let
		Rmax(G) denote the maximum Richman value of a child gamestate that
		the opponent can move to.  Then
		
		    R(G) = (Rmax(G) + Rmin(G)) / 2.

		Furthermore, the optimal move from R(G) is the move that brings the
		agent to the gamestate with Richman value Rmin(G), and the optimal
		bid is abs( Rmax(G) - Rmin(G)) / 2.

		"""

		for i in range(1,10):
			nodes = getNodes(i)
			
			for node in nodes:
				if node.isWin(self.player):
					self.nodesToRichman[i][node] = 0.0
					continue
				elif node.isWin(self.opponent):
					self.nodesToRichman[i][node] = 1.0
					continue
				
				Rmax = -1.0
				Rmin = 2.0
				myChildren = node.generateChildren(self.player)
				oppChildren = node.generateChildren(self.opponent)

				for myChild in myChildren:
					if Rmin > self.nodesToRichman[i-1][myChild]:
						Rmin = self.nodesToRichman[i-1][myChild]
						favoredChild = myChild

				for oppChild in oppChildren:
					Rmax = max(Rmax,self.nodesToRichman[i-1][oppChild])
				
				self.nodesToRichman[i][node] = (Rmax + Rmin)/2.0
				self.nodesToMoveBid[i][node] = (node.generateMove(favoredChild), abs(Rmax-Rmin)/2.0)

		node = TTTGameNode()
		print self.nodesToRichman[9][node]

		
class PlayTTT:		
	"""
	PlayTTT is the game engine for Tic-Tac-Toe.
	"""
	def __init__(self):

		debug(str(time.time()) + "\tInitializing game...")
		self.biddingType = self._queryBiddingType()

		debug(str(time.time()) + "\tInitializing root node...")
		self.gamenode = TTTGameNode()

		if self.biddingType == 'r':
			self.chips = {X:1-0.51953126,O:0.51953126}
			self.rules = "You are playing real-valued bidding Tic-Tac-Toe."
			self.agent = TTTRealPlayer(O) 
			print self.agent.nodesToRichman[9][self.gamenode]

		elif self.biddingType == 'd':
			chipNo = self._queryChipCount()
			agentChips = float(math.ceil(0.51953126*chipNo))
			self.chips = {X:chipNo-agentChips,O:agentChips}
			
			if self._queryStartWithTieBreakingChip():
				self.chips[X] += 0.5
			else:
				self.chips[O] += 0.5
			self.rules = "You are playing discrete-valued bidding Tic-Tac-Toe."	
			self.agent = TTTDiscretePlayer(O, chipNo)
			print self.agent.nodesToDiscreteRich[9][self.gamenode]

		self.agentLastBid = None

		self.userWonLastBid = -1

		debug(str(time.time()) + "\tPlaying...")


		if self.biddingType == 'r':
			self.playReal()
		elif self.biddingType == 'd':
			self.playDiscrete()

	def updateGameState(self, player, move, bid):
		"""
		Updates current gamenode and chip counts

		"""

		self.gamenode = self.gamenode.generateChild(player,move) 

		if player == X:
			self.userWonLastBid = 1
			self.chips[X] -= bid
			self.chips[O] += bid
		else:
			self.userWonLastBid = 0
			self.chips[X] += bid
			self.chips[O] -= bid

	def playDiscrete(self):
		"""
		Runs a discrete-valued bidding game.
		
		"""
		self._printBoard()
		while not self.gamenode.isTerminal():
			userBid = self._queryBid() # must be an int
			userMove = self._queryMove()

			agentMove,agentBid = self.agent.getMoveBid(self.gamenode)
			agentHasTieBreaker = ((self.chips[O] % 1) == 0.5)


			# If agentBid is marked with 0.25, then check if the agent
			# has the tie breaking chip.  If the agent does, then bid
			# the underlying integer amount (and use the tie-breaking
			# chip if a tie arises); else, bid the underlying integer
			# amount plus 1.
			if agentBid % 1 == 0.25:
				if agentHasTieBreaker:
					agentBid = math.floor(agentBid)
				else:
					if agentBid < self.chips[O]:
						agentBid = math.ceil(agentBid)
						
						
			self.agentLastBid = agentBid

			# Cast bid values to ints to get underlying bid values.
			if int(userBid) > int(agentBid):
				self.updateGameState(X, userMove, userBid)

			elif int(userBid) < int(agentBid):
				self.updateGameState(O, agentMove, agentBid)
			
			elif int(userBid) == int(agentBid) and agentHasTieBreaker:
 				self.updateGameState(O, agentMove, agentBid+0.5)
			
			else: # int(userBid) == int(agentBid) and not agentHasTieBreaker
				if self._queryUseTieBreakingChip():
					self.updateGameState(X, userMove, userBid+0.5)
				else:
					self.updateGameState(O, agentMove, agentBid)
				
			self._printStatus()
			
		if self.gamenode.isWin(X):
			print "You won!"
		elif self.gamenode.isWin(O):
			print "Sorry, the computer bested you this time."
		else:
			print "You seem to be an even match... Just watch out next time..."

		sys.exit("GAME OVER.")

	def playReal(self):
		"""
		Runs a real-valued bidding game.

		"""
		
		self._printBoard()
		while not self.gamenode.isTerminal():
			userBid = self._queryBid()
			userMove = self._queryMove()

			agentMove,agentBid = self.agent.getMoveBid(self.gamenode)

			self.agentLastBid = agentBid

			if userBid > agentBid:
				print 'You won the bid.\n'
				self.updateGameState(X, userMove, userBid)
				
			elif agentBid > userBid:
				print 'You lost the bid.\n'
				self.updateGameState(O, agentMove, agentBid) 

			# In real-valued bidding, the event of a tie is so rare that it is
			# not even considered by many authors.  However, in their paper titled
			# 'Richman Games', Lazarus et. al state in their introduction that
			# "Should the two bids be equal, the tie is broken by a toss of a coin."
			else:
				if random.random() < 0.5:
					print 'You won the bid.\n'
					self.updateGameState(X, userMove, userBid)
				else:
					print 'You lost the bid.\n'
					self.updateGameState(O, agentMove, agentBid)

			self._printStatus()

		if self.gamenode.isWin(X):
			print "You won!"
		elif self.gamenode.isWin(O):
			print "Sorry, the computer bested you this time."
		else:
			print "You seem to be an even match... Just watch out next time..."
			
		sys.exit("GAME OVER.")

	@staticmethod
	def getOpponent(player):
		""" Returns the opponent of the given player. """
		if player == X: return O
		return X

	def _printBoard(self):
		board = self.gamenode.getBoard()
		c = ['' for i in range(9)]
		i = 0
		for row in range(len(board)):
			for col in range(len(board[row])):
				cell = board[row][col]
				if cell == BLANK:
					c[i] = str(i + 1)
				else:
					c[i] = ' '
   				i += 1

		colSep = "|"
		helpRow1 = " " + c[0] + " " + colSep + " " + c[1] + " " + colSep + " " + c[2]
		helpRow2 = " " + c[3] + " " + colSep + " " + c[4] + " " + colSep + " " + c[5]
		helpRow3 = " " + c[6] + " " + colSep + " " + c[7] + " " + colSep + " " + c[8]
		helpRowSep = "---+---+---"

		bTitle = " THE BOARD "
		hTitle = " THE GUIDE "
		rowSep = "---+---+---"
		tab = "\t"

		print bTitle, tab, hTitle

		print '', board[0][0] , colSep , board[0][1] , colSep , board[0][2] , tab , helpRow1
		print rowSep, tab, helpRowSep
		print '', board[1][0] , colSep , board[1][1] , colSep , board[1][2] , tab , helpRow2
		print rowSep, tab, helpRowSep
		print '', board[2][0] , colSep , board[2][1] , colSep , board[2][2] , tab , helpRow3
		print ''

	def _printChips(self):
		"""
		A private method for printing chip statuses.

		"""
		
		c1 = str(self.chips[X])
		c2 = str(self.chips[O])

		if self.biddingType == 'd':
			c1 = c1[:-2]
			c2 = c2[:-2]
			if ((self.chips[X] % 1) == 0.5):
				c1 += "*"
			if ((self.chips[O] % 1) == 0.5):
				c2 += "*"

		### TESTING ###
		l = str(self.agentLastBid)
		header = " " + "YOU:".rjust(len(c1)) + "\t" + "CPU:".rjust(len(c2)) + "\t" + "LAST CPU BID:".rjust(len(l))
		footer = " " + c1 + "\t" + c2 + "\t" + l
		print header
		print footer

	def _printStatus(self):
		"""
		A private method for flushing the terminal,
		and printing chip statuses and the board.

		"""
		flush()
		green(self.rules)
		print '\n\n\n'
		
		self._printChips()
		print ''
		self._printBoard()
		print '\n'

		if self.userWonLastBid == 1:
			print "You won the bid!\n\n"
		elif self.userWonLastBid == 0:
			print "You lost the bid!\n\n"
		else:
			print "\n\n"


	def _queryBiddingType(self):
		while True:
			flush()
			gameType = raw_input("Would you like to play a real-valued bidding game ('r') or a discrete-valued bidding game ('d')? ").lower()[0]
			if gameType == 'r' or gameType == 'd':
				return gameType


   	def _queryStartWithTieBreakingChip(self):
		"""
		A private method that determines which player starts
		with the tie-breaking chip.

		"""
		while True:
			flush()
			answer = raw_input("Would you like to start with the tie-breaking chip ('y' or 'n')? ").lower()
			if answer[0] == 'y':
				return True
			elif answer[0] == 'n':
				return False
			continue

	def _queryChipCount(self):
		"""
		A private method for querying the user for an initial number of chips.
		Only used in discrete-valued Tic-Tac-Toe.

		"""
		query = "Enter the total starting chip count: "
		while True:
			flush()
			try:
				chips = int(float(raw_input(query)))
			except ValueError:
				continue
			if chips >= 0: # Can't have negative chips
				break
		return chips
			
	def _queryUseTieBreakingChip(self):
		"""
		A private method for querying the user to use a tie breaker.
		Returns true if player wants to use the tie breaker, otherwise false.

		"""
		query = "You've tied bids. Would you like to use the tie-breaking chip ('y' or 'n')? "
		while True:
			self._printStatus()
			answer = raw_input(query).lower()
			if answer[0] == 'y':
				return True
			elif answer[0] == 'n':
				return False

	def _queryBid(self):
		"""
		A private method for querying the user for a bid.

		"""
		if self.biddingType == 'r':
			query = "Enter a non-negative real-valued bid up to " + str(self.chips[X]) + ": "
			while True:
				self._printStatus()
				try:
					bid = float(raw_input(query))
				except ValueError:
					continue
				if self._isLegalBid(bid):
					break

		elif self.biddingType == 'd':
			query = "Enter a non-negative integer bid up to " + str(int(self.chips[X])) + ": "
			while True:
				self._printStatus()
				try:
					bid = int(raw_input(query))
				except ValueError:
					continue
				if self._isLegalBid(bid):
					break

   		return bid

	def _queryMove(self):
		"""
		A private method for querying the user for a move.

		"""
		query = "Enter the desired square: "
		while True:
			self._printStatus()
			userMoveList = raw_input(query).split()
			if len(userMoveList) != 1:
				continue
			try:
				for i in userMoveList:
					int(i)
			except ValueError:
				continue

			row,col = self._squareToCoordinates(int(userMoveList[0]))
			if self._isLegalMove(row,col): 
				break
		return (row,col)

	def _squareToCoordinates(self, square):
		"""
		A private method, used in _queryMove, to convert user-entered
		ints representing board spaces to (row,column) tuples.
		1 -> 0,0
		2 -> 1,0
		3 -> 2,0
		4 -> 0,1
		5 -> 1,1
		6 -> 2,1
		7 -> 0,2
		8 -> 1,2
		9 -> 2,2
		"""
		if 0 < square < 10:
			col = (square-1) % 3
			row = (square-1) / 3
			return (row, col)
		return (None,None)
	
	def _isLegalMove(self, row, col):
		"""
		A private method that determines whether a given move, encoded as a 
		(row, column) tuple, is legal (i.e., if it's blank on the board).
		"""
		if row is None or col is None: 
			return False
		try:
			return self.gamenode.board[row][col] == BLANK
		except IndexError:
			return False
	
	def _isLegalBid(self, bid):
		"""
		A private method that determines if a bid is legal (i.e., if it is
		greater than 0 and less than the number of chips the user has).
		"""
		return 0 <= bid <= self.chips[X]



if __name__ == '__main__':

	PlayTTT()

