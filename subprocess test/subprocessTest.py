'''
Created on 5 Nov, 2014

@author: AdminNUS
'''

import subprocess
import os
import subprocessVariables

lastProcess = subprocess.Popen('sudo python sprocess.py', 
 							   shell=True, 
							   stdout=subprocess.PIPE, 
							   preexec_fn = os.setsid)

while True:
	print 'loop loop'
	print 'queueing low priority'
	subprocessVariables.addToQueue("low priority message",0)
	subprocessVariables.addToQueue("medium priority message",1)
	subprocessVariables.addToQueue("high priority message",2)
	print 'pool pool'
