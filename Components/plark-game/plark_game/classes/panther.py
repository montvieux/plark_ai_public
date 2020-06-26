## Panther class is responsible for controlling the PLARK submarine game piece
class Panther():

	def __init__(self):
		self.col = None
		self.row = None
		self.type = "PANTHER"

	def setLocation(self, col, row):
		self.col = col
		self.row = row