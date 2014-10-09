#from pythonwifi.iwlibs import Wireless
#import time
#import os

#wifi = Wireless('wlan0')

#print wifi.getChannelInfo()
#print wifi.getEssid()
#print wifi.getStatistics()
#print wifi.getWirelessName() 
#print wifi.scan()
#string = '/Address:/{a=$5}/ESSID:"rolls"/{print a}'

#address = os.system("iwlist wlan0 scan|awk '"
#print os.system("iwlist wlan0 scan|awk '"+ string + "'")

import getMap
import getCoordinates
import simplevector
import accessPoints
import sys

def determineCircles(selection_list):
	circles = []
	for selection in selection_list:
		x = float(selection['node']['x'])
		y = float(selection['node']['y'])
		dist = selection['accessPoints']['distance']
		circle = {}
		circle['x'] = x
		circle['y'] = y
		circle['dist'] = dist
		circles.append(circle)
	return circles

def determineLocation(coordinates):
	sum_x = 0
	sum_y = 0
	for coordinate in coordinates:
		sum_x += coordinate[0]
		sum_y += coordinate[1]

	mid_x = sum_x/len(coordinates)
	mid_y = sum_y/len(coordinates)

	return simplevector.Vector2d(mid_x,mid_y)

def calculateUserLocation(ap_list, wifi_nodes, map_nodes):
	# calculate mean x and y positions?
	# print ap_list
	# print '\n'
	# print wifi_nodes
	# print '\n'
	selection_list = accessPoints.determineUsableAp(ap_list,wifi_nodes)
	# print selection_list
	# print '\n'
	circles = determineCircles(selection_list)
	# print circles
	# print '\n'
	list_of_coordinates = getCoordinates.determineIntersectionCoordinates(circles)
	# print list_of_coordinates
	# print '\n'
	localization_coordinates = getCoordinates.determineCoordinatesInAllCircles(list_of_coordinates,circles)
	# print localization_coordinates
	# print '\n'
	userLocation = determineLocation(localization_coordinates)
	# print userLocation
	# print '\n'
	return userLocation
	



def initAll():
	mapObj = getMap.getMap()
	mapObj.downloadAllMaps()
	return mapObj

def getAP():
	stdout_list = accessPoints.scanWifiData()							#--- Get Wifi data
	ap_list = accessPoints.getAccessPoints(stdout_list)				#--- Get List of Access Points
	ap_list = accessPoints.sortAccessPoints(ap_list)					#--- Sort list of Access Points
	return ap_list


try:
	mapObj = initAll()

except:
	e = sys.exc_info()[0]
	print e
# packet = mapObj.getFromCache("DemoBuilding1")
# map_nodes = packet['map']
# wifi_nodes = packet['wifi']
# // main code here

# map_nodes = getMapNodes()							#--- Got the nodes from map
# wifi_nodes = getWifiNodes()

# demoBuilding_cache.put('lvl1-map', map_nodes)			#--- Cache the map
# demoBuilding_cache.put('lvl1-wifi', wifi_nodes)			#--- Cache the wifi_nodes

# ap_list = getAP()
# print ap_list

# mapObj.reloadAllMaps()

# // for testing
# print wifi_nodes
pseudo_ap_list = [{'address':"29:11:A1:8B:C2:D0", 'essid':"accessPoints-101", 'frequency':"2.41", 'signal': -87, 'distance': accessPoints.calculateDistanceFromAP(-87,2.41)}, {'address':"9A:22:5B:1C:D4:5E", 'essid':"accessPoints-102", 'frequency':"2.41", 'signal': -95, 'distance': accessPoints.calculateDistanceFromAP(-95,2.41)}, {'address':"F9:33:0A:92:9C:D9", 'essid':"accessPoints-103", 'frequency':"2.41", 'signal': -90, 'distance': accessPoints.calculateDistanceFromAP(-90,2.41)}, {'address':"B1:44:A6:BB:EC:D0", 'essid':"accessPoints-104", 'frequency':"2.41", 'signal': -90, 'distance': accessPoints.calculateDistanceFromAP(-90,2.41)}]

while True:
	user_input = raw_input("Map: ")
	user_input2 = raw_input("Level: ")
	try:
		loca = str(user_input)+user_input2
		packet = mapObj.loadLocation(loca)
		map_nodes = packet['map']
		wifi_nodes = packet['wifi']
		user_input = raw_input("Map Node: ")
		while user_input != "break":
			# ap_list = getAP()
			print "\n"
			try:
				print map_nodes[str(user_input)]
			except:
				e = sys.exc_info()[0]
				print e
			print calculateUserLocation(pseudo_ap_list, wifi_nodes, map_nodes)
			print "\n"
			user_input = raw_input("Map Node: ")
	except:
		e = sys.exc_info()[0]
		print e
		print "\n"
		



# while(1):
# 	print calculateUserLocation(pseudo_ap_list, wifi_nodes, map_nodes)
# 	time.sleep(2)



# p1 = simplevector.Vector2d(3,1)
# p2 = simplevector.Vector2d(0,1)
# r1 = 2
# r2 = 3

# result = getCoordinates.cc_intersect(p1, r1, p2, r2)



# print pseudo_ap_list

# testnode = {}
# testnode['ap'] = "test1"
# testnode['signal'] = -69
# testnode_list = []
# testnode_list.append(testnode)
# testnode['ap'] = "test2"
# testnode['signal'] = -79
# testnode_list.append(testnode)
# print testnode_list




# namespace = 'lvl1-map'
# result = demoBuilding_cache.get(namespace)
# if result:
# 	print result 

# namespace = 'lvl1-wifi'
# result = demoBuilding_cache.get(namespace)
# if result:
# 	print result 


# r = response.split( )


# print getCoordinates.determineIntersectPoint(int(r[0]),int(r[1]),int(r[2]),int(r[3]),int(r[4]),int(r[5]))







# print map_nodes
# for ap in ap_list:
# 	print ap

# print "\n"
# ap_list = sortAccessPoints(ap_list)

# for ap in ap_list:
# 	print ap;


# print essid
# print address
# print signal_str
# print frequency




