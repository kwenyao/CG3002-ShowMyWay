import os
import RPi.GPIO as GPIO
import serial
import subprocess
import messages

class Keypad():
	# CONSTANTS   
	KEYPAD = [['1','2','3'],
			  ['4','5','6'],
		   	  ['7','8','9'],
			  ['*','0','#']]
	
	ROW = [7,8,25,24]
	COLUMN = [11,9,10]
	
	def __init__(self):
		GPIO.setmode(GPIO.BCM)
	
	def getKey(self):
		# Set all columns as output low
		for j in range(len(self.COLUMN)):
			GPIO.setup(self.COLUMN[j], GPIO.OUT)
			GPIO.output(self.COLUMN[j], GPIO.LOW)
		
		# Set all rows as input
		for i in range(len(self.ROW)):
			GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
		
		# Scan rows for pushed key/button
		# A valid key press should set "rowVal"  between 0 and 3.
		rowVal = -1
		for i in range(len(self.ROW)):
			tmpRead = GPIO.input(self.ROW[i])
			if tmpRead == 0:
				rowVal = i
				
		# if rowVal is not 0 thru 3 then no button was pressed and we can exit
		if rowVal <0 or rowVal >3:
			self.exit()
			return
		
		# Convert columns to input
		for j in range(len(self.COLUMN)):
				GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		
		# Switch the i-th row found from scan to output
		GPIO.setup(self.ROW[rowVal], GPIO.OUT)
		GPIO.output(self.ROW[rowVal], GPIO.HIGH)

		# Scan columns for still-pushed key/button
		# A valid key press should set "colVal"  between 0 and 2.
		colVal = -1
		for j in range(len(self.COLUMN)):
			tmpRead = GPIO.input(self.COLUMN[j])
			if tmpRead == 1:
				colVal=j
				
		# if colVal is not 0 thru 2 then no button was pressed and we can exit
		if colVal <0 or colVal >2:
			self.exit()
			return

		# Return the value of the key pressed
		self.exit()
		return self.KEYPAD[rowVal][colVal]
	
	def exit(self):
		# Reinitialize all rows and columns as input at exit
		for i in range(len(self.ROW)):
			GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP) 
		for j in range(len(self.COLUMN)):
			GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)

	def getKeysInput(self):
		inputBuffer = ""
		current_state = next_state = 0
		while(1):
			current_state = next_state	
			digit = self.getKey()
			if current_state == 0:
				if(digit == None):
					next_state = 0
				else:
					next_state = 1
					if '#' in digit:
						return inputBuffer
					inputBuffer += digit

			else:
				if(digit == None):
					next_state = 0
				else:
					next_state = 1
	
class Voice():
	def __init__(self):
		self.messagesObj = Messages()
		self.phrases = self.messagesObj.getPhrases()
		self.messages = self.messagesObj.getMessages()
		self.setupVoice()
		
		### CLASS ATTRIBUTES ###
		self.lastProcess = None
		self.lastImportance = 0 # 0 least important 2 most important
		
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
		
	#output message given
	def say(self, message, importanceLevel = 0):
		print message
		if(importanceLevel > self.lastImportance):
			os.killpg(self.lastProcess.pid, signal.SIGTERM)
		else:
			response = self.lastProcess.poll()
			if response is None: # Voice output not finished
				return
		voiceCmd = messages.VOICE_CMD_TEMPLATE.format(volume = 100, 
													  voice = self.variation.get('female1'), 
													  msg = message)
# 		voiceCmd = self.syntax_head + self.volume + self.variation['female1'] + " '" + str(message) + self.syntax_tail
		self.lastProcess = subprocess.Popen(voiceCmd, 
											shell=True, 
											stdout=subprocess.PIPE, 
											preexec_fn=os.setsid)
		self.lastImportance = importanceLevel
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
				   31: 'starting location', 32: 'destination', 33: 'building number', 34: 'building level',
				   41: 'please press', 42: '1 for yes', 43: '2 for no',
				   51: 'left', 52: 'right', 53: 'front', 54: 'start ascending', 55: 'start desecnding',
				   56: 'stop',
				   # inputs needed
				   61: 'in' , 62: self.step_count, 63: 'steps',
				   64: '|'.join(self.startloc), 65: '|'.join(self.dest), 66: self.yninput}
		
		#dictionary of actual phrases strings to be printed
		self.messages = {
					# startup processes: start location, destination, calibration and path calculations
					'startup1':			self.phrases[1]  + ". " + self.phrases[2]  + " "  + self.phrases[33] + ".", 	#get building number
					'startup2':			self.phrases[2]  + " "  + self.phrases[34] + ".",								#get building level
					'get_startloc':		self.phrases[2]  + " "  + self.phrases[31] + ".",								#get startloc
					'get_dest':			self.phrases[2]  + " "  + self.phrases[32] + ".",								#get dest
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
					'right_st':			self.phrases[11] + " " + self.phrases[52] + " " + self.phrases[61] + " " +  self.phrases[62] + " " + self.phrases[63] + ".",
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
