from guide import Guide
from path import Path
from visualiseMap import visualiseMap
import constants
import math
import time

class Navigation():
	def __init__(self, mapNodes, north):		
		### OBJECTS ###
		self.visual = visualiseMap(1300,1300)
		self.path = Path(mapNodes)
		self.guide = Guide(self.PROXIMITY_RADIUS)
		
		### CLASS ATTRIBUTES ###
		self.mapNodes = mapNodes
		self.mapNorth = north
		self.currNode
		self.currCoor
		self.nextNode
		self.nextCoor
		self.lastUpdatedTime
		self.destinationNode
		self.destinationCoor
		self.routeNodes
		
		### FUNCTION CALLS ###
		self.visual.setMap(mapNodes,0)
	
	##########################################
	# Functions called by Main
	##########################################
	
	def getRoute(self, start_point, end_point):
		self.path.shortestPath(start_point)
		route = self.path.routeToTravel(start_point, end_point)
		self.routeNodes =  self.getRouteNodes(route)
		self.setAttributes(start_point, end_point)
		if(constants.VISUALISATION):
			self.visual.setMap(self.routeNodes,1)
			self.visual.printMap()
		return self.routeNodes
	
	def beginNavigation(self, apNodes):
		while(abs(self.currCoor[0] - self.destinationCoor[0]) > constants.PROXIMITY_RADIUS or 
			  abs(self.currCoor[1] - self.destinationCoor[1]) > constants.PROXIMITY_RADIUS):
			offset = self.calculateOffset()
			bearingToFace = (self.mapNorth + offset) % 360
			self.currCoor = self.guide.updateCoordinates(self.currCoor, self.north, apNodes)
			self.guide.warnUser()
			if(self.checkLocation()):
				break
			self.guide.checkBearing(bearingToFace, self.currCoor, self.nextCoor)
		self.guide.destinationReached()
			
	##########################################
	# Helper Functions
	##########################################
	
	def getRouteNodes(self, route):
		route_nodes = {}
		for i in range(len(route)):
			route_nodes[route[i]] = self.mapNodes[route[i]]
			if i != len(route)-1:
				route_nodes[route[i]]['linkTo'] = [route[i+1]]
			else:
				del route_nodes[route[i]]['linkTo']
		return route_nodes
	
	def setAttributes(self, start_point, end_point):
		self.currNode = self.route_nodes.get(start_point) 
		self.currCoor = [int(self.currNode.get('x')), int(self.currNode.get('y'))]
		self.destinationNode = self.route_nodes.get(end_point)
		self.destinationCoor = [int(self.destinationNode.get('x')), int(self.destinationNode.get('y'))]
		self.nextNode = self.route_nodes.get((self.currNode.get('linkTo'))[0])
		self.nextCoor = [int(self.nextNode.get('x')), int(self.nextNode.get('y'))]
		self.guide.lastUpdatedTime = time.time()
		
	def calculateOffset(self):
		if self.currCoor[0] < self.nextCoor[0]:
			if self.currCoor[1] < self.nextCoor[1]:
				return math.degrees(math.atan2((self.nextCoor[0] - self.currCoor[0]),
											   (self.nextCoor[1] - self.currCoor[1])))
			elif self.currCoor[1] > self.nextCoor[1]:
				return 180 - math.degrees(math.atan2((self.nextCoor[0] - self.currCoor[0]),
													 (self.currCoor[1] - self.nextCoor[1])))
			else:
				return 90
		elif self.currCoor[0] > self.nextCoor[0]:
			if self.currCoor[1] < self.nextCoor[1]:
				return 360 - math.degrees(math.atan2((self.currCoor[0] - self.nextCoor[0]),
													 (self.nextCoor[1] - self.currCoor[1])))
			elif self.currCoor[1] > self.nextCoor[1]:
				return 180 + math.degrees(math.atan2((self.currCoor[0] - self.nextCoor[0]),  
													 (self.currCoor[1] - self.nextCoor[1])))
			else:
				return 270
		else:
			if self.currCoor[1] < self.nextCoor[1]:
				return 360
			else:
				return 180
			
	def checkLocation(self, bearingToFace):
		if (abs(self.currCoor[0] - self.nextCoor[0]) < constants.PROXIMITY_RADIUS and 
			abs(self.currCoor[1] - self.nextCoor[1]) < constants.PROXIMITY_RADIUS):
			self.currNode = self.nextNode
			if self.currNode == self.destinationNode: # why?!?!
				return True
			self.nextNode = self.routeNodes.get((self.currNodee.get('linkTo'))[0])
			self.nextCoor = (int(self.nextNode.get('x')), int(self.nextNode.get('y')))
			self.guide.userReachedNode(self.currNode)
		self.guide.checkBearing(bearingToFace)
		return False