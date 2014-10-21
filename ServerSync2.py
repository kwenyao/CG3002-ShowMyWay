#!/usr/bin/python
import urllib2
import json
import os.path

class MapSync(object):
	def __init__(self):
		### CONSTANTS ###
		self.URL_TEMPLATE = "http://ShowMyWay.comp.nus.edu.sg/getMapInfo.php?Building={building}&Level={level}"
		self.FILE_NAME_TEMPLATE = "{building}_{level}"
		self.SCRIPT_DIR = os.path.dirname(__file__)
		self.STATUS_OK = 200
		self.FILE_EXTENSION = ".txt"
		self.MAP_DIRECTORY = os.path.join(self.SCRIPT_DIR, "maps//")
		self.MAP_LIST_PATH = os.path.join(self.SCRIPT_DIR, "maps/maplist.txt")
		
		### ATTRIBUTES ###
		self.fileManager = Storage()
		self.apNodes = {}
		self.mapNodes = {}
		self.north = 0
		
		self.info = {}
		self.map = {}
		self.wifi = {}
		
		### FUNCTION CALLS ###	
		if not os.path.exists(self.MAP_DIRECTORY):
			os.makedirs(self.MAP_DIRECTORY)			
		self.updateAllMaps()
	
	###################################
	# Functions used by Navigation
	###################################
	
	def getMap(self):
		return self.mapNodes
	
	def getNorth(self):
		return self.north
	
	def getAPNodes(self):
		return self.apNodes
	
	def loadLocation(self, buildingName, levelNum):
		path = self.getFilePath(buildingName, levelNum)
		
		if not os.path.isfile(path):
			self.addNewMap(buildingName, levelNum)
			
		currentMapJSON = self.fileManager.readFromFile(path)
		mapData = json.loads(currentMapJSON)
		self.parseData(mapData)
	
	###################################
	# Functions to add/update maps
	###################################
	
	def updateAllMaps(self):
		buildingJSON = self.fileManager.readFromFile(self.MAP_LIST_PATH)
		if buildingJSON is None:
			return
		else:
			buildings = json.loads(buildingJSON)
			self.refreshMaps(buildings)
	
	def refreshMaps(self, buildings):
		for building in buildings:
			buildingName = building.get('name')
			levelNum = building.get('level')
			data = self.downloadMap(buildingName, levelNum)
			if data is None: # nothing downloaded
				continue
			else:
				filePath = self.getFilePath(buildingName, levelNum) 
				self.fileManager.writeToFile(filePath, json.dumps(data))
					
	def addNewMap(self, buildingName, levelNum):
		# Add building into list
		self.addToMapList(buildingName, levelNum)
		
		# Create new map file
		filePath = self.getFilePath(buildingName, levelNum) 
		data = self.downloadMap(buildingName, levelNum)
		if data is not None:
			self.fileManager.writeToFile(filePath, json.dumps(data))
	
	def addToMapList(self, buildingName, levelNum):
		locationArray = []
		locationJSON = self.fileManager.readFromFile(self.MAP_LIST_PATH)
		if locationJSON == '':
			locationArray = []
		else:
			locationArray = json.loads(locationJSON)
		newLocation = {}
		newLocation['name'] = buildingName
		newLocation['level'] = levelNum
		locationArray.append(newLocation)
		self.fileManager.writeToFile(self.MAP_LIST_PATH, json.dumps(locationArray))
	
	def downloadMap(self, buildingName, levelNum):
		url = self.URL_TEMPLATE.format(building = buildingName, level = levelNum)
		response = urllib2.urlopen(url)
		if response.getcode() == self.STATUS_OK:
			return json.load(response)
		else:
			print "Download Failed: No data available"
			return None
	
	def getFilePath(self, buildingName, levelNum):
		location = self.FILE_NAME_TEMPLATE.format(building = buildingName, level = levelNum)
		filePath = self.MAP_DIRECTORY + location + self.FILE_EXTENSION
		return filePath
	
	###################################
	# Functions for parsing data
	###################################
	
	def parseData(self, data):
		self.separateData(data)
		self.extractNorth()
		self.extractMapNodes()
		self.extractAPNodes()
	
	def separateData(self, data):
		self.info = data.get('info')
		self.map = data.get('map')
		self.wifi = data.get('wifi')
	
	def extractNorth(self):
		self.north = int(self.info.get('northAt'))
	
	def extractMapNodes(self):
		nodeList = {}
		for node in self.map:
			nodeData = {}
			nodeData['name'] = node.get('nodeName')
			nodeData['x'] = node.get('x')
			nodeData['y'] = node.get('y')
			nodeData['linkTo'] = self.extractMapEdges(node.get('linkTo'))
			nodeList[node.get('nodeId')] = nodeData
		self.mapNodes = nodeList
	
	def extractAPNodes(self):
		apNodeList = {}
		for node in self.wifi:
			nodeData = {}
			nodeData['name'] = node.get('nodeName')
			nodeData['x'] = node.get('x')
			nodeData['y'] = node.get('y')
			nodeData['id'] = node.get('nodeId')
			macAddr = node.get('macAddr').upper()
			macAddr = macAddr[0:14]
			apNodeList[macAddr] = nodeData
		self.apNodes = apNodeList
		
	def extractMapEdges(self, linkTo):
		adjNodes = linkTo.split(',')
		edgeList = []
		for node in adjNodes:
			edgeList.append(node)
		return edgeList
		
		
class Storage():
	def writeToFile(self, filename, content):
		f = open(filename, 'w')
		f.write(content)
		f.close()
		
	def isFileExist(self, filename):
		content = ""
		if os.path.isfile(filename) and os.access(filename, os.R_OK):
			return True
		else:
			self.writeToFile(filename, content)  # to recreate a new file
			return False
		
	def readFromFile(self, filename):
		if self.isFileExist(filename):
			f = open(filename, 'r')
			data = f.read()
			f.close()
			return data
		
	def appendToFile(self, filename, content):
		f = open(filename, 'a')
		f.write(content)  # to append on the end of the file
		f.close()
		