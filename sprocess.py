'''
Created on 5 Nov, 2014

@author: AdminNUS
'''

import subprocessVariables
import messages
import subprocess

variation = {'female1': ' -ven+f3', 
			 'female2': ' -ven+f4',
			 'male1': ' -ven+m2', 
			 'male2': ' -ven+m3'}

lastProcess = None

while True:
	if (not subprocessVariables.voiceQueue.empty()) and (lastProcess.poll() is None):
		nextMessage = subprocessVariables.voiceQueue.get()
		voiceCmd = messages.VOICE_CMD_TEMPLATE.format(volume = 100, 
												  	  voice = variation.get('female1'),
												  	  msg = nextMessage)
		lastProcess = subprocess.Popen(voiceCmd,
									   shell=True,
									   stdout = subprocess.PIPE, 
									   preexec_fn = os.setsid)
	else:
			
	
		