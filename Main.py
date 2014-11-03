from navigation.navigation import Navigation
from ServerSync import MapSync
import initialise

def main():	
	currmap = MapSync()

	initialise.arduinoHandshake()
	initialise.calibrateStep()
	# userInput = initialise.getInitialInput()
	userInput = {'building': '1', 'level': '2', 'start': '1', 'end': '2'}
	currmap.loadLocation(userInput.get('building'), userInput.get('level'))
	apNodes = currmap.apNodes
	
	# map north stored as anti clockwise
	# previous calculation is based on rotating anti clockwise, 
	# current input is based on clockwise, hence need to offset
	map_north = abs(currmap.north-360)
	mapNodes = currmap.mapNodes
	print map_north
	navigate = Navigation(mapNodes, map_north)
	navigate.getRoute(userInput.get('start'), userInput.get('end'))
	navigate.beginNavigation(apNodes)
	
	########################################
	# Calculate current position from IMU
	########################################
		# angle_off = abs(bearingToFace - bearing_faced)
		# if (step_detected == 1 and abs(bearing_faced - prev_bearing) < 20 and stairs_detected == False) :
		# 	if currCoor[0] <= next_coor[0]: #x-coor supposed to increase
		# 		imu_new_x = currCoor[0] + STEP_LENGTH * 100 * math.cos(angle_off/360*PI)
		# 	else:
		# 		imu_new_x = currCoor[0] - STEP_LENGTH * 100 * math.cos(angle_off/360*PI)
	
		# 	if currCoor[1] <= next_coor[1]:
		# 		imu_new_y = currCoor[1] + STEP_LENGTH * 100 * math.sin(angle_off/360*PI)
		# 	else:
		# 		imu_new_y = currCoor[1] - STEP_LENGTH * 100 * math.sin(angle_off/360*PI)
		# 	imuCoor = [imu_new_x, imu_new_y]
		# else:
		# 	if (step_detected == 1 and abs(bearing_faced - prev_bearing) >= 20):
		# 		# print "bb is ",
		# 		# print bearing_faced, 
		# 		# print "    "
		# 		# print prev_bearing
		# 		print "                                          steps detected but not taken due to turn being made"
		# 	imuCoor = currCoor
	
		# 	if (step_detected == 1 and stairs_detected == True):
		# 		print "                                          steps detected but not taken due to stairs detected."
		# 	print "imu coordinate is ",
		# 	print imuCoor

		
if __name__ == "__main__":
	main()
