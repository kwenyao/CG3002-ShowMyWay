'''
Created on 5 Nov, 2014

@author: AdminNUS
'''

import subprocess
import os

lastProcess = subprocess.Popen('sudo python sprocess.py', 
 							   shell=True, 
							   stdout=subprocess.PIPE, 
							   preexec_fn = os.setsid)

while True:
	print 'loop loop'
	
	
	
	print 'pool pool'
