from plark_game.classes import Panther_Agent

class PantherAgentIllegalMove(Panther_Agent):

	def __init__(self):
		self.moves_taken = 0

	def reset_moves_taken(self):
		self.moves_taken = 0

	def getAction(self, state):
		# Always try to move down (illegal move)
		self.moves_taken += 1
		return self.action_lookup(3)


