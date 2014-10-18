from wifi import Wifi
from ServerSync2 import MapSync


def main():
	currmap = MapSync()
	wifi = Wifi()
	
	currmap.loadLocation("COM1", "2")
	
	# print packet
# 	apNodes = packet.get('wifi')
	
	north = currmap.getNorth()
	mapNodes = currmap.getMap()
	apNodes = currmap.getAPNodes()
	
	print north
	print mapNodes
	print apNodes
	
	while(1):
		coords = wifi.getUserCoordinates(apNodes)
		print coords

if __name__ == "__main__":
	main()