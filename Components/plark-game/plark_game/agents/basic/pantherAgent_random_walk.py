import os
from random import seed
from random import randint

from plark_game.classes import Panther_Agent
from plark_game import game_helper
import jsonpickle


class Panther_Agent_Random_Walk(Panther_Agent):

	def __init__(self):
		pass

	def getAction(self, state):
		map_width = state['map_width']
		panther_col = state['panther_col']
		actions = [0]
		if panther_col != 0: #If it is not on the left add move left action
			actions.append(5)
		if panther_col < map_width: #If it is not on the right add move right action
			actions.append(1)

		seed()
		actionValue =  actions[randint(0, len(actions)-1)]

		return self.action_lookup(actionValue) 



# ACTION_LOOKUP = {
#     0 : '1',  # Up
#     1 : '2',  # Up right
#     2 : '3',  # Down right
#     3 : '4',  # Down
#     4 : '5',  # Down left
#     5 : '6',  # Up left
# 	6 : 'end'
# }
