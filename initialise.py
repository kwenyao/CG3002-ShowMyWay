from arduino_communication import Arduino
from Keypad import keypad
from ServerSync import Storage
from UserInteraction import Voice
import constants
import messages


def arduinoHandshake():
	voiceOutput = Voice()
	arduino = Arduino()
	handshake = arduino.handshakeWithArduino()
	if(handshake != "Done"):
		message = messages.HANDSHAKE_FAIL_TEMPLATE.format(code = handshake)
	else:
		message = "Handshake successful"
	print message
	voiceOutput.say(message)

def calibrateStep():
	voiceOutput = Voice()
	fileManager = Storage()
	data_path = fileManager.getFilePath('data', 'step_length.txt')
	data_exist = fileManager.readFromFile(data_path)
	if data_exist is None:
		#asks user to stand still and initialise the IR sensor, 
		#ser.write('2')
		#IR_stairs= ser.readline()
		voiceOutput.say(messages.CALIBRATION_START)
		ser.write('2')
		constants.STEP_LENGTH = ser.readline()
		print "step size is " + constants.STEP_LENGTH + "cm"
		voiceOutput.say(messages.CALIBRATION_END)
		fileManager.writeToFile(data_path, str(constants.STEP_LENGTH))
	else:
		#ser.write('2') #remove after inte with mega
		#ser.readline() #remove after inte with mega
		constants.STEP_LENGTH = float(fileManager.readFromFile(data_path))

def getInitialInput():
	voiceOutput = Voice()
	keyInput = keypad()
	userInput = {}
	comfirmation = 0 
	while comfirmation != 1:
		voiceOutput.say(messages.INPUT_BUILDING_NUMBER)
		userInput['building'] = keyInput.getKeysInput()
		voiceOutput.say(messages.INPUT_BUILDING_LEVEL)
		userInput['level'] = keyInput.getKeysInput()
		voiceOutput.say(messages.INPUT_START_LOCATION)
		userInput['start'] = keyInput.getKeysInput()
		voiceOutput.say(messages.INPUT_END_LOCATION)
		userInput['end'] = keyInput.getKeysInput()
		voiceOutput.say(messages.INPUT_CONFIRMATION_TEMPLATE.format(building = userInput.get('building'),
																	level = userInput.get('level'),
																	start = userInput.get('start'),
																	end = userInput.get('end')))
		comfirmation = int(keyInput.getKeysInput())
	voiceOutput.say(messages.INPUT_CONFIRMATION_SUCCESS)