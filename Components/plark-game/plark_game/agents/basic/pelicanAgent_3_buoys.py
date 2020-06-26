from plark_game.classes import PelicanAgentFixedSBs

class Pelican_Agent_3_Bouys(PelicanAgentFixedSBs):

	def __init__(self):
		super(Pelican_Agent_3_Bouys, self).__init__()
		self.sb_locations = [
			{'col':2, 'row':2},
			{'col':7, 'row':5},
			{'col':0, 'row':7}
		]
