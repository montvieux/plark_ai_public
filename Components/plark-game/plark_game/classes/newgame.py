from .pelican import Pelican
from .panther import Panther
from .torpedo import Torpedo
from .sonobuoy import Sonobuoy
from .map import Map
from .pil_ui import PIL_UI
from .move import Move
from .pelicanAgent import Pelican_Agent
from .pantherAgent import Panther_Agent
from .pantherAgent_load_agent import Panther_Agent_Load_Agent
from .pelicanAgent_load_agent import Pelican_Agent_Load_Agent
from .observation import Observation
from .explosion import Explosion
import numpy as np
import os
import json
import sys
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Newgame():

	# Python constructor to initialise the players within the gamespace.
	# These are subsequently used throughout the game.
	def __init__(self, game_config, **kwargs):
		self.trained_agents_filepath = '/data/models/'
		self.relative_basic_agents_filepath = '../agents/basic'
		self.import_agents()

		# load the game configurations
		self.load_configurations(game_config, **kwargs)

		# Create required game objects
		self.create_game_objects()

		# Load agents
		relative_basic_agents_filepath = os.path.join(os.path.dirname(__file__), self.relative_basic_agents_filepath)
		relative_basic_agents_filepath = os.path.normpath(relative_basic_agents_filepath)
		
		if self.driving_agent == 'panther':
			if not self.output_view_all:
				self.gamePlayerTurn = "PANTHER"
		
			self.pelicanAgent = load_agent(self.pelican_parameters['agent_filepath'], self.pelican_parameters['agent_name'],relative_basic_agents_filepath,self)

		else:
			if not self.output_view_all:
				self.gamePlayerTurn = "PELICAN"

			self.pantherAgent = load_agent(self.panther_parameters['agent_filepath'], self.panther_parameters['agent_name'],relative_basic_agents_filepath,self)


		# Game state variables
		self.default_game_variables()

		# Create UI objects and render game. This must be the last thing in the __init__
		if self.driving_agent == 'pelican':
			self.render_height = self.pelican_parameters['render_height']
			self.render_width = self.pelican_parameters['render_width']
		else:
			self.render_height = self.panther_parameters['render_height']
			self.render_width = self.panther_parameters['render_width']

		self.reset_game()
		self.render(self.render_width,self.render_height,self.gamePlayerTurn)

	def reset_game(self):
		# Create required game objects
		self.create_game_objects()

		# Game state variables
		self.default_game_variables()

		self.pil_ui = PIL_UI(
			self._state("ALL"),
			self.hexScale,
			self.output_view_all,
			self.sonobuoy_parameters['display_range'],
			self.render_width,
			self.render_height,
			self.sonobuoy_parameters['active_range'],
			self.torpedo_parameters['hunt'],
			self.torpedo_parameters['speed']
		)
		self.phase = "PELICAN"
		self.pelican_illegal_move_streak = 0
		self.panther_illegal_move_streak = 0

		self.render(self.render_width,self.render_height,self.gamePlayerTurn)

	def game_step(self, action):
		if self.phase == "PELICAN":
			# pelican phase
			if self.driving_agent == 'pelican':
				self.illegal_pelican_move = False
				self.clear_status_bar()
				if self.pelican_move_in_turn <= self.pelican_parameters['move_limit'] and action != 'end':
					self.perform_pelican_action(action)
					if self.pelican_move_in_turn < self.pelican_parameters['move_limit']:
						return self.gameState, self.gameBoard.UIOutput(self.gamePlayerTurn)
			else:
				self.pelicanPhase()

			self.phase = "MADMAN"

		# Madman phase
		if self.phase == "MADMAN":
			self.madmanPhase(self.pelicanMove.getMoveList())
			self.phase = "MAYPOLE"

		# Maypole phase
		if self.phase == "MAYPOLE":
			self.maypolePhase()
			self.phase = "PANTHER"

		if self.phase == "PANTHER":
			# Panther phase
			self.driving_agent
			if self.driving_agent == 'panther':
				self.illegal_panther_move = False
				self.clear_status_bar()
				if self.panther_move_in_turn <= self.panther_parameters['move_limit'] and action != 'end':
					self.perform_panther_action(action)
					if self.panther_move_in_turn < self.panther_parameters['move_limit']:
						return self.gameState, self.gameBoard.UIOutput(self.gamePlayerTurn)
			else:
				self.pantherPhase()

			self.phase = "BLOODHOUND"

		if self.phase == "BLOODHOUND":
			if self.gameState != 'ESCAPE':
				# Bloodhound phase
				self.bloodhoundPhase()

				# reset counters for new turn
				self.panther_move_in_turn = 0
				self.panther_illegal_move_streak = 0
				self.pelican_move_in_turn = 0
				self.pelican_illegal_move_streak = 0
				self.pantherMove = Move()
				self.pelicanMove = Move()

				# Check turn limit
				if self.gameState == "Running" :
					if self.turn_count == self.bingo_limit:
						self.gameState = "BINGO"

			self.turn_count = self.turn_count + 1
			self.phase = "PELICAN"

		return self.gameState, self.gameBoard.UIOutput(self.gamePlayerTurn)


	def perform_panther_action(self, panther_action):
		if self.escape_rule:
			if self.pantherPlayer.row == 0:

				if self.pantherPlayer.col % 2 == 0: 
					# If even row
					if panther_action in ['0', '1', '5']: # left up , up ,right up
						self.gameState = "ESCAPE"
						return
				elif self.pantherPlayer.col % 2 != 0: 
					# If odd row
					if panther_action == '1': #  Up
						self.gameState = "ESCAPE"
						return

		if panther_action in ['1', '2', '3', '4', '5', '6']:
			new_col, new_row = self.gameBoard.getNeighbours(int(panther_action), self.pantherPlayer.col, self.pantherPlayer.row)

			if self.gameBoard.withinMap(new_col, new_row):
				self.pantherMove.moveList.append({'col': new_col, 'row':new_row})
				self.gameBoard.moveItem(self.pantherPlayer, new_col, new_row)

				self.panther_move_in_turn = self.panther_move_in_turn + 1

			else:
				self.illegal_panther_move = True
				self.panther_illegal_move_streak += 1
				if self.panther_illegal_move_streak >= self.max_illegal_moves_per_turn:
					logger.warning("Too many illegal moves ({}). Ending panther turn...".format(self.panther_illegal_move_streak))
					self.panther_move_in_turn = self.panther_parameters['move_limit']
				self.update_status_bar('Illegal panther move : Moving outside of game map', 'red')

	def _illegal_pelican_move(self, reason):
		self.illegal_pelican_move = True
		self.pelican_illegal_move_streak += 1
		self.update_status_bar('Illegal pelican move : {}'.format(reason), 'red')
		if self.pelican_illegal_move_streak >= self.max_illegal_moves_per_turn:
			logger.warning("Too many illegal moves ({}). Ending pelican turn...".format(self.pelican_illegal_move_streak))
			self.pelican_move_in_turn = self.pelican_parameters['move_limit']

		
	def perform_pelican_action(self, pelican_action):
		if pelican_action in ['1', '2', '3', '4', '5', '6']:
			new_col, new_row = self.gameBoard.getNeighbours(int(pelican_action), self.pelicanPlayer.col, self.pelicanPlayer.row)

			if self.gameBoard.withinMap(new_col, new_row):
				self.pelicanMove.moveList.append({'col': new_col, 'row':new_row})
				self.gameBoard.moveItem(self.pelicanPlayer, new_col, new_row)

				self.pelican_move_in_turn = self.pelican_move_in_turn + 1

			else:
				self._illegal_pelican_move('Moving outside of game map')

		elif pelican_action == 'drop_buoy':

			# check if sonobuoy is in payload
			if (list(filter(lambda item: (item.type == 'SONOBUOY'), self.pelicanPlayer.payload))):
	
				# check if current hex already contains a sonobuoy
				if self.gameBoard.is_item_type_in_cell('SONOBUOY', self.pelicanPlayer.col, self.pelicanPlayer.row):
					self._illegal_pelican_move('Duplicate sonobuoy')
				else:
					# deploy sonobuoy 
					sb = Sonobuoy(self.sonobuoy_parameters['active_range'])
					sb.setLocation(self.pelicanPlayer.col, self.pelicanPlayer.row)
					sb.setState("COLD")
					self.gameBoard.addItem(sb.col, sb.row, sb)
					self.globalSonobuoys.append(sb)
					self.pelicanPlayer.removeSonoBouyFromPayload()
			else:
				self._illegal_pelican_move('No sonobuoy remaining')

		elif pelican_action == 'drop_torpedo':

			# check if torpedo is in payload
			if (list(filter(lambda item: (item.type == 'TORPEDO'), self.pelicanPlayer.payload))):

				# check if current hex already contains a torpedo
				if self.gameBoard.is_item_type_in_cell('TORPEDO', self.pelicanPlayer.col, self.pelicanPlayer.row):
					self._illegal_pelican_move('Duplicate torpedo')
				else:
					# deploy torpedo
					t = Torpedo(**self.torpedo_parameters)
					t.setLocation(self.pelicanPlayer.col, self.pelicanPlayer.row)
					self.gameBoard.addItem(t.col, t.row, t)
					self.globalTorps.append(t)
					self.pelicanPlayer.removeTorpFromPayload()
			else:
				self._illegal_pelican_move('No torpedo remaining')		


	def madmanPhase(self, pelicanMoves):
		self.pelicanPlayer.madmanStatus = False
		for pelicanMove in pelicanMoves:

			if len(self.gameBoard.searchRadius(pelicanMove['col'], pelicanMove['row'], self.pelican_parameters['madman_range'], "PANTHER")) > 0:
				self.pelicanPlayer.madmanStatus = True
				break


	# Maypole Phase : Responsible for handling the sonobuoy Activations
	def maypolePhase(self):
		for bouy in self.globalSonobuoys:
			if (len(self.gameBoard.searchRadius(bouy.col, bouy.row, bouy.range, 'PANTHER')) > 0):
				bouy.setState('HOT')
			else:
				bouy.setState('COLD')

	def pelicanPhase(self):
		# This is what is called if the panther is the playable agent.
		self.pelicanMove = Move()
		while True:
			pelican_action = self.pelicanAgent.getAction(self._state("PELICAN"))

			self.perform_pelican_action(pelican_action)

			if self.pelican_move_in_turn >= self.pelican_parameters['move_limit'] or pelican_action == 'end':
				break

	def pantherPhase(self):
		# This is what is called if the pelican is the playable agent.
		self.pantherMove = Move()
		while True:
			panther_action = self.pantherAgent.getAction(self._state("PANTHER"))

			self.perform_panther_action(panther_action)
			if self.gameState == 'ESCAPE' or self.panther_move_in_turn >= self.panther_parameters['move_limit'] or panther_action == 'end':
				break

	def bloodhoundPhase(self):
		newGlobalTorps = []
		for t in self.globalTorps:

			# search torpedo range for targets including other torpedos, need to remove the current torpedo from the search
			# results.
			detected = self.gameBoard.searchRadius(t.col, t.row, t.searchRadius, ["PANTHER", "TORPEDO"])
			detected.remove(t)

			# If there are targets in range
			if len(detected) > 0:

				# sort list based on distance from torp closest first
				detected.sort(key=lambda result: self.gameBoard.distance(t.col, t.row, result.col, result.row))

				# Torp in hunting range
				if self.torpedo_parameters['hunt']:
					# create a path to the target
					path = self.gameBoard.get_path(t.col, t.row, detected[0].col, detected[0].row )

					# full path might be longer/shorter than torps movement range only move max range or required range
					if len(path) > 0:
						currentSpeed = t.speed[t.turn - 1]
						if len(path) > currentSpeed:
							path_col = path[currentSpeed - 1]['col']
							path_row = path[currentSpeed - 1]['row']
							self.gameBoard.moveItem(t, path_col, path_row)
						else:
							self.gameBoard.moveItem(t, path[len(path)-1]['col'], path[len(path)-1]['row'])

				# Torp and pelican in same hex
				if detected[0].type == "PANTHER" and ((detected[0].col == t.col) and (detected[0].row == t.row)):

					# add explosion to the board
					e = Explosion()
					e.setLocation(t.col, t.row)
					self.gameBoard.addItem(e.col, e.row, e)

					# remove dead panther and torpedo
					self.gameBoard.removeItem(self.pantherPlayer)
					self.gameBoard.removeItem(t)
					self.gameState = "PELICANWIN"
					break

			# Update torpedo turn counts and remove dead torpedos
			if t.turn >= self.torpedo_parameters['turn_limit']:
				self.gameBoard.removeItem(t)
			else:
				t.turn = t.turn + 1
				newGlobalTorps.append(t)

		self.globalTorps = newGlobalTorps

		#  If winchester rule is in play check there are stil torpedoes available
		if self.winchester_rule:
			if self.gameState == "Running" :
				undeployed_torpedoes = len(	list(filter(lambda item: (item.type == 'TORPEDO'), self.pelicanPlayer.payload)))
				deployed_torpedoes = len(self.globalTorps)
				total_torpedoes = undeployed_torpedoes + deployed_torpedoes
				if total_torpedoes == 0:
					self.gameState = "WINCHESTER"
				
	def update_status_bar(self, message, colour):
		self.status_bar = {
			'message': message,
			'fill': colour
		}

	def clear_status_bar(self):
		self.status_bar = {
			'message': '',
			'fill': None
		}

	def _state(self, view):
		if view not in ['PANTHER','PELICAN','ALL']:
			raise ValueError("View", view, ' is not one of:', str(['PANTHER','PELICAN','ALL']) )

		state = {
			'mapFile': self.gameBoard.UIOutput(view),
			'maxTurns': self.maxTurns,
			'turn_count': self.turn_count,
			'game_state': self.gameState,
			'driving_agent': self.driving_agent,
			'status_bar': self.status_bar,
			# additional parameters needed to create PIL_UI
			'hexScale': self.hexScale,
			'view_all': self.output_view_all,
			'sb_display_range': self.sonobuoy_parameters['display_range'],
			'render_width': self.render_width,
			'render_height': self.render_height,
			'sb_range': self.sonobuoy_parameters['active_range'],
			'torpedo_hunt_enabled': self.torpedo_parameters['hunt'],
			'torpedo_speeds': self.torpedo_parameters['speed'],
			'pelican_loadout': self.pelicanPlayer.payload,
			'map_width': self.map_width ,
			'map_height': self.map_height,
		}

		state['pelican_col'] = self.pelicanPlayer.col 
		state['pelican_row'] = self.pelicanPlayer.row
		state['madman'] = self.pelicanPlayer.madmanStatus
		state['remaining_sonobuoys'] = len([obj for obj in self.pelicanPlayer.payload if obj.type == "SONOBUOY"])
		state['deployed_sonobuoys'] = self.globalSonobuoys
		state['remaining_torpedoes'] = len([obj for obj in self.pelicanPlayer.payload if obj.type == "TORPEDO"])
		state['deployed_torpedoes'] = self.globalTorps	
		
		if view in ['PELICAN', 'ALL'] or self.driving_agent == 'pelican' or self.output_view_all:
			state['pelican_max_moves'] = self.pelican_parameters['move_limit']
			state['pelican_move_in_turn'] = self.pelican_move_in_turn
		
		if view in ['PANTHER', 'ALL'] or self.driving_agent == 'panther':
			state['panther_max_moves'] = self.panther_parameters['move_limit']
			state['panther_move_in_turn'] = self.panther_move_in_turn
			state['panther_col'] = self.pantherPlayer.col 
			state['panther_row'] = self.pantherPlayer.row

		return state

	def render(self, render_width,render_height,view):
		return self.pil_ui.update(self._state(view),render_width,render_height)

	def set_pelican_Payload(self):
		for i in range(self.pelican_parameters['default_torps']):
			t = Torpedo()
			self.pelicanPlayer.addTorpToPayload(t)

		for i in range(self.pelican_parameters['default_sonobuoys']):
			s = Sonobuoy(self.sonobuoy_parameters['active_range'])
			self.pelicanPlayer.addSonoBouyToPayload(s)

	def load_configurations(self, game_config, **kwargs):
		logger.info('kwargs: '+str(kwargs))

		# Game settings
		self.maxTurns = kwargs.get('maximum_turns', game_config['game_settings']['maximum_turns'])
		self.map_width = kwargs.get('map_width', game_config['game_settings']['map_width'])
		self.map_height = kwargs.get('map_height', game_config['game_settings']['map_height'])
		self.driving_agent = kwargs.get('driving_agent', game_config['game_settings']['driving_agent'])
		self.max_illegal_moves_per_turn = kwargs.get('max_illegal_moves_per_turn', game_config['game_settings']['max_illegal_moves_per_turn'])

		# Render settings
		self.hexScale = kwargs.get('hex_scale', game_config['render_settings']['hex_scale'])
		self.output_view_all = kwargs.get('output_view_all', game_config['render_settings']['output_view_all'])
		
		# this is used to override the driving agent when rendering the display
		if self.output_view_all:
			self.gamePlayerTurn = "ALL"

		# Game Rules
		self.bingo_limit = kwargs.get('bingo_limit', game_config['game_rules']['bingo_limit'])
		self.winchester_rule = kwargs.get('winchester_rule', game_config['game_rules']['winchester_rule'])
		self.escape_rule = kwargs.get('escape_rule', game_config['game_rules']['escape_rule'])

		# Pelican settings
		self.pelican_start_col = kwargs.get('pelican_start_col', game_config.get('game_rules', {}).get('pelican', {}).get('start_col', int(self.map_width/2)))
		self.pelican_start_row = kwargs.get('pelican_start_row', game_config.get('game_rules', {}).get('pelican', {}).get('start_row', 0))
		self.pelican_parameters = {
			"move_limit": kwargs.get('pelican_move_limit', game_config['game_rules']['pelican']['move_limit']),
			"agent_filepath": kwargs.get('pelican_agent_filepath', game_config['game_rules']['pelican']['agent_filepath']),
			"agent_name": kwargs.get('pelican_agent_name', game_config['game_rules']['pelican']['agent_name']),
			"madman_range": kwargs.get('madman_range', game_config['game_rules']['pelican']['madman_range']),
			"default_torps": kwargs.get('default_torps', game_config['game_rules']['pelican']['default_torps']),
			"default_sonobuoys": kwargs.get('default_sonobuoys', game_config['game_rules']['pelican']['default_sonobuoys']),
			"render_height" :kwargs.get('pelican_render_height', game_config['game_rules']['pelican']['render_height']),
			"render_width" :kwargs.get('pelican_render_width', game_config['game_rules']['pelican']['render_width'])
		}

		# Torpedo settings
		self.torpedo_parameters = {
			"turn_limit": kwargs.get('torpedos_turn_limit', game_config['game_rules']['torpedo']['turn_limit']),
			"hunt": kwargs.get('torpedos_hunt', game_config['game_rules']['torpedo']['hunt']),
			"speed": kwargs.get('torpedos_speed', game_config['game_rules']['torpedo']['speed']),
			"search_range": kwargs.get('torpedos_search_range', game_config['game_rules']['torpedo']['search_range'])
		}

		# Sonobouy settings
		self.sonobuoy_parameters = {
			"active_range": kwargs.get('sonobuoy_active_range', game_config['game_rules']['sonobuoy']['active_range']),
			"display_range": kwargs.get('display_range', game_config['game_rules']['sonobuoy']['display_range'])
		}

		#Panther settings
		self.panther_start_col = kwargs.get('panther_start_col', game_config.get('game_rules', {}).get('panther', {}).get('start_col', int(self.map_width/2)))
		self.panther_start_row = kwargs.get('panther_start_row', game_config.get('game_rules', {}).get('panther', {}).get('start_row', int(self.map_height - 5)))

		self.panther_parameters = {
			"move_limit": kwargs.get('panther_move_limit', game_config['game_rules']['panther']['move_limit']),
			"agent_filepath": kwargs.get('panther_agent_filepath', game_config['game_rules']['panther']['agent_filepath']),
			"agent_name": kwargs.get('panther_agent_name', game_config['game_rules']['panther']['agent_name']),
			"render_height" :kwargs.get('panther_render_height', game_config['game_rules']['panther']['render_height']),
			"render_width" :kwargs.get('panther_render_width', game_config['game_rules']['panther']['render_width'])
		}
	
	def import_agents(self):
		#This loads the agents from a default relative_basic_agents_filepath path which is inside the pip module.
		relative_basic_agents_filepath = os.path.join(os.path.dirname(__file__), self.relative_basic_agents_filepath)
		relative_basic_agents_filepath = os.path.normpath(relative_basic_agents_filepath)

		for agent in os.listdir(relative_basic_agents_filepath):
			if os.path.splitext(agent)[1] == ".py":
				# look only in the modpath directory when importing
				oldpath, sys.path[:] = sys.path[:], [relative_basic_agents_filepath]

				try:
					logger.info('Opening agent from:'+relative_basic_agents_filepath+'/'+str(agent))
					module = __import__(agent[:-3])
	
				except ImportError as err:
					raise ValueError("Couldn't import", agent, ' - ', err )
					continue
				finally:    # always restore the real path
					sys.path[:] = oldpath

	
	def create_game_objects(self):
		self.gameBoard = Map(self.map_width, self.map_height)
		self.pantherPlayer = Panther()
		self.pantherMove = Move()  # reset for new turn

		self.pantherPlayer.setLocation(self.panther_start_col, self.panther_start_row)

		self.pelicanPlayer = Pelican()
		self.pelicanMove = Move()  # reset for new turn
		self.set_pelican_Payload()
		
		self.pelicanPlayer.setLocation(self.pelican_start_col, self.pelican_start_row)

		self.gameBoard.addItem(self.pantherPlayer.col, self.pantherPlayer.row, self.pantherPlayer)
		self.gameBoard.addItem(self.pelicanPlayer.col, self.pelicanPlayer.row, self.pelicanPlayer)

	def default_game_variables(self):
		self.id = ""
		self.gameState = "Running"  # Can be "BINGO","Running","PELICANWIN"
		self.turn_count = 0
		self.pelican_move_in_turn = 0
		self.panther_move_in_turn = 0

		self.startTimeStep = 0
		self.currentTimeStep = 0
		self.endTimeStep = 0

		self.globalSonobuoys = []
		self.globalTorps = []

		self.illegal_pelican_move = False
		self.illegal_panther_move = False
		self.status_bar = {
			'message': '',
			'fill': 'red'
		}

