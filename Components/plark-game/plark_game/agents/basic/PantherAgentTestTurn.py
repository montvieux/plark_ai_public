from plark_game.classes import Panther_Agent

class PantherAgentTestTurn(Panther_Agent):

	def __init__(self):
		self.moves_taken = 0

	def getAction(self, state):
		# Alternately move up/down
		action = 0 if self.moves_taken % 2 == 0 else 3
		self.moves_taken += 1
		return self.action_lookup(action)


