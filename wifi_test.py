from wifi_trilateration.wifi import Wifi
from ServerSync import MapSync
import time
import constants

def main():
	print constants.STEP_LENGTH
	constants.STEP_LENGTH = 1
	print constants.STEP_LENGTH
	currmap = MapSync()
	wifi = Wifi()
	
	currmap.loadLocation("DemoBuilding" , "1")
# 	currmap.loadLocation("COM1", "2")
	
	# print packet
# 	apNodes = packet.get('wifi')
	
	north = currmap.north
	mapNodes = currmap.mapNodes
	apNodes = currmap.apNodes
	
	
# 	timeout = time.time() + 60*2
# 	while True:
# 		if time.time() > timeout:
# 			break
# 		coords = wifi.getUserCoordinates(apNodes)
# 		print coords

if __name__ == "__main__":
	main()