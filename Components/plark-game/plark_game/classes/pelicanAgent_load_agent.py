import os
from stable_baselines3 import DQN, PPO, A2C
from .pelicanAgent import Pelican_Agent
import logging
import numpy  as np
from .pil_ui import PIL_UI
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Pelican_Agent_Load_Agent(Pelican_Agent):

	def __init__(self, filepath, algorithm_type, observation = None, imaged_based=True):

		# Can't initialise this until we have game state
		self.pil_ui = None
		self.imaged_based = imaged_based

		if not self.imaged_based: 
			if observation is not None:
				self.observation = observation
			else:
				raise ValueError('Observation object not passed in to load agent.' )

		if os.path.exists(filepath): 
			self.loadAgent(filepath , algorithm_type)
			logger.info('pelican agent loaded')
		else:
			raise ValueError('Error loading pelican agent. File : "' + filepath + '" does not exsist' )

	def loadAgent(self, filepath, algorithm_type ):
		try:
			if algorithm_type.lower() == 'dqn':
				self.model = DQN.load(filepath)
			elif algorithm_type.lower() == 'ppo':
				self.model = PPO.load(filepath)
			elif algorithm_type.lower() == 'a2c':
				self.model = A2C.load(filepath)
		except:
			raise ValueError('Error loading pelican agent. File : "' + filepath + '" does not exsist' )

		
	def getAction(self, state):
		# Eventually this should be replaced by a helper method that doesn't require constructing a class instance
		if not self.pil_ui:
			self.pil_ui = PIL_UI(
				state,
				state['hexScale'],
				state['view_all'],
				state['sb_display_range'],
				state['render_width'],
				state['render_height'],
				state['sb_range'],
				state['torpedo_hunt_enabled'],
				state['torpedo_speeds']
			)

		if self.imaged_based:
			obs = self.pil_ui.update(state)
			obs = np.array(obs, dtype=np.uint8)
		else:
			obs = self.observation.get_observation(state) 
			
		action, _ = self.model.predict(obs, deterministic=False)
		return self.action_lookup(action)



