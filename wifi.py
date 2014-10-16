from trilateration2 import TrilaterationCalculation
from accessPoints import AccessPoints

class Wifi():
	def __init__ (self):
		self.defaultUserCoordinate = {'x': -1, 'y': -1}
		
	def getUserCoordinates(self, wifiDict):
		self.ap = AccessPoints()
		self.trilateration = TrilaterationCalculation()

		#For testing#
		# ap_list = [{'address':"29:11:A1:8B:C2", 'essid':"accessPoints-101", 'frequency':"2.41", 'signal': -45, 'distance': self.ap.calculateDistanceFromAP(-45,2.41)},
		# 			 {'address':"9A:22:5B:1C:D4", 'essid':"accessPoints-102", 'frequency':"2.41", 'signal': -56, 'distance': self.ap.calculateDistanceFromAP(-56,2.41)}, 
		# 			 {'address':"F9:33:0A:92:9C", 'essid':"accessPoints-103", 'frequency':"2.41", 'signal': -54, 'distance': self.ap.calculateDistanceFromAP(-54,2.41)}, 
		# 			 {'address':"B1:44:A6:BB:EC", 'essid':"accessPoints-104", 'frequency':"2.41", 'signal': -68, 'distance': self.ap.calculateDistanceFromAP(-68,2.41)}]

		# ap_list = [{'address':"28:93:FE:D3:8B", 'essid':"arc-0241-a", 'frequency':"2.412", 'signal': -35, 'distance': self.ap.calculateDistanceFromAP(-35,2.412)},
		# 			 {'address':"E8:BA:70:52:3B", 'essid':"arc-0205-a", 'frequency':"2.437", 'signal': -61, 'distance': self.ap.calculateDistanceFromAP(-61,2.437)}, 
		# 			 {'address':"E8:BA:70:52:BF", 'essid':"arc-0205-b", 'frequency':"2.462", 'signal': -57, 'distance': self.ap.calculateDistanceFromAP(-57,2.462)}, 
		# 			 {'address':"E8:BA:70:52:1E", 'essid':"arc-0231", 'frequency':"2.41", 'signal': -80, 'distance': self.ap.calculateDistanceFromAP(-80,2.41)}]


		ap_list = self.ap.getAccessPoints()
		ap_list = self.ap.sortAccessPoints(ap_list)
		print "matches: " + str(len(ap_list))

		selection_list = self.ap.determineUsableAp(ap_list, wifiDict)
		
		if not selection_list:
			print "Selection list is empty"
			return self.defaultUserCoordinate
		else:
			print "selection list:"
			print selection_list
			return self.trilateration.determineTrilateration(selection_list)
	