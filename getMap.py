#!/usr/bin/python
import sys
import requests
import urllib
import json
import os
import os.path
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

# buildings = [{'name':"DemoBuilding",'level':['1','2','3']}, {'name':"COM1",'level':['1','2','3']} , {'name':"COM2", 'level': ['1','2','3']}]

cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': '/tmp/cache/data',
    'cache.lock_dir': '/tmp/cache/lock'
}


def isFileExist(filename):
	content = ""
	if os.path.isfile(filename) and os.access(filename, os.R_OK):
		return True
	else:
		writeToFile(filename, content) # to recreate a new file
		return False

def readFromFile(filename):
	if isFileExist(filename):
		f = open(filename, 'r')
		data = f.read()
		f.close
		return data

def writeToFile(filename, content):
	f = open(filename, 'w')
	f.write(content)
	f.close()

def appendToFile(filename,content):
	f = open(filename, 'a')
	f.write(content) 					# to append on the end of the file
	f.close()


def extractingLinkToNodes(linkToString):
	linkToString = str(linkToString)
	linkToNodes = []
	linkToNodes = linkToString.split(",")
	linkToNodes2 = []
	for x in linkToNodes:
		node = ""
		for i in x:
			if i.isdigit():
				node += i
		linkToNodes2.append(node)

	return linkToNodes2
	
def determineNorth(info):
	north = str(info['northAt'])
	return north

def determineMapNodes(map_info):
	map_nodes = {}
	for node in map_info:
		node_data = {}
		node_data['name'] = str(node['nodeName'])
		node_data['x'] = str(node['x'])
		node_data['y'] = str(node['y'])
		node_data['linkTo'] = extractingLinkToNodes(node['linkTo'])
		map_nodes[str(node['nodeId'])] = node_data
	return map_nodes

def determineWifiNodes(wifi_info):
	wifi_nodes = {}
	for node in wifi_info:
		node_data = {}
		node_data['name'] = str(node['nodeName'])
		node_data['x'] = str(node['x'])
		node_data['y'] = str(node['y'])
		node_data['id'] = node['nodeId']
		wifi_nodes[str(node['macAddr']).upper()] = node_data
	return wifi_nodes


def determineSource(building_name, level_value):
	# print "Hello World"
	
	url = 'http://showmyway.comp.nus.edu.sg/getMapInfo.php?Building=' + building_name + "&Level=" + level_value 
	# req = requests.request('GET', 'http://showmyway.comp.nus.edu.sg/getMapInfo.php?Building=DemoBuilding&Level=1')
	req = urllib.urlopen(url)
	source = req.read()
	req.close()
	source = json.loads(source)
	return source

# def getMapNodes():
# 	return map_nodes

class getMap(object):
	def __init__(self):
		self.val = 0
		self.info = []
		self.map_info = []
		self.wifi_info = []
		self.map_nodes = {}
		print "created obj"
		cache = CacheManager(**parse_cache_config_options(cache_opts))
		self.cache_manager = cache.get_cache('map.php', expire=3600) 		#--- get specific cache from cacheManager
		try:
			building_json = readFromFile("buildinglist.txt") 
			self.buildings = json.loads(building_json)
			print "building loaded"
		except:
			return

	# def determineMainSource(self, building_name, level_value):
	# 	source = determineSource(building_name,level_value)
	# 	# print "in determineMainSource"
	# 	return source

	def determineAllInfos(self,source):
		self.info = source['info']
		self.map_info = source['map']
		self.wifi_info = source['wifi']
		# print "in determineInfos"

	def extractMapNodes(self):
		map_nodes = determineMapNodes(self.map_info)
		# print "in getMapNodes"
		return map_nodes

	def extractWifiNodes(self):
		wifi_nodes = determineWifiNodes(self.wifi_info)
		return wifi_nodes

	def getInfo(self):
		return determineInfos(self.info)

	def getFromCache(self,request):
		return self.cache_manager.get(request)

	def reloadAllMaps(self):
		writeToFile("buildings.txt", "")
		try:
			building_json = readFromFile("buildinglist.txt") 
			self.buildings = json.loads(building_json)
		except:
			print sys.exc_info()[0]
		self.downloadAllMaps()



	def printAllMaps(self):
		for building in buildings:
			building_name = building['name']
			for lvl in building['level']:
				print self.cache_manager.get(building_name+lvl)			#--- Cache the map
				print "\n"
				

	def downloadAllMaps(self):
		if not isFileExist("buildings.txt") or readFromFile("buildings.txt") == "":
			print "             downloading map"
			array_of_cache = []
			for building in self.buildings:
				building_name = building['name']
				for lvl in building['level']:
					source = determineSource(building_name,lvl)
					self.determineAllInfos(source)
					map_nodes = self.extractMapNodes()							#--- Got the nodes from map
					wifi_nodes = self.extractWifiNodes()
					cache = {}
					cache['map_name'] = building_name+lvl
					cache['map'] = map_nodes
					cache['wifi'] = wifi_nodes
					cache['info'] = self.info
					array_of_cache.append(cache)
					self.cache_manager.put(building_name+lvl, cache)			#--- Cache the map
			appendToFile("buildings.txt",json.dumps(array_of_cache))
		else:
			print "             loading map from storage"
			array_of_cache = readFromFile("buildings.txt")
			array_of_cache = json.loads(array_of_cache)
			for cache in array_of_cache:
				self.cache_manager.put(cache['map_name'], cache)

		print "done caching"		

		# map_nodes = getMapNodes()							#--- Got the nodes from map
		# wifi_nodes = getWifiNodes()
		# demoBuilding_cache.put('lvl1-map', map_nodes)			#--- Cache the map
		# demoBuilding_cache.put('lvl1-wifi', wifi_nodes)			#--- Cache the wifi_nodes

# print map_info
# print "\n"
# 4

# print nodes
# print "\n\n"
# print info
# print "\n\n"
# print map_info 
# print "\n\n"
# print wifi_info

