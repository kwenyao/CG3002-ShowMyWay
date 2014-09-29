from trilateration import TrilaterationCalculation
from accessPoints import AccessPoints

class Wifi():
	def getUserCoordinates(self, wifiDict):
		ap_list = AccessPoints.getAccessPoints(self)
		ap_list = AccessPoints.sortAccessPoints(ap_list)
		selection_list = AccessPoints.determineUsableAp(ap_list, wifiDict)
		circles = TrilaterationCalculation.determineCircles(selection_list)
		list_of_coordinates = TrilaterationCalculation.determineIntersectionCoordinates(circles)
		localization_coordinates = TrilaterationCalculation.determineCoordinatesInAllCircles(list_of_coordinates, circles)
		userLocation = TrilaterationCalculation.determineLocation(localization_coordinates)
		return userLocation
		
	