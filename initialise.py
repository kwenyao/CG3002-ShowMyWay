from arduino_communication import Arduino, SerialCommunicator
from ServerSync import Storage
from UserInteraction import Voice, Keypad
import constants
import messages
import time

def arduinoHandshake():
	voiceOutput = Voice()
	arduino = Arduino()
	handshake = arduino.handshakeWithArduino()
	if(handshake != "Done"):
		message = messages.HANDSHAKE_FAIL_TEMPLATE.format(code = handshake)
	else:
		message = "Handshake successful"
	print message
	# voiceOutput.say(message)

def calibrateStep():
	voiceOutput = Voice()
	fileManager = Storage()
	serial = SerialCommunicator()
	data_path = fileManager.getFilePath('data', 'calibration_info.txt')
	data_exist = fileManager.readFromFile(data_path)
	if data_exist is None:
		voiceOutput.say(messages.CALIBRATION_START)
		calibration_info= serial.serialRead()
		calibration_info_splited = calibration_info.split(' ')
		calibration_info_filtered = []
		for i in range(len(calibration_info_splited)):
			if calibration_info_splited[i] != "":
				calibration_info_filtered.append(dataSplited[i])
		constants.STEP_LENGTH = float(calibration_info_filtered[0])
		constants.ORIENTATION_DEGREE_ERROR = float(calibration_info_filtered[1])
		constants.IR_STAIRS_CONSTANT = float(calibration_info_filtered[2])

		print "step size is " + constants.STEP_LENGTH + "m"
		print "orientation degree error is " + constants.ORIENTATION_DEGREE_ERROR + " degrees"
		print "IR stairs constant is " + constants.IR_STAIRS_CONSTANT + "m"
		voiceOutput.say(messages.CALIBRATION_END)
		fileManager.writeListToFile(data_path, calibration_info_filtered)
	else:
		#ser.write('2') #remove after inte with mega
		#ser.readline() #remove after inte with mega
		constants.STEP_LENGTH = (fileManager.readFileToList(data_path))[0]
		constants.ORIENTATION_DEGREE_ERROR = (fileManager.readFileToList(data_path))[1]
		constants.IR_STAIRS_CONSTANT = (fileManager.readFileToList(data_path))[2]
def getInitialInput():
	voiceOutput = Voice()
	keyInput = Keypad()
	userInput = {}
	confirmation = 0 
	while confirmation != 1:
		voiceOutput.say(messages.INPUT_START_BUILDING_NUMBER)
		time.sleep(1)
		userInput['buildingstart'] = keyInput.getKeysInput()
		voiceOutput.say(messages.INPUT_START_BUILDING_LEVEL)
		time.sleep(1)
		userInput['levelstart'] = keyInput.getKeysInput()
		voiceOutput.say(messages.INPUT_START_NODE)
		time.sleep(1)
		userInput['start'] = keyInput.getKeysInput()
		voiceOutput.say(messages.INPUT_START_CONFIRMATION_TEMPLATE.format(building = userInput.get('buildingstart'),
																		  level = userInput.get('levelstart'),
																		  start = userInput.get('start')))
		time.sleep(1)
		confirmation = int(keyInput.getKeysInput())
	confirmation = 0
	while confirmation != 1:
		voiceOutput.say(messages.INPUT_END_BUILDING_NUMBER)
		time.sleep(1)
		userInput['buildingend'] = keyInput.getKeysInput()
		voiceOutput.say(messages.INPUT_END_BUILDING_LEVEL)
		time.sleep(1)
		userInput['levelend'] = keyInput.getKeysInput()
		voiceOutput.say(messages.INPUT_END_NODE)
		time.sleep(1)
		userInput['end'] = keyInput.getKeysInput()
		voiceOutput.say(messages.INPUT_END_CONFIRMATION_TEMPLATE.format(building = userInput.get('buildingend'),
																		  level = userInput.get('levelend'),
																		  end = userInput.get('end')))
		time.sleep(1)
		confirmation = int(keyInput.getKeysInput())
	voiceOutput.say(messages.INPUT_CONFIRMATION_SUCCESS)
	return userInput