import os, subprocess, time, signal
import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np 

import sys
from plark_game import classes

from gym_plark.envs.plark_env import PlarkEnv

import logging
logger = logging.getLogger(__name__)
# logger.setLevel(logging.ERROR)

class PlarkEnvIllegalMove(PlarkEnv):

	def __init__(self,config_file_path=None,verbose=False,  **kwargs):
		super(PlarkEnvIllegalMove, self).__init__(config_file_path,verbose,**kwargs)
		if self.driving_agent != 'pelican':
			raise ValueError('This environment only supports pelican')
		
		self.pelican_col = self.env.activeGames[len(self.env.activeGames)-1].pelicanPlayer.col
		self.pelican_row = self.env.activeGames[len(self.env.activeGames)-1].pelicanPlayer.row
  
	def step(self, action):
		
		action = self.ACTION_LOOKUP[action]
		if self.verbose:
			logger.info('Action:'+action)

		game = self.env.activeGames[len(self.env.activeGames)-1]
		state = game.game_step(action)
		self.status = state['game_state']

		reward = 1       

		game = self.env.activeGames[len(self.env.activeGames) -1]
		if self.driving_agent == 'pelican':
			illegal_move = game.illegal_pelican_move
		else:
			illegal_move = game.illegal_panther_move

		if illegal_move == True:
			reward = -1
						
		ob = self._observation()
		
		done = False  
		if self.status in ["PELICANWIN","ESCAPE","BINGO","WINCHESTER"]:
			done = True
			if self.verbose:
				logger.info("GAME STATE IS " + self.status)   
		
		return ob, reward, done, {}
