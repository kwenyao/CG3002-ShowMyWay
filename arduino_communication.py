import serial

class Arduino():
	def __init__(self, serialPort):
		### CLASS ATTRIBUTES ###
		self.serialPort = serialPort
		
	def handshakeWithArduino(self):
		handshake = 0
		isTimeOut = 0
		print "enter handshake"
		#handshake with GY87
		while(handshake == 0 and isTimeOut == 0):
			message = self.serialPort.readline()
			print "after serial read 1"
			if (len(message) == 0 ):
			#	isTimeOut = 1
				print "nth receive at 1"
			else:
				print message
				if message[0] == 'S':
					handshake = 1
					self.serialPort.write("1")	
		handshake = 0
		while (handshake == 0 and isTimeOut == 0) :
			message = self.serialPort.readline()
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