from navigation.navigation import Navigation
from ServerSync import MapSync
from UserInteraction import Voice
import initialise
import messages
import threading
from navigation.guide import Guide
from voiceThread import VoiceHandler
import constants

def main():	
	mapUsed = [] 				#store the mapsync obj of the maps to be used later.
	interMapNodes = []
	COM12 = MapSync()
	COM12.loadLocation('1', '2')
	COM22 = MapSync()
	COM22.loadLocation('2', '2')
	COM23 = MapSync()
	COM23.loadLocation('2', '3')
	allMaps = {'12' : COM12, '22' : COM22 , '23': COM23}
	
# 	voiceOutput = Voice()

	### VOICE THREAD ###
	voiceOutput = VoiceHandler()
	voiceThread = threading.Thread(target = voiceOutput)
	voiceThread.start()
	
	guiding = Guide(voiceOutput)
	initialise.arduinoHandshake(voiceOutput) #add in the code whereby if handshake fails, try another few more times
	initialise.calibrateStep(voiceOutput)
	userInput = initialise.getInitialInput(voiceOutput)
# 	userInput = {'buildingstart': '1', 'levelstart': '2', 'start': '26', 'buildingend': '2', 'levelend': '2',  'end': '2'}
	startKey = userInput.get('buildingstart') + userInput.get('levelstart')
	endKey = userInput.get('buildingend') + userInput.get('levelend')
	mapUsed.append(allMaps.get(startKey))
	interMapNodes.append(userInput.get('start'))
	
	if userInput.get('buildingstart') != userInput.get('buildingend'):
		if userInput.get('levelstart') != userInput.get('levelend'): #diff floor diff build
			for k, v in (mapUsed[0].mapConnection).iteritems():
				if v.get('building') == '2' and v.get('level') == '2' :
					interMapNodes.append(k)
					interMapNodes.append(v.get('node'))
			mapUsed.append(allMaps.get('22'))
			for k, v in (mapUsed[1].mapConnection).iteritems():
				if v.get('building') == userInput.get('buildingend') and v.get('level') == userInput.get('levelend') :
					interMapNodes.append(k)
					interMapNodes.append(v.get('node'))
			mapUsed.append(allMaps.get(endKey))
			
		else:
			print "inside" #diff floor same level
			for k, v in (mapUsed[0].mapConnection).iteritems():
				if v.get('building') == userInput.get('buildingend') and v.get('level') == userInput.get('levelend') :
					interMapNodes.append(k)
					interMapNodes.append(v.get('node'))
			mapUsed.append(allMaps.get(endKey))		
	else:
		if userInput.get('levelstart') != userInput.get('levelend'):#same level diff build
			for k, v in (mapUsed[0].mapConnection).iteritems():
				if v.get('building') == userInput.get('buildingend') and v.get('level') == userInput.get('levelend') :
					interMapNodes.append(k)
					interMapNodes.append(v.get('node'))
		mapUsed.append(allMaps.get(endKey))
	interMapNodes.append(userInput.get('end'))
	
	print "current interMap coor is " ,
	print interMapNodes
	print "mapUsed is "
	for i in range(len(mapUsed)):
		currmap = mapUsed[i]
		apNodes = currmap.apNodes
		# map north stored as anti clockwise
		# previous calculation is based on rotating anti clockwise, 
		# current input is based on clockwise, hence need to offset
		map_north = (abs(currmap.north-360)-5)%360
		mapNodes = currmap.mapNodes
		navigate = Navigation(mapNodes, map_north, voiceOutput)
		navigate.getRoute(interMapNodes[i*2], interMapNodes[i*2+1])
		navigate.beginNavigation(apNodes)
		if i != len(mapUsed)-1:
# 			voiceOutput.say('You have reach the end of a map, switching to a new map.',2)
			voiceOutput.addToQueue('You have reach the end of a map, switching to a new map.', constants.HIGH_PRIORITY)
	guiding.destinationReached()
		
if __name__ == "__main__":
	main()
