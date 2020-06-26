from .agent import Agent

class Pelican_Agent(Agent):
	def cell_to_action(self, cell, col, row ):
		# this function return the action required to move from a current cell to a target cell. this only work for a single cell
		if  cell['col'] == col:
			# 0 or 3
			if cell['row'] < row:
				return 0 # Up
			else:
				return 3 # Down

		if cell['col'] % 2 == 0:
			# even cells
			if cell['col'] > col:
				# 2 or 3
				if cell['row'] == row:
					return 1 # Up right
				else:
					return 2 # Down right
			elif cell['col'] < col:
				# 5 or 6
				if cell['row'] == row:
					return 5 # Up left
				else:
					return 4 # Down left
		else:
			# odd cells
			if cell['col'] > col:
				# 2 or 3
				if cell['row'] == row:
					return 2 # Up right
				else:
					return 1 # Down right
			elif cell['col'] < col:
				# 5 or 6
				if cell['row'] == row:
					return 4 # Up left
				else:
					return 5 # Down left 


	def action_lookup(self, action):
		return ACTION_LOOKUP[action]

ACTION_LOOKUP = {
    0 : '1',  # Up
    1 : '2',  # Up right
    2 : '3',  # Down right
    3 : '4',  # Down
    4 : '5',  # Down left
    5 : '6',  # Up left
    6 : 'drop_buoy',  
    7 : 'drop_torpedo',  
    8 : 'end'  
}