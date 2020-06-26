from plark_game.classes import Pelican_Agent

class PelicanAgentTestTurn(Pelican_Agent):

	def __init__(self):
		self.moves_taken = 0

	def getAction(self, state):
		# Alternately move down/up
		action = 3 if self.moves_taken % 2 == 0 else 0
		self.moves_taken += 1
		return self.action_lookup(action)


