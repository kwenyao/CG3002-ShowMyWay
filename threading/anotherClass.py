'''
Created on 14 Nov, 2014

@author: AdminNUS
'''
import time


class TestClass():
	def startTest(self, voice):
		while True:
			voice.voiceLock.acquire()
			message = "low priority"
			print message		
			voice.addToQueue(message, 0)
			voice.voiceLock.release()
			time.sleep(1)
