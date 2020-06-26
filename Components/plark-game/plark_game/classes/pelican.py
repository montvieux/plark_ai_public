## Pelican class is responsible for controlling the plane game piece in Hunting the Plark 
from .torpedo import Torpedo
from .sonobuoy import Sonobuoy

import os
class Pelican():

	## constructor
	def __init__(self):
		self.payload = []
		self.col = None
		self.row = None
		self.detected = []
		# self.payloadFreeSpace = 24
		self.madmanStatus = False
		self.type = "PELICAN"

	def setLocation(self, col, row):
		self.col = col
		self.row = row

	## Responsible for checking if a particular weapon type is in stock.
	## output returns true if type is present, false if none exist.
	def checkWeaponStock(self, capabilityType):
		if capabilityType in self.payload:
			return True
		if capabilityType not in self.payload:
			return False

	## Allows the adding of a torpedo to the payload
	## The only time we are concerned about space restrictions is when we add an item to the payload
	## Therefore monitor only when loading and reject any further items when no space.
	## input : torpedo object
	def addTorpToPayload(self, torpedo):
		self.payload.append(torpedo)
 		# if self.payloadFreeSpace > 2 :
 		# 	self.payload.append(torpedo)
 		# 	self.payloadFreeSpace = self.payloadFreeSpace - 2
	
	## Allows the adding of a sonobuoy to the payload
	## The only time we are concerned about space restrictions is when we add an item to the payload
	## Therefore monitor only when loading and reject any further items when no space.
	## input : sonobuoy object
	def addSonoBouyToPayload(self, sonobuoy):
		## Same as adding torpedos but sonobuoy only takes up one slot.
		self.payload.append(sonobuoy)
		# if self.payloadFreeSpace > 1 :
		# 	self.payload.append(sonobuoy)
		# 	self.payloadFreeSpace = self.payloadFreeSpace - 1
	
	## When a capability is deployed it will need to be removed from the payload.
	## No output, torpedo removed from payload
	def removeTorpFromPayload(self):
		for i in self.payload:
			if i.type == "TORPEDO":
				self.payload.remove(i)
				break
	
	## When a capability is deployed it will need to be removed from the payload.
	## No output, torpedo removed from payload
	def removeSonoBouyFromPayload(self):
		for i in self.payload:
			if i.type == "SONOBUOY":
				self.payload.remove(i)
				break

