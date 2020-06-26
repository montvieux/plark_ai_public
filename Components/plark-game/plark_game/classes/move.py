## Class that represents a move on the board. This involves the creation of various game components
## These components will be set with specific information regarding where to move and what to deploy on the board.
class Move():
	
	def __init__(self):
		self.sonobuoyList = []
		self.torpList = []
		self.moveList = []
		self.type = "test"
		self.id = "TESTMOVE"

	## Method for taking in a single pair of coordinates and adding to the movelist.
	def addToMoveList(self, list):
		self.moveList.append(list)

	## Set the ID of the move object, will be useful later on.
	def setID(id):
		self.id = id
	
	## Get the move list a list of 2 element lists. 
	def getMoveList(self):
		return self.moveList
	
	## Get the torp list, list of torp objects
	def getTorpList(self):
		return self.torpList

	## Getter for sonobuoy objects return sonobuoy object list 
	def getSonobuoyList(self):
		return self.sonobuoyList

	## Setter for movelist returns a list of 2 element lists
	def setMoveList(self,movelist):
		self.moveList = movelist

	## Setter for the TorpList returns list of Torpedo objects
	def setTorpList(self, torplist):
		self.torpList = torplist

	## Setter for Sonobuoy, allows the addition of a list of Sonobuoy objects.
	def setSonobuoyList(self, sonobuoylist):
		self.sonobuoyList = sonobuoylist

