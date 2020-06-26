from plark_game.classes import Panther_Agent

class Panther_Agent_Move_North(Panther_Agent):

	def __init__(self):
		pass

	def getAction(self, state):
		return self.action_lookup(0)


