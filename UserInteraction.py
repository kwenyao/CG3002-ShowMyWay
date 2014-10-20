import os, time
import serial

class Keypad():
	#################################################################
	# to update start location and destination,						#
	# initalise a string and call getLocationInput() first			#
	# then call updateLocations and pass in the strings				#
	# 																#
	# EXAMPLE (under main):											#
	# startloc = Keypad.getLocationInput()							#
	# dest = Keypad.getLocationInput()								#
	# Keypad.updateLocations(startloc, dest)						#
	#################################################################

	def __init__(self):
		self.voiceOutput = Voice()
		self.step_count = str(5)
		self.startloc = ['0', '0', '0', '0']
		self.dest = ['0', '0', '0', '0']
		self.yninput = 0
		#initialise serial port with Arduino
		self.ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
		self.ser.open()
	
	#user_startloc is a string that must be attained from getLocationInput()
	#user_dest is also a string that must be attained from getLocationInput()
	def updateLocations(self, user_startloc, user_dest):
		for x in range (0, 4):
				self.startloc[x] = user_startloc[x]
				self.dest[x] = user_dest[x]
		print self.startloc
		print self.dest

		self.voiceOutput.messagesObj.updateDictionaryValues(self.startloc, 'startloc')
		self.voiceOutput.messagesObj.updateDictionaryValues(self.dest, 'dest')

	#determine if user pressed 1 for yes or 2 for no.
	#returns user input
	#arbitrarily using '!' symbol as a command to arduino to get yes/no input
	#i.e. read 1 bit from user

	def getYNInput(self):
		##### CHECK THIS PART #####
		print self.voiceOutput.messagesObj.get('yn_inst')
		###########################

		self.voiceOutput.voiceOut('yn_inst')
		self.ser.write("!")
		yn_response = ''
		while (not yn_response):
			yn_response = self.ser.readline()
		self.yninput = yn_response
		return yn_response
	
	#get user input for location. 4 digit number.
	#returns user input but does NOT update dictionary
	def getLocationInput(self):
		self.ser.write(">")
		response = ''
		while (not response):
			response = self.ser.readline()
		return response

class Voice():
	def __init__(self):
		self.messagesObj = Messages()
		self.phrases = self.messagesObj.getPhrases()
		self.messages = self.messagesObj.getMessages()
		self.setupVoice()

		# formatting of syntax and defining speech quality
		self.variation = {'female1': ' -ven+f3', 'female2': ' -ven+f4',
				'male1': ' -ven+m2', 'male2': ' -ven+m3'}
		self.volume = str(100)
		self.syntax_head = 'espeak -s150 -a'
		self.syntax_tail = " ' 2>/dev/null"

	def setupVoice(self):
		# convert audio output to audio jack
		os.system("amixer cset numid=3 1")
	
	#handles user's yes/no input
	def YNHandler(self, yn_response):
		if (yn_response[0] == '1'):
			print self.messages.get('confirm_yes')
			self.voiceOut('confirm_yes')
			return 1
		
		#all other values aside from '1' interpreted as no
		else:
			print self.messages.get('confirm_no')
			self.voiceOut('confirm_no')
			return 0
	
	#read out phrases from messages
	#phrases strings are FIXED in messages dictionary
	def voiceOut(self, messagetype):
		voiceCmd = self.syntax_head + self.volume + self.variation['female1'] + " '" + self.messages.get(messagetype) + self.syntax_tail 
		os.system(voiceCmd)
		return

	#output message given
	def say(self, message):
		voiceCmd = self.syntax_head + self.volume + self.variation['female1'] + " '" + message + self.syntax_tail 
		os.system(voiceCmd)
		return

