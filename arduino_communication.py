import serial

class Arduino():		
	def handshakeWithArduino(self):
		serial = SerialCommunicator()
		handshake = 0
		isTimeOut = 0
		print "enter handshake"
		#handshake with GY87
		while(handshake == 0 and isTimeOut == 0):
			message = serial.serialRead()
			print "after serial read 1"
			if (len(message) == 0 ):
			#	isTimeOut = 1
				print "nth receive at 1"
			else:
				print message
				if message[0] == 'S':
					handshake = 1
					serial.serialWrite('1')
		handshake = 0
		while (handshake == 0 and isTimeOut == 0):
			message = serial.serialRead()
			if (len(message) == 0 ):
			#	isTimeOut = 1
				print "nth receive at 2"
			else:
				print message
				if message[0] == 'G':
					handshake = 1
	
		if isTimeOut != 0 :
			return str(isTimeOut)
		else:
			return "Done"
		
class SerialCommunicator():
	def __init__(self):
		#initialise serial port with Arduino
		self.ser = serial.Serial('/dev/ttyAMA0', 9600)
		self.ser.open()

	def serialWrite(self, message_str):
		self.ser.write(message_str)
		return

	def serialRead(self):
		message = self.ser.readline()
		return message
