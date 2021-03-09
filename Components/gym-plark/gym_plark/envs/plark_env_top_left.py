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

class PlarkEnvTopLeft(PlarkEnv):

	def __init__(self,config_file_path=None, verbose=False, **kwargs):
		if kwargs is None:
			kwargs = {}
		kwargs['driving_agent'] = 'pelican'
		super(PlarkEnvTopLeft, self).__init__(config_file_path,verbose,**kwargs)
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

		reward = 0
		self.new_pelican_col = self.env.activeGames[len(self.env.activeGames)-1].pelicanPlayer.col
		self.new_pelican_row = self.env.activeGames[len(self.env.activeGames)-1].pelicanPlayer.row
		
		if self.new_pelican_col == 0: 
			reward = reward + .5 
		if self.new_pelican_row == 0: 
			reward = reward + .5 
		if self.new_pelican_col < self.pelican_col:
			reward = reward + .1
		if self.new_pelican_row < self.pelican_row:
			reward = reward + .1    
		if self.new_pelican_col > self.pelican_col:
			reward = reward - .3
		if self.new_pelican_row > self.pelican_row:
			reward = reward - .3
		
		
		if reward > 1:
			reward = 1
		if reward < -1:
			reward = -1    

		self.pelican_col = self.new_pelican_col 
		self.pelican_row = self.new_pelican_row
	
		ob = self._observation()
		done = False 

		if self.new_pelican_col == 0 and self.new_pelican_row == 0: 
			done = True 
		if self.status == "PELICANWIN" or self.status == "BINGO" or self.status == "WINCHESTER" or self.status == "ESCAPE": 
			done = True
			if self.verbose:
				logger.info("GAME STATE IS " + self.status)        
		return ob, reward, done, {}




