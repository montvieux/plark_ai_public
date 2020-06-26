from .agent import Agent

class Panther_Agent(Agent):
	def action_lookup(self, action):
		return ACTION_LOOKUP[action]

ACTION_LOOKUP = {
    0 : '1',  # Up
    1 : '2',  # Up right
    2 : '3',  # Down right
    3 : '4',  # Down
    4 : '5',  # Down left
    5 : '6',  # Up left
	6 : 'end'
}
