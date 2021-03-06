from wifi_trilateration.wifi import Wifi
from UserInteraction import Voice
from arduino_communication import SerialCommunicator
import constants
import math
import messages
import time
from numpy import angle

class Guide():
	def __init__(self, voice):		
		### OBJECTS ###
		self.wifi = Wifi()
# 		self.voiceOutput = Voice()
		self.serial = SerialCommunicator()
		self.voiceOutput = voice
		
		### CLASS ATTRIBUTES ###
		self.prevBearing = 0
		self.prevStairSensor = 0
		self.stairSensor = 0
		self.headSensor = 0
		self.bearingFaced = 0
		self.stepDetected = 0
		self.lastUpdatedTime = 0
		self.lastInstructionTime = 0
		self.warningMessage = ""
		self.prevStep = 0
		self.prevAngleVoice = 0
		self.warningStairsCount = 0
		self.lastTurnTime = 0
		### FLAGS ###
		self.isStairsDetected = False
		self.isUpStairs = False
		self.isDownStairs = False
		self.onPlatform = False
		self.rightAfterBearingCheck = False # To allow the walking forward instruction to be triggered directly after bearing is check.
		
		### TIMING ATTRIBUTES FOR STEPS ###
		self.timeSinceLastStep = time.time() - 3 #to ensure that orientation checking will be triggered the first time
		self.timeSinceNoStep = time.time()
		
		### COUNTERS ###
		self.stepsOnPlatform = 0
		
	##########################################
	# Functions called by Navigation
	##########################################
	def updateCoordinates(self, currCoor, north, apNodes, bearingToFace):
		self.receiveDataFromArduino()
		if self.stepDetected > self.prevStep :
			self.timeSinceLastStep = time.time()
		else:
			self.timeSinceNoStep = time.time()
		imuCoor = self.updateIMUCoor(currCoor, north, bearingToFace)
		print "                                    current coor is ",
		print imuCoor
		# wifiCoor = self.wifi.getUserCoordinates(apNodes)
		# newCoor = self.estimateCurrentPosition(imuCoor, wifiCoor, north)
		# return newCoor
		return imuCoor
		
	def warnUser(self, currCoor, mapNorth):
		self.warnHeadObstacle()
		if mapNorth == 50 and (currCoor[0] <4350) and (currCoor[0] > 3700) and (currCoor[1] > 1800) and (currCoor[1] < 2750):   
			self.warnStairs()
			self.guideAlongStairs()
		
	def userReachedNode(self, node):
		message = messages.NODE_REACHED_TEMPLATE.format(node = node['name'])
		print message
# 		self.voiceOutput.say(message,2)
		self.voiceOutput.addToQueue(message, constants.HIGH_PRIORITY)
		
	def userNextNode(self, nextNode):
		message = messages.NEXT_NODE_TEMPLATE.format(node = nextNode['name'])
		print message
		self.voiceOutput.addToQueue(message, constants.HIGH_PRIORITY)
	
	def checkBearing(self, bearingToFace, currCoor, nextCoor):
		bearingOffset = int(abs(bearingToFace - self.bearingFaced))
		angleToTurn = 0
		if ((bearingOffset > constants.ORIENTATION_DEGREE_ERROR) and
			(abs(self.timeSinceLastStep-self.timeSinceNoStep) > constants.TIME_TO_CHECK_BEARING)):
			if bearingToFace < self.bearingFaced:
				if bearingOffset > 180 : 
					message = messages.TURN_TEMPLATE.format(direction = "right", angle = (360 - bearingOffset))
					angleToTurn = 360 - bearingOffset
				else :
					message = messages.TURN_TEMPLATE.format(direction = "left", angle = bearingOffset)
					angleToTurn = bearingOffset
			else:
				if bearingOffset > 180 : 
					message = messages.TURN_TEMPLATE.format(direction = "left", angle = 360 - bearingOffset)
					angleToTurn = 360 - bearingOffset
				else :
					message = messages.TURN_TEMPLATE.format(direction = "right", angle = bearingOffset)
					angleToTurn = bearingOffset
			print message
# 			self.voiceOutput.say(message)
			
			if abs(self.prevAngleVoice - angleToTurn) != 1  and (time.time() - self.lastTurnTime) >= constants.TURN_INSTRUCTION_FREQ: 
				self.voiceOutput.addToQueue(message, constants.HIGH_PRIORITY)
				self.lastTurnTime = time.time()
			self.rightAfterBearingCheck = True
			self.prevAngleVoice = angleToTurn
			
		else: #guide user to walk straight
			if (self.rightAfterBearingCheck == True) or (time.time() - self.lastInstructionTime) >= constants.INSTRUCTIONS_FREQUENCY:
				distToNextNode = math.sqrt((nextCoor[0] - currCoor[0]) ** 2 +
										   (nextCoor[1] - currCoor[1]) ** 2)
				stepsToNextNode = int((distToNextNode/100) / (constants.STEP_LENGTH)) #changed dist from cm to meters 
				message = messages.WALK_FORWARD_TEMPLATE.format(steps = stepsToNextNode)
				print message
# 				self.voiceOutput.say(message)
				self.voiceOutput.addToQueue(message, constants.LOW_PRIORITY)
				self.lastInstructionTime = time.time()
				self.rightAfterBearingCheck = False
		self.prevBearing = self.bearingFaced # Why?!?!
	
	def destinationReached(self):
		message = messages.DESTINATION_REACHED
		print message
