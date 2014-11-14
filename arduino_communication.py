import serial
import RPi.GPIO as GPIO ## Import GPIO library
import time

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
				print "from Serial" ,
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
				print "from Serial" ,
				print message
				if message[0] == 'G':
					handshake = 1
	
		if isTimeOut != 0 :
			return str(isTimeOut)
		else:
			return "Done"
		
	def resetArduino(self):
		GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
		GPIO.setup(22, GPIO.OUT) ## Setup GPIO Pin 22 to OUT
		GPIO.output(22,False)
		time.sleep(1)
		GPIO.output(22,True) ## Turn on GPIO pin 22
		
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
