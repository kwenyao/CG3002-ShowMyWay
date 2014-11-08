'''
Created on 5 Nov, 2014

@author: AdminNUS
'''
import subprocessVariables
import messages
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

while True:
	if subprocessVariables.currPriority < subprocessVariables.priority:
		killProcess(lastProcess)
		message = subprocessVariables.get()
		sayMsg(message)
	elif isProcessDone(lastProcess):
		message = subprocessVariables.get()
		sayMsg(message)
	
	
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
		
			

		