class Messages():
	def __init__(self):
		self.step_count = str(5)
		self.startloc = ['0', '0', '0', '0']
		self.dest = ['0', '0', '0', '0']
		self.yninput = 0
		#dictionary of phrases chips
		self.phrases = {1: 'Welcome', 2: 'Please key in your', 
				   3: 'you have keyed in', 4: 'as your', 5: 'shall I proceed?', 
				   6: 'please take a step', 7: 'please take another step', 
				   8: 'thank you', 9: 'calculating path', 10: 'process complete', 
				   11: 'please turn', 12: 'please go straight', 
				   13: 'you have reached the edge of a staircase. please be careful and',
				   14: 'please open the door to your', 15: 'you have arrived at your destination',
				   16: 'object detected', 17: 'please proceed with caution',
				   18: 'path is blocked. would you like to stay on the same path?',
				   19: 'path is clear', 20: 'goodbye', 21: 'calibrating your stride',
				   22: 'please wait', 23: 'you have reached the end of the staircase',
				   24: 'please try again.',
				   # phrases chips
				   31: 'starting location', 32: 'destination',
				   41: 'please press', 42: '1 for yes', 43: '2 for no',
				   51: 'left', 52: 'right', 53: 'front', 54: 'start ascending', 55: 'start desecnding',
				   56: 'stop',
				   # inputs needed
				   61: 'in' , 62: self.step_count, 63: 'steps',
				   64: '|'.join(self.startloc), 65: '|'.join(self.dest), 66: self.yninput}
		
		#dictionary of actual phrases strings to be printed
		self.messages = {
					# startup processes: start location, destination, calibration and path calculations
					'startup':			self.phrases[1]  + ". " + self.phrases[2]  + " "  + self.phrases[31] + ".",
					'get_dest':			self.phrases[2]  + " "  + self.phrases[32] + ".",
					'confirm_startloc':	self.phrases[3]  + " "  + self.phrases[64] + " "  + self.phrases[4]  + " " + self.phrases[31] + ". " + self.phrases[5],
					'confirm_dest':		self.phrases[3]  + " "  + self.phrases[65] + " "  + self.phrases[4]  + " " + self.phrases[32] + ". " + self.phrases[5],
					'yn_inst':			self.phrases[41] + " "  + self.phrases[42] + ". " + self.phrases[41] + " " + self.phrases[43] + ".",
					'confirm_yes':		self.phrases[3]  + " "  + self.phrases[42] + ".",
					'confirm_no':		self.phrases[3]  + " "  + self.phrases[43] + ".",
					'cali_header':		self.phrases[21] + ".",
					'cali_inst1':		self.phrases[6]  + ".",
					'cali_inst2':		self.phrases[7]  + ".",
					'path_calc':		self.phrases[9]  + ". " + self.phrases[22],
					# directional self.messages
					'left':				self.phrases[11] + " " + self.phrases[51] + ".",
					'right':			self.phrases[11] + " " + self.phrases[52] + ".",
					'left_st':			self.phrases[11] + " " + self.phrases[51] + " " + self.phrases[61] + " " +	self.phrases[62] + " " + self.phrases[63] + ".",
					'right_st':			self.phrases[11] + " " + self.phrases[52] + " " + self.phrases[61] + " " + self.phrases[62] + " " + self.phrases[63] + ".",
					'straight':			self.phrases[12] + ".", 
					'stairs_a':			self.phrases[13] + " " + self.phrases[54] + ".",
					'stairs_d':			self.phrases[13] + " " + self.phrases[55] + ".",
					'stairs_end':		self.phrases[23] + ".",
					'door_left':		self.phrases[14] + " " + self.phrases[51] + ".",
					'door_right':		self.phrases[14] + " " + self.phrases[52] + ".",
					'door_front':		self.phrases[14] + " " + self.phrases[53] + ".", 
					'dest_arrived':		self.phrases[15] + ".",
					# object detection
					'obj_det':			self.phrases[16] + ".",
					'obj_det_st':		self.phrases[16] + " " + self.phrases[61] + " " + self.phrases[62] + " " + self.phrases[63] + ".",
					'caution':			self.phrases[17] + ".",
					'path_blocked':		self.phrases[18],
					'path_clear':		self.phrases[19],
					# miscellaneous self.messages
					'error':		    self.phrases[24],
					'wait_inst':		self.phrases[22] + ".",
					'process_done':		self.phrases[10] + ".",
					'thankyou':			self.phrases[8]  + ".",
					'goodbye':			self.phrases[20] + "." }
	
	def setStartLoc(self, new_value):
		self.startloc = new_value
		
	def setDest(self, new_value):
		self.dest = new_value
		
	#updates dictionary values based on field given
	#fields available: 
	# ** user's start location (self.startloc)
	# ** user's destination (self.dest)
	# new_value is a list passed in from caller
	def updateDictionaryValues(self, new_value, update_field):
		if (update_field == 'startloc'):
			self.setStartLoc(new_value)
			del self.phrases[64]
			del self.messages['confirm_startloc']
			self.phrases[64] = '|'.join(self.startloc)
			self.messages['confirm_startloc'] = (self.phrases[3] + " " + self.phrases[64] + " " + self.phrases[4] + 
												" " + self.phrases[31] + ". " + self.phrases[5])
		
		elif (update_field == 'dest'):
			self.setDest(new_value)
			del self.phrases[65]
			del self.messages['confirm_dest']
			self.phrases[65] = '|'.join(self.dest)
			self.messages['confirm_dest'] = (self.phrases[3] + " " + self.phrases[65] + " " + self.phrases[4] + 
											" " + self.phrases[32] + ". " + self.phrases[5])
		
		else:
			print ('****ERROR IN UPDATING VALUES****')
			return 0
		return 1
	
	def getPhrases(self):
		return self.phrases
	
	def getMessages(self):
		return self.messages




