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


class PlarkEnvGuidedReward(PlarkEnv):

	def __init__(self,config_file_path=None,verbose=False,  **kwargs):
		super(PlarkEnvGuidedReward, self).__init__(config_file_path,verbose,**kwargs)
		if self.driving_agent != 'pelican':
			raise ValueError('This environment only supports pelican')
		self.pelican_col = self.env.activeGames[len(self.env.activeGames)-1].pelicanPlayer.col
		self.pelican_row = self.env.activeGames[len(self.env.activeGames)-1].pelicanPlayer.row

	def distance(self,x, y):
		if x >= y:
			result = x - y
		else:
			result = y - x
		return result
	
	def step(self, action):
		action = self.ACTION_LOOKUP[action]
		if self.verbose:
			logger.info('Action:'+action)
		gameState,uioutput = self.env.activeGames[len(self.env.activeGames)-1].game_step(action)
		self.status = gameState
		self.uioutput = uioutput 

		reward = 0
		self.new_pelican_col = self.env.activeGames[len(self.env.activeGames)-1].pelicanPlayer.col
		self.new_pelican_row = self.env.activeGames[len(self.env.activeGames)-1].pelicanPlayer.row
		
		self.plark_col = self.env.activeGames[len(self.env.activeGames)-1].pantherPlayer.col
		self.plark_row = self.env.activeGames[len(self.env.activeGames)-1].pantherPlayer.row

		if  self.status == "PELICANWIN":    
			reward = reward + 1.0
		
		## Reward for being directly over the plark    
		if self.new_pelican_col == self.plark_col:
			reward = reward + .6
		if self.new_pelican_row == self.plark_row:
			reward = reward + .6
		
		## Reward for being closer to the plark
		if self.distance(self.new_pelican_col,self.plark_col) < self.distance(self.pelican_col, self.plark_col):
			reward = reward + .4
		else:
			 ## Punish for being further from the plark
			reward = reward - .6
		if self.distance(self.new_pelican_row,self.plark_row) < self.distance(self.pelican_row, self.plark_row):
			reward = reward + .4
		else:
			## Punish for being further from the plark
			reward = reward - .6
					
		if reward > 1:
			reward = 1
		if reward < -1:
			reward = -1
			
		self.pelican_col = self.new_pelican_col
		self.pelican_row = self.new_pelican_row

		ob = self._observation()
		
		
		done = False  
		if self.status == "PELICANWIN" or self.status == "BINGO" or self.status == "WINCHESTER" or self.status == "ESCAPE": 
			done = True
			if self.verbose:
				logger.info("GAME STATE IS " + self.status)   
			if self.status in ["ESCAPE","BINGO","WINCHESTER"]:
				reward = -1      
		return ob, reward, done, {}
	



