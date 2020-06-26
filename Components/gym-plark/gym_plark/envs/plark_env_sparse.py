import os
import subprocess
import time
import signal
import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

import sys
from plark_game import classes

from gym_plark.envs.plark_env import PlarkEnv

import logging
logger = logging.getLogger(__name__)


class PlarkEnvSparse(PlarkEnv):

	def __init__(self,config_file_path=None, **kwargs):
		super(PlarkEnvSparse, self).__init__(config_file_path, **kwargs)
		
  
	def step(self, action):
		action = self.ACTION_LOOKUP[action]
		if self.verbose:
			logger.info('Action:'+action)
		gameState, uioutput = self.env.activeGames[len(
			self.env.activeGames)-1].game_step(action)
		self.status = gameState
		self.uioutput = uioutput

		ob = self._observation()

		reward = 0
		done = False
		_info = {}

		#  PELICANWIN = Pelican has won
		#  ESCAPE     = Panther has won
		#  BINGO      = Panther has won, Pelican has reached it's turn limit and run out of fuel
		#  WINCHESTER = Panther has won, All torpedoes dropped and stopped running. Panther can't be stopped
		if self.status in ["ESCAPE", "BINGO", "WINCHESTER", "PELICANWIN"]:
			done = True
			if self.verbose:
				logger.info("GAME STATE IS " + self.status)
			if self.status in ["ESCAPE", "BINGO", "WINCHESTER"]:
				if self.driving_agent == 'pelican':
					reward = -1
					_info['result'] = "LOSE"
				elif self.driving_agent == 'panther':
					reward = 1
					_info['result'] = "WIN"
				else:
					raise ValueError('driving_agent not set correctly')
			if self.status == "PELICANWIN":
				if self.driving_agent == 'pelican':
					reward = 1
					_info['result'] = "WIN"
				elif self.driving_agent == 'panther':
					reward = -1
					_info['result'] = "LOSE"
				else:
					raise ValueError('driving_agent not set correctly')

		return ob, reward, done, _info

