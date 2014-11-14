#!/usr/bin/env python

import subprocessVariables
import subprocess

'''

low priority: 
- ask for user input
- walk straight

medium priority:
- turning

high priority:
- obstacles detected

'''

#########################
# MAIN CODE
#########################

lastProcess = None
print "test"
while True:
	
	if not subprocessVariables.voiceQueue.empty() and lastProcess is None:
		message = subprocessVariables.get()
		lastProcess = subprocessVariables.sayMsg(message)
	elif subprocessVariables.currPriority < subprocessVariables.priority:
		killProcess(lastProcess)
		message = subprocessVariables.get()
		lastProcess = subprocessVariables.sayMsg(message)
	elif not lastProcess is None and subprocessVariables.isProcessDone(lastProcess):
		message = subprocessVariables.get()
		lastProcess = subprocessVariables.sayMsg(message)
	
	
# 	if isHighPriority:
# 		
# 		if not subprocessVariables.isCurrMessageHigh: #if current message is low priority
# 			message = subprocessVariables.voiceQueue.get()
# 			# Kill
# 			
# 			# say message
# 			
# 			subprocessVariables.isCurrMessageHigh = True
# 			if subprocessVariables.voiceQueue.empty():
# 				isHighPriority = False
# 			
# 	
# 	#there is a message in the queue and voice is not finished
# 	if (not subprocessVariables.voiceQueue.empty()) and (lastProcess.poll() is None):
# 		nextMessage = subprocessVariables.voiceQueue.get()
# 		
# 		lastProcess = subprocess.Popen(voiceCmd,
# 									   shell=True,
# 									   stdout = subprocess.PIPE, 
# 									   preexec_fn = os.setsid)
		
			

		