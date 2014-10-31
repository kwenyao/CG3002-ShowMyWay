'''
Created on 31 Oct, 2014

@author: Wen Yao
'''

def handshakeWithArduino(serialPort):
	handshake = 0
	time_limit_exceed_flag = 0
	print "enter handshake"
	#handshake with GY87
	while(handshake==0 and time_limit_exceed_flag == 0):
		message = serialPort.readline()
		print "after serial read 1"
		if (len(message) == 0 ):
		#	time_limit_exceed_flag = 1
			print "nth receive at 1"
		else:
			print message
			if message[0] == 'S':
				handshake = 1
				serialPort.write("1")	
	handshake = 0
	while (handshake == 0 and time_limit_exceed_flag == 0) :
		message = serialPort.readline()
		if (len(message) == 0 ):
		#	time_limit_exceed_flag = 1
			print "nth receive at 2"
		else:
			print message
			if message[0] == 'G':
				handshake = 1

	if time_limit_exceed_flag != 0 :
		return "Fail with exit code " + str(time_limit_exceed_flag)
	else:
		return "Done"

def initArduino():
	handshake_result = handshakeWithArduino(keypad_mich.returnSerial())
	if ( handshake_result != "Done"):
		print handshake_result
		voice_command.say("Handshake Failed with exit code" + handshake_result + ", please restart the system")
	else:
		print "Handshake Successful"
		voice_command.say("Handshake with Arduino Successful")

#---------------------------------------------------------Calibrating User Step Size-----------------------------------------------------
#Assumption: this device is specialised for ONE user only, current code will only support one user. 
#Check if calibrated before, if so, read from the text file
def calibrateStep():
	data_path = file_manager.getFilePath('data', 'step_length.txt')
	data_exist = file_manager.readFromFile(data_path)
	if data_exist is None:
		#asks user to stand still and initialise the IR sensor, 
		#ser.write('2')
		#IR_stairs= ser.readline()
		voice_command.say("Running calibration phase, please start walking 10 meters.")
		ser.write('2')
		STEP_LENGTH = ser.readline()
		print "step size is " + STEP_LENGTH
		voice_command.say("Calibration completed. You many start navigating now.")
		file_manager.writeToFile(data_path, str(STEP_LENGTH))
	else:
		#ser.write('2') #remove after inte with mega
		#ser.readline() #remove after inte with mega
		STEP_LENGTH = float(file_manager.readFromFile(data_path))

#---------------------------------------------------------Get Map Location and initial state of User-------------------------------------

comfirmation = 0 
while comfirmation != 1:
	voice_command.voiceOut("startup1")
	current_map = keypad_input.getKeysInput()
	voice_command.voiceOut("startup2")
	current_floor = keypad_input.getKeysInput()
	voice_command.voiceOut("get_startloc")
	start_point = keypad_input.getKeysInput()
	voice_command.voiceOut("get_dest")
	end_point = keypad_input.getKeysInput()
	voice_command.say( "Your building name is " + current_map + " ,level " + current_floor + " , starting location is " + start_point + " ,ending location is " + end_point)
	voice_command.say("press 1 to comfirm, 2 to re-enter again.")
	comfirmation = int(keypad_input.getKeysInput())
voice_command.say("Welcome to Cloud nine navigation system")
