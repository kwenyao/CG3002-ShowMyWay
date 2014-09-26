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

import subprocess
import re
import time
import math
import getMap
import getCoordinates
import simplevector
import ap
import sys


# def calculateDistanceFromAP(signal, freq):
# 	FreeSpaceConstant = 27.55
# 	freq = float(freq)*1000
# 	result = (float(FreeSpaceConstant) - 20*math.log10(float(freq)) - float(signal))/20
# 	distance = math.pow(10,result)
# 	return distance 

# def determineUsableAp(ap_list, wifi_nodes):
# 	selection = []
# 	for j in range(0, len(ap_list)):
# 		if len(selection) >= 3:
# 			break
# 		mac_addr = ap_list[j]['address']
# 		for x in range(1,len(wifi_nodes)):
# 			node = wifi_nodes[str(x)]
# 			if mac_addr == node['macaddr']:
# 				found = {}
# 				found['ap'] = ap_list[j]
# 				found['node'] = node
# 				selection.append(found)
# 				break

# 	return selection # [{ 'ap': AP, 'node': NODE }, {}...]

# def calculateDistanceFromCoordinates(coord_A, coord_B):
# 	return (coord_A - coord_B).magnitude


# def determineWithinCircle(x, y, r, x_1, y_1):
# 	return (math.pow(x-x_1,2) + math.pow(y-y_1,2) - math.pow(r,2)) <= 0.2 #tolerance

# def determineCoordinatesInAllCircles(list_of_coordinates,circles):
# 	coordinates = []
# 	for coord_tuple in list_of_coordinates:
# 		for coord in coord_tuple:
# 			count = 0
# 			for circle in circles:
# 				if determineWithinCircle(circle['x'],circle['y'],circle['dist'],coord[0],coord[1]):
# 					count += 1
# 				if count >= len(circles):
# 					coordinates.append(coord)
# 					break
				
# 	return coordinates

def determineCircles(selection_list):
	circles = []
	for selection in selection_list:
		x = float(selection['node']['x'])
		y = float(selection['node']['y'])
		dist = selection['ap']['distance']
		circle = {}
		circle['x'] = x
		circle['y'] = y
		circle['dist'] = dist
		circles.append(circle)
	return circles

# def determineIntersectionCoordinates(circles):
# 	found_coordinates = []
# 	for j in range(0, len(circles)-1):
# 		circleA = circles[j]
# 		for k in range(j+1, len(circles)):
# 			circleB = circles[k]
# 			coordinates = []
# 			a_x = circleA['x']
# 			a_y = circleA['y']
# 			dist_a = circleA['dist']
# 			pA = simplevector.Vector2d(a_x,a_y)

# 			b_x = circleB['x']
# 			b_y = circleB['y']
# 			dist_b = circleB['dist']
# 			pB = simplevector.Vector2d(b_x,b_y)

# 			coordinates = getCoordinates.cc_intersect(pA, dist_a, pB, dist_b)
# 			found_coordinates.append(coordinates)

# 	return found_coordinates

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
	print ap_list
	print '\n'
	print wifi_nodes
	print '\n'
	selection_list = ap.determineUsableAp(ap_list,wifi_nodes)
	print selection_list
	print '\n'
	circles = determineCircles(selection_list)
	print circles
	print '\n'
	list_of_coordinates = getCoordinates.determineIntersectionCoordinates(circles)
	print list_of_coordinates
	print '\n'
	localization_coordinates = getCoordinates.determineCoordinatesInAllCircles(list_of_coordinates,circles)
	print localization_coordinates
	print '\n'
	userLocation = determineLocation(localization_coordinates)
	print userLocation
	print '\n'
	return userLocation
	

# def getWifiData():
# 	proc = subprocess.Popen('iwlist scan 2>/dev/null', shell=True, stdout=subprocess.PIPE, )
# 	stdout_str = proc.communicate()[0]
# 	stdout_list = stdout_str.split('\n')
# 	return stdout_list

