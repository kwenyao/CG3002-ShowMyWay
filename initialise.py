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
	data_path = fileManager.getFilePath('data', 'step_length.txt')
	data_exist = fileManager.readFromFile(data_path)
	if data_exist is None:
		#asks user to stand still and initialise the IR sensor, 
		#ser.write('2')
		#IR_stairs= ser.readline()
		voiceOutput.say(messages.CALIBRATION_START)
		serial.serialWrite('2')
		# weijian to parse the string into individual constants
		constants.STEP_LENGTH = serial.serialRead()
		print "step size is " + constants.STEP_LENGTH + "m"
		voiceOutput.say(messages.CALIBRATION_END)
		fileManager.writeToFile(data_path, str(constants.STEP_LENGTH))
	else:
		#ser.write('2') #remove after inte with mega
		#ser.readline() #remove after inte with mega
		constants.STEP_LENGTH = float(fileManager.readFromFile(data_path))

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