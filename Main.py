from navigation import Navigation
from ServerSync import MapSync,Storage
from wifi_trilateration.wifi import Wifi

import Path
import math
import time
import serial
from UserInteraction import Voice, KeypadMich
import Keypad

import initialise


#----------------------------------------------------------------------------------------------------------------------------------------
#FUNCTIONS IMPLEMENTATION
#----------------------------------------------------------------------------------------------------------------------------------------



#----------------------------------------------------------------------------------------------------------------------------------------
#VARIABLES
#----------------------------------------------------------------------------------------------------------------------------------------
currCoor = [0, 0]		#current coordinate of the user
wifiCoor = [0,0]
imuCoor = [0,0]
map_north = -1				#bearing of the north given by the map
bearing_faced = 0			#direction that user is facing as determined by the Mega compass, a bearing from north, rotate anti-clockwise
step_direction = []			#queue of directions given by the Mega Accelerometer 
ultrasound_data = []		#list of ultrasound data, each element is a tuple. e.g. sensor_number:distance
current_map = ""
current_floor = ""
start_point = ""
end_point = ""
time_location_last_updated = 0
IR_stairs = 1
#----------------------------------------------------------------------------------------------------------------------------------------
#CONSTANTS
#----------------------------------------------------------------------------------------------------------------------------------------
STEP_LENGTH = 0.4 				#length of each step of user, measured in meters
RADIUS_OF_CLOSENESS = 0.3 		#this radius determines the level of closeness we need to get to the node to determine that use is actually at that node
ORIENTATION_DEGREE_ERROR= 20 	#the degree of deviant the user can be wrt to the actual bearing he shld be walking straight to reach the node.
FREQ_INSTRUCTIONS = 1			#the time (in minutes) between consecutive "walk straight" instructions
APRROX_SPEED = 0.4 				#approx speed of user in m/s
PI = math.pi
IR_limit = 25
#----------------------------------------------------------------------------------------------------------------------------------------
#FLAGS
#----------------------------------------------------------------------------------------------------------------------------------------
ultra_head_obstacle = 0			#set to the dist when object detected
#user_input = 0 				#set to 1 when user presses the keyboard
stairs_detected = False
up_stairs = False
down_stairs = False

