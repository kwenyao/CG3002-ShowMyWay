'''
Created on 1 Nov, 2014

@author: Wen Yao
'''
from wifi_trilateration.wifi import Wifi
from UserInteraction import Voice
import math
import time
from Main import stairs_detected

class Guide():
	def __init__(self, PROX_RAD):
		### CONSTANTS ###
		self.STEP_LENGTH
		self.USER_SPEED
		self.STAIR_LIMIT
		self.PROXIMITY_RADIUS = PROX_RAD # in centimeters
		
		### OBJECTS ###
		self.wifi = Wifi()
		self.voiceOutput = Voice()
		
		### CLASS ATTRIBUTES ###
		self.prevBearing
		self.prevStairSensor = 1
		self.stairSensor
		self.headSensor
		self.bearingFaced
		self.stepDetected
		self.lastUpdatedTime
		
		### FLAGS ###
		self.isStairsDetected = False
		self.isUpStairs = False
		self.isDownStairs = False
		
		
	##########################################
	# Functions called by Navigation
	##########################################
	
	def guideUser(self, currCoor, north, apNodes):
		self.receiveDataFromArduino()
		imuCoor = self.updateIMUCoor(currCoor, north)
		wifiCoor = self.wifi.getUserCoordinates(apNodes)
		newCoor = self.estimateCurrentPosition(imuCoor, wifiCoor, north)
		self.warnHeadObstacle()
		self.warnStairs()
		
		
	def checkLocation(self, currCoor, nextCoor):
		########## NOT DONE YET ########## 
		if (abs(currCoor[0]-nextCoor[0]) < self.PROXIMITY_RADIUS and 
			abs(currCoor[1]-nextCoor[1]) < self.PROXIMITY_RADIUS):
			current_node = next_node_to_travel
			if current_node == final_node :
				break
			next_node_to_travel = route_nodes.get((current_node.get('linkTo'))[0])
			nextCoor = (int(next_node_to_travel.get('x')), int(next_node_to_travel.get('y')))
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
				dist_to_next_node = math.sqrt((nextCoor[0] - currCoor[0])**2 + (nextCoor[1] - currCoor[1])**2)
				num_steps_to_next = dist_to_next_node/(STEP_LENGTH*100)
				print "                                           walk forward" , int(num_steps_to_next) , "steps"
				voice_command.say("walk forward " + str(int(num_steps_to_next)) + " steps")
				tick_since_last = time.time()
	
		prev_bearing = bearing_faced
		print "final coordinate is ", 
		print final_coor
		print "You have reach your desitnation"
		
	##########################################
	# Helper Functions
	##########################################
	
	def receiveDataFromArduino(self):
		dataReceived = (keypad_mich.returnSerial()).readline()
		dataSplited = dataReceived.split(' ')
		dataFiltered = []
		for i in range(len(dataSplited)):
			if dataSplited[i] != "":
				dataFiltered.append(dataSplited[i])
		self.headSensor = float(dataFiltered[0])
		self.stairSensor = float(dataFiltered[1])
		self.bearingFaced = float(dataFiltered[2])
		self.stepDetected = float(dataFiltered[3])
	
	def updateIMUCoor(self, currCoor, north):
		if (self.stepDetected == 1 and 
			abs(self.bearingFaced - self.prevBearing) < 30 and 
			self.isStairsDetected == False):
			imu_new_x = (currCoor[0] + self.STEP_LENGTH * 100 * 
						 math.sin((self.bearingFaced - north) /180 * math.pi))
			imu_new_y = (currCoor[1] + self.STEP_LENGTH * 100 *
						 math.cos((self.bearingFaced - north) / 180 * math.pi))
			return [imu_new_x, imu_new_y]
		else:
			if (self.stepDetected == 1 and abs(self.bearingFaced - self.prevBearing) >= 30):
				print "steps detected but not taken due to turn being made"
			if (self.stepDetected == 1 and self.isStairsDetected == True):
				print "steps detected but not taken due to stairs detected."
			return currCoor
		
	def estimateCurrentPosition(self, imuCoor, wifiCoor, north):
		currCoor = []
		timeElapsed = time.time() - self.lastUpdatedTime
		approx_x_travelled = (timeElapsed * self.USER_SPEED * 
							  math.sin((self.bearingFaced - north) / 180 * math.pi))
		approx_y_travelled = (timeElapsed * self.USER_SPEED * 
							  math.cos((self.bearingFaced - north) / 180 * math.pi))
	
		if (approx_x_travelled+currCoor[0] <= wifiCoor[0] ):
			if (approx_y_travelled+currCoor[1] <= wifiCoor[1]):
				currCoor[0] = (imuCoor[0] + wifiCoor[0])/2
				currCoor[1] = (imuCoor[1] + wifiCoor[1])/2
		else:
			currCoor = imuCoor
		self.lastUpdatedTime = time.time()
		return currCoor
		
	def warnHeadObstacle(self):
		if self.headSensor != 0:
			message = "obstacle at head level " + str(self.headSensor) + " meters away"
			print message
			self.voiceOutput.say(message)
	
	def warnStairs(self):
		if self.stairSensor - self.prevStairSensor > self.STAIR_LIMIT:
			if self.isUpStairs:
				self.isStairsDetected ^= True
				self.isUpStairs ^= True
			else:
				self.isStairsDetected ^= True
				self.isDownStairs ^= True
			self.voiceOutput.say("Downward stairs detected")
		elif self.stairSensor - self.prevStairSensor < -self.STAIR_LIMIT:
			if self.isDownStairs:
				self.isStairsDetected ^= True
				self.isDownStairs ^= True
			else:
				self.isStairsDetected ^= True
				self.isUpStairs ^= True
			self.voiceOutput.say("Upward stairs detected")
		self.prevStairSensor = self.stairSensor
	
	