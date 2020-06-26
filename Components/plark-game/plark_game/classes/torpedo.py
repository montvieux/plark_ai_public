## Class responsible for representing the torpedo game piece
class Torpedo():
	
	def __init__(self, **kwargs):
		self.id = ""
		self.type = "TORPEDO"
		self.col = None
		self.row = None
		self.turn = 1
		self.size = 2
		self.speed = kwargs.get('speed')
		self.searchRadius = kwargs.get('search_range')
	 
	def setLocation(self, col, row):
		self.col = col
		self.row = row
