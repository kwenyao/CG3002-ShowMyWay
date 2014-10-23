from ServerSync2 import MapSync,Storage
from wifi import Wifi
import visualiseMap
import getPath
import math
import time
import serial
from UserInteraction import Voice, Keypad

#----------------------------------------------------------------------------------------------------------------------------------------
#FUNCTIONS IMPLEMENTATION
#----------------------------------------------------------------------------------------------------------------------------------------
def handshakeWithArduino(serialPort):
	handshake = 0;
	prev_Tick = time.time()
	current_Tick = time.time()
	time_limit_exceed_flag = 0
	time_limit = 1 #time limit for arduino to respond
	print "enter handshake"
	#handshake with GY87
	while(handshake==0 and time_limit_exceed_flag == 0):
		message = serialPort.readline()
		print "after seiral read"
		if (len(message) == 0 ):
			time_limit_exceed_flag = 1
		else:
			print message
			if message[0] == 'S':
				handshake = 1
				serialPort.write("1")	
	handshake = 0
	while(handshake==0 and time_limit_exceed_flag == 0):
		message = serialPort.readline()
		if (len(message) == 0 ):
			time_limit_exceed_flag = 1
		else:
			print message
			if message[0] == 'D':
				handshake =1
				print "Handshake With GY87 Completed."
	handshake = 0
	#waiting for GY87 values to stabalise.
	while (handshake == 0 and time_limit_exceed_flag == 0) :
		message = serialPort.readline()
		if (len(message) == 0 ):
			time_limit_exceed_flag = 1
		else:
			print message
			if message[0] == 'G':
				handshake = 1

	if time_limit_exceed_flag != 0 :
		return "Fail with exit code " + str(time_limit_exceed_flag)
	else:
		return "Done"

#----------------------------------------------------------------------------------------------------------------------------------------
#VARIABLES
#----------------------------------------------------------------------------------------------------------------------------------------
current_coor = (0, 0)		#current coordinate of the user
wifi_coor = (0,0)
imu_coor = (0,0)
map_north = -1				#bearing of the north given by the map
bearing_faced = 0			#direction that user is facing as determined by the Mega compass, a bearing from north, rotate anti-clockwise
step_direction = []			#queue of directions given by the Mega Accelerometer 
ultrasound_data = []		#list of ultrasound data, each element is a tuple. e.g. sensor_number:distance
current_map = ""
current_floor = ""
start_point = ""
end_point = ""
time_location_last_updated = 0
#----------------------------------------------------------------------------------------------------------------------------------------
#CONSTANTS
#----------------------------------------------------------------------------------------------------------------------------------------
STEP_LENGTH = 0.8 				#length of each step of user, measured in meters
RADIUS_OF_CLOSENESS = 0.3 		#this radius determines the level of closeness we need to get to the node to determine that use is actually at that node
ORIENTATION_DEGREE_ERROR= 5 	#the degree of deviant the user can be wrt to the actual bearing he shld be walking straight to reach the node.
FREQ_INSTRUCTIONS = 5			#the time (in minutes) between consecutive "walk straight" instructions
APRROX_SPEED = 0.8 				#approx speed of user in m/s
#----------------------------------------------------------------------------------------------------------------------------------------
#FLAGS
#----------------------------------------------------------------------------------------------------------------------------------------
ultra_head_obstacle = 0			#set to the dist when object detected
#user_input = 0 				#set to 1 when user presses the keyboard
IR_stairs = 0

#----------------------------------------------------------------------------------------------------------------------------------------
#INITIALISATION PHASE
#----------------------------------------------------------------------------------------------------------------------------------------

#download all maps
currmap = MapSync()
wifi = Wifi()

#create Storage for the step size
file_manager = Storage()

#initialise voice command
#voice_command = Voice()
#keypad_input = Keypad()

ser = serial.Serial('COM13', 115200)
###handshaking with arduino
# handshake_result = handshakeWithArduino(ser)
# if ( handshake_result != "Done"):
# 	print handshake_result
# 	voice_command.say("Handshake Failed with exit code" + handshake_result)
# else:
# 	print "Handshake Successful"
# 	voice_command.say("Handshake with Arduino Successful")

