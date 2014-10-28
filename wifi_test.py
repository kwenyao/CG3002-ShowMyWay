from wifi import Wifi
from ServerSync2 import MapSync
import time


def main():
	currmap = MapSync()
	wifi = Wifi()
	
	currmap.loadLocation("DemoBuilding" , "1")
	currmap.loadLocation("COM1", "2")
	
	# print packet
# 	apNodes = packet.get('wifi')
	
	north = currmap.north
	mapNodes = currmap.mapNodes
	apNodes = currmap.apNodes
	
	
	coords = wifi.getUserCoordinates(apNodes)
# 	timeout = time.time() + 60*2
# 	while True:
# 		if time.time() > timeout:
# 			break
# 		coords = wifi.getUserCoordinates(apNodes)
# 		print coords

if __name__ == "__main__":
	main()