# 		self.voiceOutput.say(message,3)
		self.voiceOutput.addToQueue(message, constants.HIGHEST_PRIORITY)
		
	##########################################
	# Helper Functions
	##########################################
	
	def receiveDataFromArduino(self):
		dataReceived = self.serial.serialRead()
		dataSplited = dataReceived.split(' ')
		dataFiltered = []
		for i in range(len(dataSplited)):
			if dataSplited[i] != "":
				dataFiltered.append(dataSplited[i])
		self.headSensor = float(dataFiltered[0])
		self.stairSensor = float(dataFiltered[1])
		self.bearingFaced = (float(dataFiltered[2])-constants.YPR_OFFSET + constants.COMPASS_OFFSET) % 360
		self.stepDetected = float(dataFiltered[3])
	
	def updateIMUCoor(self, currCoor, north, bearingToFace):
		if (self.stepDetected > self.prevStep and 
			abs(self.bearingFaced - self.prevBearing) < constants.WALKING_DEGREE_ERROR and 
			self.isStairsDetected == False):
			print "current bearing to faced is " + str(bearingToFace),
			print "current north is " + str(north)
			print "x increment is " + str(int(constants.STEP_LENGTH * 100 * math.sin((bearingToFace - north) /180.0 * math.pi)))
			imu_new_x = int ((currCoor[0] + constants.STEP_LENGTH * (self.stepDetected - self.prevStep) * 100 *
						 math.sin((bearingToFace - north) /180.0 * math.pi)))
			imu_new_y = int ((currCoor[1] + constants.STEP_LENGTH * (self.stepDetected - self.prevStep) * 100 *
						 math.cos((bearingToFace - north) / 180.0 * math.pi)))
			self.prevStep = self.stepDetected
			return [imu_new_x, imu_new_y]
		else:
			if (self.stepDetected == 1 and abs(self.bearingFaced - self.prevBearing) >= constants.WALKING_DEGREE_ERROR):
				print "steps detected but not taken due to turn being made"
			if (self.stepDetected == 1 and self.isStairsDetected == True):
				print "steps detected but not taken due to stairs detected."
			return currCoor
		
	def estimateCurrentPosition(self, imuCoor, wifiCoor, north):
		currCoor = []
		timeElapsed = time.time() - self.lastUpdatedTime
		approx_x_travelled = (timeElapsed * constants.USER_SPEED * 
							  math.sin((self.bearingFaced - north) / 180.0 * math.pi))
		approx_y_travelled = (timeElapsed * constants.USER_SPEED * 
							  math.cos((self.bearingFaced - north) / 180.0 * math.pi))
	
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
			message = messages.HEAD_OBSTACLE_TEMPLATE.format(distance = self.headSensor)
			print message
# 			self.voiceOutput.say(message)
			self.voiceOutput.addToQueue(message, constants.HIGH_PRIORITY)
	
	def warnStairs(self):
		
		if self.stairSensor - constants.IR_STAIRS_CONSTANT > constants.STAIR_LIMIT:				#downstairs
			if self.isDownStairs is False and self.warningStairsCount >= 5:
				self.isStairsDetected = True
				self.isDownStairs = True
				self.voiceOutput.addToQueue(messages.DOWN_STAIRS, constants.HIGH_PRIORITY)
			else:
				self.warningStairsCount += 1
# 			self.voiceOutput.say(messages.DOWN_STAIRS)
			self.voiceOutput.addToQueue(messages.DOWN_STAIRS, constants.HIGH_PRIORITY)
		elif self.stairSensor - constants.IR_STAIRS_CONSTANT < -constants.STAIR_LIMIT:			#upstairs
			if self.isUpStairs is False and self.warningStairsCount >= 5:
				self.isStairsDetected = True
				self.isUpStairs = True
				self.voiceOutput.addToQueue(messages.UP_STAIRS, constants.HIGH_PRIORITY)
			else:
				self.warningStairsCount += 1
# 			self.voiceOutput.say(messages.UP_STAIRS)		
		else:
			self.isDownStairs = False
			self.isUpStairs = False
			self.isStairsDetected = False
			self.warningStairsCount = 0
			self.onPlatform = True
			
			
# 			print self.stairSensor, 
# 			print self.prevStairSensor, 
# 			print " ",
# 			print constants.STAIR_LIMIT
# 			if self.isDownStairs:
# 				self.isStairsDetected ^= True
# 				self.isDownStairs ^= True
# 				self.onPlatform = True #set to check if user is on platform
# 				self.warningMessage = ""
# 			elif self.isUpStairs is False:
# 				self.isStairsDetected ^= True
# 				self.isUpStairs ^= True
# 				self.warningMessage = messages.UP_STAIRS
# 			self.voiceOutput.say(messages.UP_STAIRS)
# 		#self.prevStairSensor = self.stairSensor
	
	def guideAlongStairs(self):
		if self.stepDetected == 0:
			if (self.isStairsDetected is False) and not (self.isUpStairs and self.isDownStairs):
				#not on stairs
				return
			elif (self.isStairsDetected is True) and self.isUpStairs:
				message = messages.TAKE_ONE_STEP_TEMPLATE.format(direction = "up")
				print "                                           take one step up carefully"
# 				self.voiceOutput.say(message)
				self.voiceOutput.addToQueue(message, constants.HIGH_PRIORITY)
			elif (self.isStairsDetected is True) and self.isDownStairs:
				message = messages.TAKE_ONE_STEP_TEMPLATE.format(direction = "down")
				print "                                           take one step down carefully"
# 				self.voiceOutput.say(message)
				self.voiceOutput.addToQueue(message, constants.HIGH_PRIORITY)
			return
		else:
			#user taking a step
			if self.stepsOnPlatform:
				self.stepsOnPlatform += 1
			if self.stepsOnPlatform >= constants.MAX_ON_PLATFORM_STEPS: #user is not on platform
				self.onPlatform  = False
				self.stepsOnPlatform = 0
			return

		