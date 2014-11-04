from navigation.navigation import Navigation
from ServerSync import MapSync
from UserInteraction import Voice
import initialise
import messages

def main():	
	currmap = MapSync()
	voiceOutput = Voice()
	initialise.arduinoHandshake()
	initialise.calibrateStep()
	
	while True:
		# userInput = initialise.getInitialInput()
		userInput = {'building': '1', 'level': '2', 'start': '1', 'end': '2'}
		isLoadSuccess = currmap.loadLocation(userInput.get('building'), userInput.get('level'))
		if(isLoadSuccess):
			break
		else:
			voiceOutput.say(messages.MAP_DOWNLOAD_FAILED)
	apNodes = currmap.apNodes
	
	# map north stored as anti clockwise
	# previous calculation is based on rotating anti clockwise, 
	# current input is based on clockwise, hence need to offset
	map_north = abs(currmap.north-360)
	mapNodes = currmap.mapNodes
	navigate = Navigation(mapNodes, map_north)
	navigate.getRoute(userInput.get('start'), userInput.get('end'))
	navigate.beginNavigation(apNodes)

		
if __name__ == "__main__":
	main()
