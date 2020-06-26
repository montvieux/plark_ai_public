import gym
from gym import error, spaces, utils

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Observation():

	def __init__(self,game,**kwargs):
		self.game = game
		self.kwargs = kwargs
		if self.kwargs.get('driving_agent'):
			self.driving_agent = self.kwargs.get('driving_agent')
		else:
			self.driving_agent = 'pelican'
			self.kwargs['driving_agent'] = self.driving_agent

		self.max_grid_width = 30
		self.max_grid_height = 30
		self.max_sonobuoys = 25
		self.max_turns = 40
		self.max_pelican_moves = 25
		self.max_panther_moves = 5
		self.max_torpedoes = 25
		self.max_torpedo_turns = 3
		self.max_torpedo_speed = 3

		# self.max_grid_width = kwargs.get('max_grid_width', 30)
		# self.max_grid_height = kwargs.get('max_grid_height',30)
		# self.max_sonobuoys = kwargs.get('max_sonobuoys', 25)
		# self.max_turns = kwargs.get('max_turns', 40)
		# self.max_pelican_moves = kwargs.get('max_pelican_moves', 25)
		# self.max_panther_moves = kwargs.get('max_panther_moves', 5)
		# self.max_torpedoes = kwargs.get('max_torpedoes', 25)
		# self.max_torpedo_turns = kwargs.get('max_torpedo_turns', 3)
		# self.max_torpedo_speed = kwargs.get('max_torpedo_speed', 3)

		self.pelican_col = 0 
		self.pelican_row = 0
		self.panther_col = 0
		self.panther_row = 0 


		logger.info('non-image observation space')
		obs_shape = []
		obs_label = [] 

		# Represent the chosen grid width
		assert game.map_width <= self.max_grid_width, "Game width must not be greater than max grid width: {}".format(self.max_grid_width)
		assert game.map_height <= self.max_grid_height, "Game height must not be greater than max grid height: {}".format(self.max_grid_width)
		obs_shape.append(self.max_grid_width)
		obs_label.append('max_grid_width')
		obs_shape.append(self.max_grid_height)
		obs_label.append('max_grid_height')
		# Number of turns remaining
		assert game.maxTurns <= self.max_turns, "Game max turns must not be greater than max possible turns: {}".format(self.max_turns)
		obs_shape.append(self.max_turns)
		obs_label.append('max_turns')	
		if self.driving_agent == 'pelican':
			# Number of moves remaining per turn
			assert game.pelican_parameters['move_limit'] <= self.max_pelican_moves, "Game move limit must not be greater than max move limit: {}".format(self.max_pelican_moves)
			obs_shape.append(self.max_pelican_moves)
			obs_label.append('max_pelican_moves')	
			# Pelican location
			obs_shape.append(self.max_grid_width)
			obs_label.append('pel x')	
			obs_shape.append(self.max_grid_height)
			obs_label.append('pel y')	
			
			# Madman status - this is a boolean
			obs_shape.append(2)
			obs_label.append('madman')	

			# sonobuoy range
			self.max_sb_range = int(max(self.max_grid_height, self.max_grid_width)/2)
			assert game.sonobuoy_parameters['active_range'] <= self.max_sb_range, "Sonobuoy active range must not be greater than max range: {}".format(self.max_sb_range)
			obs_shape.append(self.max_sb_range)
			obs_label.append('max_sb_range')	

			# Number of sonobuoys remaining
			assert game.pelican_parameters['default_sonobuoys'] <= self.max_sonobuoys, "Starting number of sonobuoys must not be greater than maximum possible sonobuoys: {}".format(self.max_sonobuoys)
			obs_shape.append(self.max_sonobuoys)
			obs_label.append('max_sonobuoys')	

			# sonobuoy locations and activations
			for i in range(self.max_sonobuoys):
				# location (max_height+1, max_width+1) represents undeployed
				obs_shape.append(self.max_grid_width+1)
				obs_label.append('sb x')	
				obs_shape.append(self.max_grid_height+1)
				obs_label.append('sb y')	
				# binary: 0=inactive, 1=active
				obs_shape.append(2)
				obs_label.append('sb active')

			# Number of torpedoes remaining
			assert game.pelican_parameters['default_torps'] <= self.max_torpedoes, "Starting number of sonobuoys must not be greater than maximum possible sonobuoys: {}".format(self.max_torpedoes)
			obs_shape.append(self.max_torpedoes)
			obs_label.append('max_torpedoes')

			# Torpedo hunt enabled - boolean
			obs_shape.append(2)
			obs_label.append('Torpedo hunt enabled bool')

			# Torpedo speeds for each turn
			assert game.torpedo_parameters['turn_limit'] <= self.max_torpedo_turns, "Torpedo turn limit must not be greater than the maximum torpedo turns: {}".format(self.max_torpedo_turns)
			for speed in game.torpedo_parameters['speed']:
				assert speed <= self.max_torpedo_speed, "Torpedo speed for each turn must not be greater than the maximum torpedo speed: {}".format(self.max_torpedo_speed)
			for turn in range(self.max_torpedo_turns):
				# speed can also be zero:
				# e.g. max speed of 3 leads to possible values [0,1,2,3]
				obs_shape.append(self.max_torpedo_speed+1)
				obs_label.append('max_torpedo_speed+1')

			# torpedo locations
			for i in range(self.max_torpedoes):
				# location (max_height+1, max_width+1) represents undeployed
				obs_shape.append(self.max_grid_width+1)
				obs_label.append('torp x')
				obs_shape.append(self.max_grid_height+1)
				obs_label.append('torp y')

			
		else:
			# Number of moves remaining per turn
			assert game.panther_parameters['move_limit'] <= self.max_panther_moves, "Game move limit must not be greater than max move limit: {}".format(self.max_panther_moves)
			obs_shape.append(self.max_panther_moves)
			obs_label.append('max_panther_moves')
			# Pelican location
			obs_shape.append(self.max_grid_width)
			obs_label.append('pel x')
			obs_shape.append(self.max_grid_height)
			obs_label.append('pel y')
			
			# Panther location
			obs_shape.append(self.max_grid_width)
			obs_label.append('pan x')
			obs_shape.append(self.max_grid_height)
			obs_label.append('pan y')
			
			# Madman status - this is a boolean
			obs_shape.append(2)
			obs_label.append('madman')

			# sonobuoy range
			self.max_sb_range = int(max(self.max_grid_height, self.max_grid_width)/2)
			assert game.sonobuoy_parameters['active_range'] <= self.max_sb_range, "Sonobuoy active range must not be greater than max range: {}".format(self.max_sb_range)
			obs_shape.append(self.max_sb_range)
			obs_label.append('max_sb_range')

			# Number of sonobuoys remaining
			assert game.pelican_parameters['default_sonobuoys'] <= self.max_sonobuoys, "Starting number of sonobuoys must not be greater than maximum possible sonobuoys: {}".format(self.max_sonobuoys)
			obs_shape.append(self.max_sonobuoys)
			obs_label.append('max_sonobuoys')


			# sonobuoy locations and activations
			for i in range(self.max_sonobuoys):
				# location (max_height+1, max_width+1) represents undeployed
				obs_shape.append(self.max_grid_width+1)
				obs_label.append('sb x')
				obs_shape.append(self.max_grid_height+1)
				obs_label.append('sb y')
				# binary: 0=inactive, 1=active
				obs_shape.append(2)
				obs_label.append('sb active')

			# Number of torpedoes remaining
			assert game.pelican_parameters['default_torps'] <= self.max_torpedoes, "Starting number of sonobuoys must not be greater than maximum possible sonobuoys: {}".format(self.max_torpedoes)
			obs_shape.append(self.max_torpedoes)
			obs_label.append('max_torpedoes')

			# Torpedo hunt enabled - boolean
			obs_shape.append(2)
			obs_label.append('torpedo hunt bool')

			# Torpedo speeds for each turn
			assert game.torpedo_parameters['turn_limit'] <= self.max_torpedo_turns, "Torpedo turn limit must not be greater than the maximum torpedo turns: {}".format(self.max_torpedo_turns)
			for speed in game.torpedo_parameters['speed']:
				assert speed <= self.max_torpedo_speed, "Torpedo speed for each turn must not be greater than the maximum torpedo speed: {}".format(self.max_torpedo_speed)
			for turn in range(self.max_torpedo_turns):
				# speed can also be zero:
				# e.g. max speed of 3 leads to possible values [0,1,2,3]
				obs_shape.append(self.max_torpedo_speed+1)
				obs_label.append('max_torpedo_speed')

			# torpedo locations
			for i in range(self.max_torpedoes):
				# location (max_height+1, max_width+1) represents undeployed
				obs_shape.append(self.max_grid_height+1)
				obs_label.append('torp x')
				obs_shape.append(self.max_grid_width+1)
				obs_label.append('torp y')

		obs_shape_new = []
		for i in obs_shape:
			obs_shape_new.append(i+1)
		obs_shape = obs_shape_new	

		self.observation_space = spaces.MultiDiscrete(obs_shape)
		# logger.info("Observation space: MultiDiscrete: {}".format(obs_shape))
		# logger.info("Observation space: MultiDiscrete: {}".format(obs_label))	
		self.obs_label = obs_label

	def get_observation_space(self):
		return self.observation_space

	def _get_location(self, board, item):
		for col in range(board.cols):
			for row in range(board.rows):
				if board.is_item_type_in_cell(item, col, row):
					return (col, row)
		return (None,None)			

	def get_observation(self, state):
		obs_label_from_state = []  
		#logger.info("State: {}".format(state))
		new_pelican_col,new_pelican_row = self._get_location(self.game.gameBoard, "PELICAN")
		if new_pelican_col is not None:
			self.pelican_col = new_pelican_col
			self.pelican_row = new_pelican_row
		state['pelican_location'] =  {'col': self.pelican_col, 'row': self.pelican_row}

		new_panther_col, new_panther_row = self._get_location(self.game.gameBoard, "PANTHER")
		if new_panther_col is not None:
			self.panther_col = new_panther_col
			self.panther_row = new_panther_row
		state['panther_location'] =  {'col': self.panther_col, 'row': self.panther_row}
		state['madman_status'] = self.game.pelicanPlayer.madmanStatus
		state['sonobuoy_range'] = self.game.sonobuoy_parameters['active_range']


		pelican_payload = self.game.pelicanPlayer.payload
		remaining_sbs = len([obj for obj in pelican_payload if obj.type == "SONOBUOY"])
		remaining_torps = len([obj for obj in pelican_payload if obj.type == "TORPEDO"])
		state['remaining_sonobuoys'] = remaining_sbs
		state['deployed_sonobuoys'] = [{'col': b.col, 'row': b.row, 'state': b.state} for b in self.game.globalSonobuoys]
		state['remaining_torpedoes'] = remaining_torps
		state['torpedo_hunt_enabled'] = self.game.torpedo_parameters['hunt']
		state['torpedo_speeds'] = self.game.torpedo_parameters['speed']
		state['deployed_torpedoes'] = [{'col': t.col, 'row': t.row} for t in self.game.globalTorps]

		obs = []
		# Current game dimensions - fixed per game
		obs += [state['map_width'], state['map_height']]
		obs_label_from_state.append('map_width')
		obs_label_from_state.append('map_height')
		# Remaining turns
		remaining_turns = state['maxTurns'] - state['turn_count']
		obs.append(remaining_turns)
		obs_label_from_state.append('remaining_turns')
		if self.driving_agent == 'pelican':
			# Remaining moves
			remaining_pelican_moves = state['pelican_max_moves']  - state['pelican_move_in_turn'] 
			obs.append(remaining_pelican_moves)
			obs_label_from_state.append('remaining_pelican_moves')
			# Pelican location
			obs += [state['pelican_location']['col'], state['pelican_location']['row']]
			obs_label_from_state.append('pel x')
			obs_label_from_state.append('pel y')
			# Madman status
			obs.append(int(state['madman_status']))
			obs_label_from_state.append('madman_status')
			# Sonobuoy range - fixed per game
			obs.append(state['sonobuoy_range'])
			obs_label_from_state.append('sonobuoy_range')
			# Remaining Sonobuoys
			obs.append(state['remaining_sonobuoys'])
			obs_label_from_state.append('remaining_sonobuoys')
			# sonobuoy locations & activations
			for i in range(self.max_sonobuoys):
				if i < len(state['deployed_sonobuoys']):
					buoy = state['deployed_sonobuoys'][i]
					active = 1 if buoy['state'] == "HOT" else 0
					obs += [buoy['col'], buoy['row'], active]
					obs_label_from_state.append('sb x')
					obs_label_from_state.append('sb y')
					obs_label_from_state.append('sb active')
				else:
					obs += [self.max_grid_width+1, self.max_grid_height+1, 0]
					obs_label_from_state.append('sb x')
					obs_label_from_state.append('sb y')
					obs_label_from_state.append('sb active')

			# Remaining Torpedoes
			obs.append(state['remaining_torpedoes'])
			obs_label_from_state.append('remaining_torpedoes')
			# Torpedo hunt enabled
			obs.append(int(state['torpedo_hunt_enabled']))
			obs_label_from_state.append('torpedo_hunt_enabled')
			# Torpedo speeds per turn
			for i in range (self.max_torpedo_turns):
				if  i < len(state['torpedo_speeds']):
					speed = state['torpedo_speeds'][i]
					obs.append(speed)
					obs_label_from_state.append('tp speed')
				else:
					obs.append(0)
					obs_label_from_state.append('tp speed')

			# torpedo locations & activations
			for i in range(self.max_torpedoes):
				if i < len(state['deployed_torpedoes']):
					torp = state['deployed_torpedoes'][i]
					obs += [torp['col'], torp['row']]
					obs_label_from_state.append('torp x')
					obs_label_from_state.append('torp y')
				else:
					obs += [self.max_grid_width+1, self.max_grid_height+1]
					obs_label_from_state.append('torp x')
					obs_label_from_state.append('torp y')
		else:
			# Remaining moves
			remaining_panther_moves = state['panther_max_moves']  - state['panther_move_in_turn'] 
			obs.append(remaining_panther_moves)
			obs_label_from_state.append('remaining_panther_moves')
			# Pelican location
			obs += [state['pelican_location']['col'], state['pelican_location']['row']]
			obs_label_from_state.append('pel x')
			obs_label_from_state.append('pel y')
			# Panther location
			obs += [state['panther_location']['col'], state['panther_location']['row']]
			obs_label_from_state.append('pan x')
			obs_label_from_state.append('pan y')
			# Madman status
			obs.append(int(state['madman_status']))
			obs_label_from_state.append('madman_status')
			# Sonobuoy range - fixed per game
			obs.append(state['sonobuoy_range'])
			obs_label_from_state.append('sonobuoy_range')
			# Remaining Sonobuoys
			obs.append(state['remaining_sonobuoys'])
			obs_label_from_state.append('remaining_sonobuoys')
			# sonobuoy locations & activations
			for i in range(self.max_sonobuoys):
				if i < len(state['deployed_sonobuoys']):
					buoy = state['deployed_sonobuoys'][i]
					active = 1 if buoy['state'] == "HOT" else 0
					obs += [buoy['col'], buoy['row'], active]
					obs_label_from_state.append('sb x')
					obs_label_from_state.append('sb y')
					obs_label_from_state.append('sb active')
				else:
					obs += [self.max_grid_width+1, self.max_grid_height+1, 0]
					obs_label_from_state.append('sb x')
					obs_label_from_state.append('sb y')
					obs_label_from_state.append('sb active')

			# Remaining Torpedoes
			obs.append(state['remaining_torpedoes'])
			obs_label_from_state.append('remaining_torpedoes')
			# Torpedo hunt enabled
			obs.append(int(state['torpedo_hunt_enabled']))
			obs_label_from_state.append('torpedo_hunt_enabled')

			# Torpedo speeds per turn
			for i in range (self.max_torpedo_turns):
				if  i < len(state['torpedo_speeds']):
					speed = state['torpedo_speeds'][i]
					obs.append(speed)
					obs_label_from_state.append('tp speed')
				else:
					obs.append(0)
					obs_label_from_state.append('tp speed')

			# torpedo locations & activations
			for i in range(self.max_torpedoes):
				if i < len(state['deployed_torpedoes']):
					torp = state['deployed_torpedoes'][i]
					obs += [torp['col'], torp['row']]
					obs_label_from_state.append('torp x')
					obs_label_from_state.append('torp y')
				else:
					obs += [self.max_grid_width+1, self.max_grid_height+1]
					obs_label_from_state.append('torp x')
					obs_label_from_state.append('torp y')

		# logger.info("Observation: {}".format(obs))
		# logger.info("Observation labels: {}".format(obs_label_from_state))
		return obs