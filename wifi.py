from trilateration2 import TrilaterationCalculation
from accessPoints import AccessPoints

class Wifi():
	def __init__ (self):
		self.defaultUserCoordinate = {'x': -1, 'y': -1}
		
	def getUserCoordinates(self, wifiDict):
		self.ap = AccessPoints()
		self.trilateration = TrilaterationCalculation()

		#For testing#
		# ap_list = [{'address':"29:11:A1:8B:C2", 'essid':"accessPoints-101", 'frequency':"2.41", 'signal': -87, 'distance': self.ap.calculateDistanceFromAP(-87,2.41)},
		# 			 {'address':"9A:22:5B:1C:D4", 'essid':"accessPoints-102", 'frequency':"2.41", 'signal': -95, 'distance': self.ap.calculateDistanceFromAP(-95,2.41)}, 
		# 			 {'address':"F9:33:0A:92:9C", 'essid':"accessPoints-103", 'frequency':"2.41", 'signal': -90, 'distance': self.ap.calculateDistanceFromAP(-90,2.41)}, 
		# 			 {'address':"B1:44:A6:BB:EC", 'essid':"accessPoints-104", 'frequency':"2.41", 'signal': -90, 'distance': self.ap.calculateDistanceFromAP(-90,2.41)}]

		ap_list = self.ap.getAccessPoints()
		ap_list = self.ap.sortAccessPoints(ap_list)
		print "matches: " + str(len(ap_list))

		selection_list = self.ap.determineUsableAp(ap_list, wifiDict)
		
		print "selection: "
		print selection_list
		
		if not selection_list:
			print "Selection list is empty"
			return self.defaultUserCoordinate
		else:
			print "selection list:"
			print selection_list
			return self.trilateration.determineTrilateration(selection_list)
	