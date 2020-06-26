import os, subprocess, time, signal
import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np 
from gym_plark.envs.plark_env import PlarkEnv

import sys
from plark_game import classes

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class PantherEnvReachTop(PlarkEnv):
	def __init__(self,config_file_path=None, verbose=False, **kwargs):
		if kwargs is None:
			kwargs = {}
		kwargs['driving_agent'] = 'panther'
		super(PantherEnvReachTop, self).__init__(config_file_path,verbose, **kwargs)
		
		if self.driving_agent != 'panther':
			raise ValueError('This environment only supports panther')
		
		self.panther_col = self.env.activeGames[len(self.env.activeGames)-1].pantherPlayer.col
		self.panther_row = self.env.activeGames[len(self.env.activeGames)-1].pantherPlayer.row
	
   
	def step(self, action):
		action = self.ACTION_LOOKUP[action]
		if self.verbose:
			logger.info('Action:'+action)
		gameState,uioutput = self.env.activeGames[len(self.env.activeGames)-1].game_step(action)

		self.status = gameState
		self.uioutput = uioutput 

		reward = 0
		
		self.new_panther_col = self.env.activeGames[len(self.env.activeGames)-1].pantherPlayer.col
		self.new_panther_row = self.env.activeGames[len(self.env.activeGames)-1].pantherPlayer.row
				
		if self.new_panther_col == self.panther_col:
			if self.new_panther_row < self.panther_row:
				reward = reward + .5
			else:
				reward = reward - .2
		# Check if odd
		elif self.panther_col % 2 != 0:
			if self.new_panther_row == self.panther_row:
				reward = reward + .5
			else:
				reward = reward - .2
		# Check if even
		elif self.panther_col % 2 == 0:
			if self.new_panther_row < self.panther_row:
				reward = reward + .5
			else:
				reward = reward - .2
			
		if reward > 1:
			reward = 1
		if reward < -1:
			reward = -1  
			
		self.panther_row = self.new_panther_row
		self.panther_col = self.new_panther_col
		
		ob = self._observation()

		done = False 
		
		if self.status == "ESCAPE":
			reward = 1
		if self.status == "PELICANWIN" or self.status == "BINGO" or self.status == "WINCHESTER" or self.status == "ESCAPE": 
			done = True
			if self.verbose:
				logger.info("GAME STATE IS " + self.status)        
		return ob, reward, done, {}
