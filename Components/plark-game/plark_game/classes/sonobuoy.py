## Class responsible for representing a Sonobouy within Hunting the Plark
class Sonobuoy():
	
	def __init__(self, active_range):
		self.type = "SONOBUOY"
		self.col = None
		self.row = None
		self.range = active_range
		self.state = "COLD"
		self.size = 1
	
	## Setstate allows the change of state which will happen when detection occurs
	def setState(self,state):
		self.state = state 

	## Gets the state of the sonobuoy
	def getState(self):
		return self.state
	
	## Getter to return range of sonobuoy
	def getRange(self):
		return self.range

	## Getter for returning the object type.
	def getType(self):
		return self.type

	def setLocation(self, col, row):
		self.col = col
		self.row = row