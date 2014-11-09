'''
Created on 5 Nov, 2014

@author: AdminNUS
'''
from Queue import Queue
import time

variation = {'female1': ' -ven+f3', 
			 'female2': ' -ven+f4',
			 'male1': ' -ven+m2', 
			 'male2': ' -ven+m3'}

voiceQueue = Queue()
prevMessage = ""
priority = 0 # low priority = 0, medium priority = 1, high priority = 2
currPriority = 0


def addToQueue(message, msgPriority):
	if voiceQueue.empty():
		voiceQueue.put(message)
		priority = msgPriority
	elif (msgPriority == priority) and not (message == prevMessage):
		voiceQueue.put(message)
	elif (msgPriority > priority) and not (message == prevMessage):
		voiceQueue.queue.clear()
		voiceQueue.put(message)
		priority = msgPriority
		 
def sayMsg(message):
	print "Voice Output: " + message
	voiceCmd = messages.VOICE_CMD_TEMPLATE.format(volume = 100, 
												  voice = variation.get('female1'),
												  msg = nextMessage)
	currPriority = priority

def killProcess(process):
	os.killpg(process.pid, signal.SIGTERM)
	
def isProcessDone(process):
	response = process.poll()
	if response is None:
		return False
	else: 
		return True
	
# 	if isHigh and not isHighPriority:
# 		voiceQueue.queue.clear()
# 		voiceQueue.put(message)
# 		return
# 	
# 	if message == prevMessage:
# 		return
# 	else:
# 		voiceQueue.put(message)