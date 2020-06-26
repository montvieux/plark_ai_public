from abc import ABC, abstractmethod

class Agent(ABC):
	@abstractmethod
	def getAction(self, game):
		pass

	@abstractmethod
	def action_lookup(self, action):
		pass