# def getAccessPoints(stdout_list):
# 	# essid = []
# 	# address = []
# 	# signal_str = []
# 	# frequency = []
# 	freq1 = 2
# 	ap_list = []
# 	count = 0
# 	ap = {}
# 	for item in stdout_list:
# 		item = item.strip()
# 		match = re.search('Address: (\S+)', item)
# 		if match:
# 			ap['address'] = match.group(1)
# 			# address.append(match.group(1))
# 			count+=1

# 		match = re.search('ESSID:"(\S+)"', item)
# 		if match:
# 			ap['essid'] = match.group(1)
# 			# essid.append(match.group(1))
# 			count+=1

# 		match = re.search('Frequency:(\S+)', item)
# 		if match:
# 			ap['freq'] = match.group(1)
# 			freq1 = match.group(1)
# 			# frequency.append(match.group(1))
# 			count+=1

# 		found = re.search('Signal level=(\S+)',item)
# 		if found:
# 			match = found.group(1).split('/')[0]	
# 			sig = (int(match)/2) - 100
# 			ap['signal'] = sig
# 			# signal_str.append(str(sig) + " dBm")
# 			ap['distance'] = calculateDistanceFromAP(sig,freq1)
# 			count+=1
# 		if count == 4:
# 			ap_list.append(ap)
# 			count = 0
# 			ap = {}
# 	return ap_list

# def getKey(item):
# 	return math.fabs(float(item['signal']))

# def sortAccessPoints(ap_list):
# 	# Sort by signal strength
# 	return sorted(ap_list, key = getKey )

# def getMapNodes(mapObj):
# 	map_nodes = mapObj.getMapNodes()
# 	return map_nodes

# def getWifiNodes(mapObj):
# 	wifi_nodes = mapObj.getWifiNodes()
# 	return wifi_nodes

def initAll():
	mapObj = getMap.getMap()
	mapObj.downloadAllMaps()
	return mapObj

def getAP():
	stdout_list = ap.getWifiData()							#--- Get Wifi data
	ap_list = ap.getAccessPoints(stdout_list)				#--- Get List of Access Points
	ap_list = ap.sortAccessPoints(ap_list)					#--- Sort list of Access Points
	return ap_list

pseudo_ap_list = [{'address':"29:11:A1:8B:C2:D0", 'essid':"ap-101", 'frequency':"2.41", 'signal': -87, 'distance': ap.calculateDistanceFromAP(-87,2.41)}, {'address':"9A:22:5B:1C:D4:5E", 'essid':"ap-102", 'frequency':"2.41", 'signal': -95, 'distance': ap.calculateDistanceFromAP(-95,2.41)}, {'address':"F9:33:0A:92:9C:D9", 'essid':"ap-103", 'frequency':"2.41", 'signal': -90, 'distance': ap.calculateDistanceFromAP(-90,2.41)}, {'address':"B1:44:A6:BB:EC:D0", 'essid':"ap-104", 'frequency':"2.41", 'signal': -90, 'distance': ap.calculateDistanceFromAP(-90,2.41)}]

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
while True:
	user_input = raw_input("Map: ")
	user_input2 = raw_input("Level: ")
	try:
		loca = str(user_input)+user_input2
		packet = mapObj.getFromCache(loca)
		map_nodes = packet['map']
		wifi_nodes = packet['wifi']
		user_input = raw_input("Map Node: ")
		while user_input != "break":
			ap_list = getAP()
			try:
				print map_nodes[str(user_input)]
			except:
				e = sys.exc_info()[0]
				print e
			print "\n"
			print calculateUserLocation(ap_list, wifi_nodes, map_nodes)
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

# py3 = version_info[0] > 2 #creates boolean value for test that Python major version > 2
# if py3:
#   response = input("Please enter coordinates: ")
# else:
#   response = raw_input("Please enter coordinates: ")

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




