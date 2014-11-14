'''
Created on 5 Nov, 2014

@author: AdminNUS
'''

import subprocess
import os
import subprocessVariables

full_path = os.path.abspath('sprocess.py')

subprocess.Popen(["python", full_path])

# child = subprocess.Popen("./test.py", stdin=subprocess.PIPE)  

# lastProcess = subprocess.Popen('./sprocess.py', 
#  							   shell=True, 
# 							   stdout=subprocess.PIPE, 
# 							   preexec_fn = os.setsid)


# subprocess.call(['python', full_path])

while True:
	print 'loop loop'
	print 'queueing low priority'
	subprocessVariables.addToQueue("low priority message", 0)
# 	print 'queueing med priority'
# 	subprocessVariables.addToQueue("medium priority message",1)
# 	subprocessVariables.addToQueue("high priority message",2)
	print 'pool pool'
