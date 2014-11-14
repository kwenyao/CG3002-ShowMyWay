from arduino_communication import Arduino, SerialCommunicator
from ServerSync import Storage
from UserInteraction import Keypad
import constants
import messages
import time

def arduinoHandshake(voiceOutput):
# 	voiceOutput = Voice()
	arduino = Arduino()
	arduino.resetArduino()
	handshake = arduino.handshakeWithArduino()
	if(handshake != "Done"):
		message = messages.HANDSHAKE_FAIL_TEMPLATE.format(code = handshake)
	else:
		message = "Handshake successful"
	print message
	voiceOutput.addToQueue(message, constants.LOW_PRIORITY)
	print "voice out"

def calibrateStep(voiceOutput):
# 	voiceOutput = Voice()
	fileManager = Storage()
	serial = SerialCommunicator()
	data_path = fileManager.getFilePath('data', 'calibration_info.txt')
	data_exist = fileManager.readFromFile(data_path)
	if data_exist is None:
# 		voiceOutput.say(messages.CALIBRATION_START)
		voiceOutput.addToQueue(messages.CALIBRATION_START, constants.LOW_PRIORITY)
		serial.serialWrite('c')
		calibration_info= serial.serialRead()
		print "from serial",
		print calibration_info
		calibration_info_splited = calibration_info.split(' ')
		calibration_info_filtered = []
		for i in range(len(calibration_info_splited)):
			if calibration_info_splited[i] != "":
				calibration_info_filtered.append(calibration_info_splited[i])
		constants.STEP_LENGTH = float(calibration_info_filtered[0])
		constants.WALKING_DEGREE_ERROR = float(calibration_info_filtered[1])
		constants.IR_STAIRS_CONSTANT = float(calibration_info_filtered[2])
		constants.PEAK_ACC_VALUE = float(calibration_info_filtered[3])


		print "step size is " ,
		print constants.STEP_LENGTH, 
		print " m"
		print "orientation degree error is " ,
		print constants.ORIENTATION_DEGREE_ERROR ,
		print " degrees"
		print "IR stairs constant is ",
		print constants.IR_STAIRS_CONSTANT, 
		print " m"
		print constants.PEAK_ACC_VALUE, 
		print " m/s^2"
# 		voiceOutput.say(messages.CALIBRATION_END)
		voiceOutput.addToQueue(messages.CALIBRATION_END, constants.LOW_PRIORITY)
		fileManager.writeListToFile(data_path, calibration_info_filtered)
	else:
		#ser.write('2') #remove after inte with mega
		#ser.readline() #remove after inte with mega
		serial.serialWrite('n')
		constants.STEP_LENGTH = float((fileManager.readFileToList(data_path))[0])
		constants.WALKING_DEGREE_ERROR = float((fileManager.readFileToList(data_path))[1])
		constants.IR_STAIRS_CONSTANT = float((fileManager.readFileToList(data_path))[2])
		constants.PEAK_ACC_VALUE = float((fileManager.readFileToList(data_path))[3])
		serial.serialWrite(str(constants.PEAK_ACC_VALUE))

def getInitialInput(voiceOutput):
# 	voiceOutput = Voice()
	keyInput = Keypad()
	userInput = {}
	confirmation = 0 
	while confirmation != 1:
# 		voiceOutput.say(messages.INPUT_START_BUILDING_NUMBER)
		voiceOutput.addToQueue(messages.INPUT_START_BUILDING_NUMBER, constants.LOW_PRIORITY)
		time.sleep(1)
		userInput['buildingstart'] = keyInput.getKeysInput()
# 		voiceOutput.say(messages.INPUT_START_BUILDING_LEVEL)
		voiceOutput.addToQueue(messages.INPUT_START_BUILDING_LEVEL, constants.LOW_PRIORITY)
		time.sleep(1)
		userInput['levelstart'] = keyInput.getKeysInput()
# 		voiceOutput.say(messages.INPUT_START_NODE)
		voiceOutput.addToQueue(messages.INPUT_START_NODE, constants.LOW_PRIORITY)
		time.sleep(1)
		userInput['start'] = keyInput.getKeysInput()
# 		voiceOutput.say(messages.INPUT_START_CONFIRMATION_TEMPLATE.format(building = userInput.get('buildingstart'),
# 																		  level = userInput.get('levelstart'),
# 																		  start = userInput.get('start')))
		voiceOutput.addToQueue(messages.INPUT_START_CONFIRMATION_TEMPLATE.format(building = userInput.get('buildingstart'),
																		  level = userInput.get('levelstart'),
																		  start = userInput.get('start')), constants.LOW_PRIORITY)
		time.sleep(1)
		confirmation = int(keyInput.getKeysInput())
	confirmation = 0
	while confirmation != 1:
# 		voiceOutput.say(messages.INPUT_END_BUILDING_NUMBER)
		voiceOutput.addToQueue(messages.INPUT_END_BUILDING_NUMBER, constants.LOW_PRIORITY)
		time.sleep(1)
		userInput['buildingend'] = keyInput.getKeysInput()
# 		voiceOutput.say(messages.INPUT_END_BUILDING_LEVEL)
		voiceOutput.addToQueue(messages.INPUT_END_BUILDING_LEVEL, constants.LOW_PRIORITY)
		time.sleep(1)
		userInput['levelend'] = keyInput.getKeysInput()
# 		voiceOutput.say(messages.INPUT_END_NODE)
		voiceOutput.addToQueue(messages.INPUT_END_NODE, constants.LOW_PRIORITY)
		time.sleep(1)
		userInput['end'] = keyInput.getKeysInput()
# 		voiceOutput.say(messages.INPUT_END_CONFIRMATION_TEMPLATE.format(building = userInput.get('buildingend'),
# 																		  level = userInput.get('levelend'),
# 																		  end = userInput.get('end')))
		voiceOutput.addToQueue(messages.INPUT_END_CONFIRMATION_TEMPLATE.format(building = userInput.get('buildingend'),
																		  level = userInput.get('levelend'),
																		  end = userInput.get('end')), constants.LOW_PRIORITY)
		time.sleep(1)
		confirmation = int(keyInput.getKeysInput())
		
# 	voiceOutput.say(messages.INPUT_CONFIRMATION_SUCCESS)
	voiceOutput.addToQueue(messages.INPUT_CONFIRMATION_SUCCESS, constants.LOW_PRIORITY)
	return userInput