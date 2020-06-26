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

class PlarkEnvSonobuoyDeployment(PlarkEnv):
	def __init__(self,config_file_path=None,verbose=False, **kwargs):
		if kwargs is None:
			kwargs = {}
		kwargs['driving_agent'] = 'pelican'
	
		super(PlarkEnvSonobuoyDeployment, self).__init__(config_file_path,verbose, **kwargs)
		if self.driving_agent != 'pelican':
			raise ValueError('This environment only supports pelican')
		
		self.pelican_col = self.env.activeGames[len(self.env.activeGames)-1].pelicanPlayer.col
		self.pelican_row = self.env.activeGames[len(self.env.activeGames)-1].pelicanPlayer.row
  
	def step(self, action):
		
		action = self.ACTION_LOOKUP[action]
		if self.verbose:
			logger.info('Action:'+action)
		gameState,uioutput = self.env.activeGames[len(self.env.activeGames)-1].game_step(action)

		self.status = gameState
		self.uioutput = uioutput 

		reward = 0        
		self.globalSonobuoys = self.env.activeGames[len(self.env.activeGames)-1].globalSonobuoys

		## Reward for droping a sonobuoy 
		if action == 'drop_buoy':
			reward = 1.00

		if len(self.globalSonobuoys) > 1 : 
			sonobuoy = self.globalSonobuoys[-1]
			sbs_in_range = self.env.activeGames[len(self.env.activeGames)-1].gameBoard.searchRadius(sonobuoy.col, sonobuoy.row, sonobuoy.range, "SONOBUOY")
			sbs_in_range.remove(sonobuoy) # remove itself from search results
			
			if len(sbs_in_range) > 0:
				reward = reward - 0.5 
						
		if reward > 1:
			reward = 1
		if reward < -1:
			reward = -1
	
		ob = self._observation()
		
		done = False  
		if self.status in ["PELICANWIN","ESCAPE","BINGO","WINCHESTER"]:
			done = True
			if self.verbose:
				logger.info("GAME STATE IS " + self.status)   
		
		return ob, reward, done, {}
