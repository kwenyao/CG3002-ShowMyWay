import sys
from wifi import Wifi
from ServerSync import MapSync


def getCache():
	currmap = MapSync()
	user_input = raw_input("Map: ")
	user_input2 = raw_input("Level: ")
	location = str(user_input)+str(user_input2)
	return currmap.getFromCache(location)

def main():
	currmap = MapSync()
	wifi = Wifi()

	currmap.downloadAllMaps()
	currmap.reloadAllMaps()
	packet = getCache()
	# print packet
	apNodes = packet['wifi']

	# north = currmap.getNorth()
	# mapNodes = currmap.getMap()
	# apNodes = currmap.getAPNodes()

	coords = wifi.getUserCoordinates(apNodes)
	print coords

if __name__ == "__main__":
	main()