#############################################

#          Stuff not in classes

#############################################


#handshaking protocol between Arduino and RPi
def getAck():
	# to be done by Alvin/Jiayi
	return 1



try:
	if getAck():
		while 1:
			# on startup
			print message_str['startup']
			voiceOut('startup')
	
			# get starting location and update values in dictionary
			response = getLocationInput()
			if (updateDictionaryValues(response, 'startloc')):
				print message_str['confirm_startloc']
				voiceOut('confirm_startloc')
				yn_response = getYNInput()
	
				if (YNHandler(yn_response)):
					break
		while 1:
			print message_str['get_dest']
			voiceOut('get_dest')
			response = getLocationInput()
	
			if (updateDictionaryValues(response, 'dest')):
				print message_str['confirm_dest']
				voiceOut('confirm_dest')
				yn_response = getYNInput()
	
				if (YNHandler(yn_response)):
					print message_str['cali_header']
					voiceOut('cali_header')
					break
	
		####### NOT COMPLETED. TO DO: GET DATA FROM SENSORS AND SEND BACK #########
		print message_str['cali_inst1']
		voiceOut('cali_inst1')
		time.sleep(2)  # time delay to simulate sensor calibration
		print message_str['cali_inst2']
		voiceOut('cali_inst2')
		time.sleep(2)
	
		print message_str['path_calc']
		voiceOut('path_calc')
		print message_str['wait_inst']
		voiceOut('wait_inst')
		time.sleep(2)  # time delay to simulate path calculation
		###########################################################################
	
		print message_str['process_done']
		voiceOut('process_done')
	
		####### USE LIST TO GIVE INSTRUCTIONS   #######
		# # 0 - turn left							 ##
		# # 1 - go straight						   ##
		# # 2 - turn right							##
		# # 3 - destination arrived				   ##
		# # 4 - open door on left					 ##
		# # 5 - open door in front					##
		# # 6 - open door on right					##
		# # 7 - climb up stairs					   ##
		# # 8 - climb down stairs					 ##
		# # 9 - end of stairs						 ##
		# # everytime the user changes level,		 ##
		# # generate a new directions list.		   ##
		###############################################
		# # INCOMPLETE: incorporate number of steps before turning left ##
		directions_list = [0, 1, 2, 3, 4, 5, 6]
		for x in directions_list:
			if x == 0:
					print message_str['left']
					voiceOut('left')
			elif x == 1:
					print message_str['straight']
					voiceOut('straight')
			elif x == 2:
					print message_str['right']
					voiceOut('right')
			elif x == 3:
					print message_str['dest_arrived']
					voiceOut('dest_arrived')
			elif x == 4:
					print message_str['door_left']
					voiceOut('door_left')
			elif x == 5:
					print message_str['door_front']
					voiceOut('door_front')
			elif x == 6:
					print message_str['door_right']
					voiceOut('door_right')
			elif x == 7:
					print message_str['stairs_a']
					voiceOut('stairs_a')
			elif x == 8:
					print message_str['stairs_d']
					voiceOut('stairs_d')
			elif x == 9:
					print message_str['stairs_end']
					voiceOut('stairs_end')
		##########################################################################
	
	
		############################## OBJECT DETECTION ##########################
		# phrases strings have been prepared but waiting on alvin & jiayi for data structure
	
	else:
		print ('ACK FAILED')
except KeyboardInterrupt:
	ser.close()
	print message_str['error']
	voiceOut('error')
	print ('program stop')