#---------------------------------------------------------Calibrating User Step Size-----------------------------------------------------
#Assumption: this device is specialised for ONE user only, current code will only support one user. 
#Check if calibrated before, if so, read from the text file

data_path = file_manager.getFilePath('data', 'step_length.txt')
data_exist = file_manager.readFromFile(data_path)
if data_exist is None:
	ser.write('2')
	STEP_LENGTH = ser.readline
	file_manager.writeToFile(data_path, str(STEP_LENGTH))
else:
	STEP_LENGTH = float(file_manager.readFromFile(data_path))

#---------------------------------------------------------Get Map Location and initial state of User-------------------------------------
#@@@@@@@@@@@@@@@@@@@@@@@ call a function from voiceoutput class to ask user for building name , level, starting vertex and ending vertex
##### DISCLAIMER: please follow the order stated below when updating start and end locations #####
# 1. voice out 'startup1/2/3/4'
# 2. startloc = keypad_obj.getInput_8()
# 3. voice out 'get_dest'
# 4. dest = keypad_obj.getLocationInput
# 5. keypad_obj.updateLocations(startloc, dest)
# *not tried and tested. changes may have to be made.
#
# to speak a certain string: voice_obj.say('say this')
##################################################################################################

currmap.loadLocation("COM1" , "2")
start_point = '3'
end_point = '1'

#apNodes = packet.get('wifi')

map_north = abs(currmap.north-360) #previous calculation is based on rotating anti clock, current input is based on clockwise, hence need to offset
mapNodes = currmap.mapNodes

#initialise visualisation tool
visual = visualiseMap.visualiseMap(1300,1300)
visual.setMap(mapNodes,0)

#initialise calculate_path object with the current number of vertex
calculate_path = getPath.getPath(mapNodes)

#determine the shortest path to take
calculate_path.formAdjlist(mapNodes)
calculate_path.shortestPath(start_point)
route = calculate_path.routeToTravel(start_point, end_point)


#include path to be taken in visualisation tool
route_nodes = visual.getRouteNodes(mapNodes, route)
visual.setMap(route_nodes,1)

#see the map
#visual.printMap()

#initialise starting coordinate and ending coordinate, next node to travel to.
current_node = route_nodes.get(start_point) #gets reassign to the next node once i reach the next node
curr_coor = (int(current_node.get('x')), int(current_node.get('y'))) #current coordinate of user 
time_location_last_updated = time.time()
final_node = route_nodes.get(end_point)
final_coor = (int(final_node.get('x')), int(final_node.get('y')))
next_node_to_travel = route_nodes.get((current_node.get('linkTo'))[0])
next_coor = (int(next_node_to_travel.get('x')), int(next_node_to_travel.get('y')))

#declare variables
offset = -1 			#the degrees to offset based on the movement to be make 
bearing_to_face = -1 	#the bearing user should face to walk straight to reach the next point
ticks_since_last = time.time()	#the timing that the last instruction for walk straight is issued, initialised to the time pi is started up
current_tick = time.time()		#current time 	
dist_to_next_node = -1 	#the distance to the next node
num_steps_to_next = -1 	#number of steps to the next node





#----------------------------------------------------------------------------------------------------------------------------------------
#GUIDING PHASE
#----------------------------------------------------------------------------------------------------------------------------------------
#condition to exit navigation is when user reaches within 30cm of the end coordinate 
while abs(curr_coor[0]-final_coor[0]) >RADIUS_OF_CLOSENESS*100 and abs(curr_coor[1]-final_coor[1]) > RADIUS_OF_CLOSENESS*100 :

#---------------------------------------------------------Receiving Data From Arduino----------------------------------------------------
	dataReceived = ser.readline()
	dataSplited = dataReceived.split(' ')
	dataSplited.pop(0)
	ultra_head_obstacle = dataSplited[0]
	IR_stairs = dataSplited[1]
	bearing_faced = dataSplited[2]


#---------------------------------------------------------Calculate current position from IMU---------------------------------------------
	if (bearing_faced != -1) :
		imu_new_x = curr_coor[0] + STEP_LENGTH * math.cos(bearing_faced)
		imu_new_y = curr_coor[1] + STEP_LENGTH * math.cos(bearing_faced)
		imu_coor = (imu_new_x, imu_new_y)

