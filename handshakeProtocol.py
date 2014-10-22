import serial
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
ser.open()

try:
	ser.write("ACK")
	response_RDY = ser.readline()
	print response_RDY
	while not 'RDY' in response_RDY:
		response_RDY = ser.readline()
		print response_RDY
	ser.write("RDY")
	response_ACKACK = ser.readline()
	print response_ACKACK
	while not 'ACKACK' in response_ACKACK:
		ser.write("ACKRDY")
		response_ACKACK = ser.readline()
		print response_ACKACK
	print ("Handshaking protocol complete. Communication line has been established.")

except KeyboardInterrupt:
	ser.close()