def load_agent(file_path, agent_name,basic_agents_filepath,game,**kwargs):
	if '.py' in file_path: # This is the case for an agent in a non standard location or selected throguh web ui. 
			# load python
			file_path = os.path.join(basic_agents_filepath, file_path)
			oldpath, sys.path[:] = sys.path[:], [basic_agents_filepath]
			try:
				module = __import__(file_path.split('/')[-1][:-3])
			except ImportError as err:
				raise ValueError("Couldn't import " + file_path, ' - ', err)
			cls = getattr(module, agent_name)
			logger.info('Playing against:'+agent_name)
			# always restore the real path
			sys.path[:] = oldpath
			return cls()	
	else:
		files = os.listdir(file_path)
		for f in files:
			if '.zip' not in f:
				# ignore non agent files
				pass

			elif '.zip' in f:
				# load model
				metadata_filepath = os.path.join(file_path, 'metadata.json')
				agent_filepath = os.path.join(file_path, f)

				with open(metadata_filepath) as f:
					metadata = json.load(f)
				logger.info('Playing against:'+agent_filepath)	

				observation = None
				image_based = True 
				if 'image_based' in metadata and metadata['image_based'] == False: # If the image_based flag is not present asume image based, if it is there and set to false the set to false.
					image_based = False
					if kwargs is None:
						kwargs = {}
					kwargs['driving_agent'] = metadata['agentplayer'] 
					observation = Observation(game,**kwargs)

				if metadata['agentplayer'] == 'pelican':	
					return Pelican_Agent_Load_Agent(agent_filepath, metadata['algorithm'], observation, image_based)
				elif metadata['agentplayer'] == 'panther':
					return Panther_Agent_Load_Agent(agent_filepath, metadata['algorithm'], observation ,image_based)

			else:
				raise ValueError('no agent found in ', file_path)