#---------------------------------------------------------Calculate current position from Wifi-trilateration-----------------------------
	wifi_coor = wifi.getUserCoordinates(currmap.apNodes)


#---------------------------------------------------------Get Optimal current position---------------------------------------------------
	time_lapse = time.time() - time_location_last_updated
	approx_x_travelled = time_lapse*APRROX_SPEED*math.cos(bearing_faced)
	approx_y_travelled = time_lapse*APRROX_SPEED*math.sin(bearing_faced)

	if (approx_x_travelled+curr_coor[0] >= wifi_coor[0] ):
		if (approx_y_travelled+curr_coor[1] >= wifi_coor[1]):
			curr_coor[0] = (imu_coor[0] + wifi_coor[0])/2
			curr_coor[1] = (imu_coor[1] + wifi_coor[1])/2
	else:
		curr_coor = imu_coor
	time_location_last_updated = time.time()

#---------------------------------------------------------Directing----------------------------------------------------------------------

	tick_since_last = time.time() # get the current time here.

	curr_coor = curr_coor
	#check if i have reach the next node
	if (abs(curr_coor[0]-next_coor[0]) <RADIUS_OF_CLOSENESS*100 and abs(curr_coor[1]-next_coor[1]) < RADIUS_OF_CLOSENESS*100) == True:
		current_node = next_node_to_travel
		next_node_to_travel = route_nodes.get((current_node.get('linkTo'))[0])
		next_coor = (int(next_node_to_travel.get('x')), int(next_node_to_travel.get('y')))
		print "you have reached ", current_node["name"]
		#@@@@@@@@@@@@@@@@@@@@@@@call wait function for the talking to finish

	#This block of code checks the bearing user shld face to move forward
	if curr_coor[0] < next_coor[0] : #x-coor increase
		if curr_coor[1] < next_coor[1] : # y-coor increase
			offset = math.degrees(math.atan2((next_coor[0] - curr_coor[0]) ,  (next_coor[1]-curr_coor[1])))
		elif curr_coor[1] == next_coor[1] : # y-coor remains constant
			offset = 90
		elif curr_coor[1] > next_coor[1] : # y-coor decrease
			offset =180 -  math.degrees(math.atan2((next_coor[0] - curr_coor[0]) ,  (curr_coor[1]-next_coor[1])))
	elif curr_coor[0] > next_coor[0] : #x-coor decrease
		if curr_coor[1] < next_coor[1] : # y-coor increase
			offset =360 - math.degrees(math.atan2((curr_coor[0]-next_coor[0]) ,  (next_coor[1]-curr_coor[1])))
		elif curr_coor[1] == next_coor[1] : # y-coor remains constant
			offset = 270
		elif curr_coor[1] > next_coor[1] : # y-coor decrease
			offset =180 + math.degrees(math.atan2((curr_coor[0]-next_coor[0]) ,  (curr_coor[1]-next_coor[1])))
	else: #x-coor remains constant
		if curr_coor[1] < next_coor[1] :
			offset = 360
		else :
			offset = 180
	bearing_to_face = (map_north + offset) % 360		
	print bearing_to_face
	if abs(bearing_to_face - bearing_faced) > ORIENTATION_DEGREE_ERROR:
		if bearing_to_face < bearing_faced:
			print "turn left", bearing_faced - bearing_to_face, "degrees"
		else:
			print "turn right" , bearing_to_face - bearing_faced, " degrees"
		#@@@@@@@@@@@@@@@@@@@@@@@call wait function here, to give user time to rotate	
	else:
		#guide user to walk straight
		if (current_tick - tick_since_last) >= FREQ_INSTRUCTIONS*60:
			time_since_last = current_tick
			dist_to_next_node = math.sqrt((next_coor[0] - curr_coor[0])**2 + (next_coor[1] - curr_coor[1])**2)
			num_steps_to_next = dist_to_next_node/STEP_LENGTH
			print "walk forward" , num_steps_to_next , "steps"

	break		


		

#---------------------------------------------------------Obstacle handling--------------------------------------------------------------