def main():
	### OBJECT CREATION ###
	currmap = MapSync()
	wifi = Wifi()
	file_manager = Storage()
	voice_command = Voice()
	keypad_input = Keypad.keypad()
	keypad_mich = KeypadMich()
	
	currmap.loadLocation(current_map, current_floor)
	apNodes = currmap.apNodes
	#map north stored as anti clockwise
	#previous calculation is based on rotating anti clock, current input is based on clockwise, hence need to offset
	map_north = abs(currmap.north-360)
	mapNodes = currmap.mapNodes
	
	navigate = Navigation(mapNodes, map_north)
	route_nodes = navigate.getRoute(start_point, end_point)
	navigate.beginNavigation()
	
	#declare variables
	offset = -1 			#the degrees to offset based on the movement to be make 
	bearing_to_face = -1 	#the bearing user should face to walk straight to reach the next point
	tick_since_last = 0	#the timing that the last instruction for walk straight is issued, initialised to the time pi is started up
	dist_to_next_node = -1 	#the distance to the next node
	num_steps_to_next = -1 	#number of steps to the next node
	prev_bearing = -1 	#takes the previous orientation for comparison with the current orientation to determine if it's a step
	prev_IR = 1
	
	
	#----------------------------------------------------------------------------------------------------------------------------------------
	#GUIDING PHASE
	#ASUMPTIONS: user will follow instructions given by the machine. 
	#----------------------------------------------------------------------------------------------------------------------------------------
	#condition to exit navigation is when user reaches within 30cm of the end coordinate 
	while (abs(currCoor[0]-final_coor[0]) >RADIUS_OF_CLOSENESS*100 or abs(currCoor[1]-final_coor[1]) > RADIUS_OF_CLOSENESS*100) :
	
	#---------------------------------------------------------calculate bearing to face------------------------------------------------------
		
		print "bearing_to_face is ",
		print bearing_to_face
	
	#---------------------------------------------------------Receiving Data From Arduino----------------------------------------------------
		dataReceived = (keypad_mich.returnSerial()).readline()
		dataSplited = dataReceived.split(' ')
		dataFiltered = []
		for i in range(len(dataSplited)):
			if dataSplited[i] != "":
				dataFiltered.append(dataSplited[i])
		ultra_head_obstacle = float(dataFiltered[0])
		IR_stairs = float(dataFiltered[1])
		bearing_faced = float(dataFiltered[2])
		step_detected = float(dataFiltered[3])
		
		print "bearing faced now: " + str(bearing_faced)
		print "previous coordinate is ", 
		print currCoor
		print "current IR at belt detecting :",
		print IR_stairs
		print "current head ultrasound is :",
		print ultra_head_obstacle
	#---------------------------------------------------------Calculate current position from IMU---------------------------------------------
		# angle_off = abs(bearing_to_face - bearing_faced)
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
		if (step_detected == 1 and abs(bearing_faced - prev_bearing) < 30 and stairs_detected == False) :
			imu_new_x = currCoor[0] + STEP_LENGTH * 100 * math.sin((bearing_faced - map_north)/180*PI)
			imu_new_y = currCoor[1] + STEP_LENGTH * 100 * math.cos((bearing_faced - map_north)/180*PI)
			imuCoor = [imu_new_x, imu_new_y]
		else:
			if (step_detected == 1 and abs(bearing_faced - prev_bearing) >= 30):
				print "                                          steps detected but not taken due to turn being made"
			imuCoor = currCoor
			if (step_detected == 1 and stairs_detected == True):
				print "                                          steps detected but not taken due to stairs detected."
			print "imu coordinate is ",
			print imuCoor
	#---------------------------------------------------------Calculate current position from Wifi-trilateration-----------------------------
		wifiCoor = wifi.getUserCoordinates(currmap.apNodes)
	#	wifiCoor = [0,0]
	
	#---------------------------------------------------------Get Optimal current position---------------------------------------------------
		time_lapse = time.time() - time_location_last_updated
		approx_x_travelled = time_lapse*APRROX_SPEED*math.sin((bearing_faced - map_north)/180*PI)
		approx_y_travelled = time_lapse*APRROX_SPEED*math.cos((bearing_faced - map_north)/180*PI)
	
		if (approx_x_travelled+currCoor[0] <= wifiCoor[0] ):
			if (approx_y_travelled+currCoor[1] <= wifiCoor[1]):
				currCoor[0] = (imuCoor[0] + wifiCoor[0])/2
				currCoor[1] = (imuCoor[1] + wifiCoor[1])/2
		else:
			currCoor = imuCoor
		time_location_last_updated = time.time()
		print "current Coordinate is " ,
		print currCoor
	
	#---------------------------------------------------------Obstacle handling--------------------------------------------------------------
		if ultra_head_obstacle != 0 :
			print "obstacle at head level at ",
			print ultra_head_obstacle,
			print "meters"
			voice_command.say("obstacle at head level at " + str(ultra_head_obstacle) + "meters ahead")
	
	
		if IR_stairs - prev_IR > IR_limit:
			if up_stairs:
				stairs_detected ^= True
				up_stairs ^= True
			else:
				stairs_detected ^= True
				down_stairs ^= True
			print "down_stairs_detected",
			print IR_stairs, 
			print " , "
			print prev_IR
			voice_command.say(" downwards stairs detected")
		elif IR_stairs - prev_IR < -IR_limit:
			if down_stairs:
				stairs_detected ^= True
				down_stairs ^= True
			else:	
				stairs_detected ^= True
				up_stairs ^= True
			print "                                                up_stairs_detected"
			voice_command.say("Upwards stairs detected")
		prev_IR = IR_stairs
	
	
	
	#---------------------------------------------------------Directing----------------------------------------------------------------------
	
		#check if i have reach the next node
		if (abs(currCoor[0]-next_coor[0]) <RADIUS_OF_CLOSENESS*100 and abs(currCoor[1]-next_coor[1]) < RADIUS_OF_CLOSENESS*100) == True:
			current_node = next_node_to_travel
			if current_node == final_node :
				break
			next_node_to_travel = route_nodes.get((current_node.get('linkTo'))[0])
			next_coor = (int(next_node_to_travel.get('x')), int(next_node_to_travel.get('y')))
			print "you have reached ", current_node["name"]
			voice_command.say("you have reached node " + str(current_node["name"]))
	
		if abs(bearing_to_face - bearing_faced) > ORIENTATION_DEGREE_ERROR:
			if bearing_to_face < bearing_faced:
				print "turn left", bearing_faced - bearing_to_face, "degrees"
				voice_command.say("turn left " + str(abs(bearing_faced - bearing_to_face)) + " degrees")
			else:
				print "                                           turn right" , bearing_to_face - bearing_faced, " degrees"
				voice_command.say("turn Right " + str(abs(bearing_faced - bearing_to_face)) + " degrees")
		else:
			#guide user to walk straight
			if (time.time() - tick_since_last) >= FREQ_INSTRUCTIONS*60:
				dist_to_next_node = math.sqrt((next_coor[0] - currCoor[0])**2 + (next_coor[1] - currCoor[1])**2)
				num_steps_to_next = dist_to_next_node/(STEP_LENGTH*100)
				print "                                           walk forward" , int(num_steps_to_next) , "steps"
				voice_command.say("walk forward " + str(int(num_steps_to_next)) + " steps")
				tick_since_last = time.time()
	
		prev_bearing = bearing_faced
		print "final coordinate is ", 
		print final_coor
	print "You have reach your desitnation"
	voice_command.say("You have reached your destination.")
	
		
if __name__ == "__main__":
	main()
