import sys
from wifi import Wifi
from ServerSync import MapSync


def main():
	MapSync.reloadAllMaps()
	north = MapSync.getNorth()
	mapNodes = MapSync.getMap()
	apNodes = MapSync.getAPNodes() 
	Wifi.getUserCoordinates(apNodes)

if __name__ == "__main__":
	main()