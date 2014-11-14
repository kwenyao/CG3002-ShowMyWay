import threading  # For Threads and Locks
import time  # For time.sleep()
import messages
import subprocess
import signal
import os
from Queue import Queue
import signal
class VoiceHandler:
	def __init__(self):
		self.voiceLock = threading.Lock()
		self.voiceQueue = Queue()
		self.lastProcess = None
		self.priority = 0 # low priority = 0, medium priority = 1, high priority = 2
		self.currPriority = 0
		self.prevMessage = ""
		self.variation = {'female1': ' -ven+f3',
						  'female2': ' -ven+f4',
			 			  'male1'  : ' -ven+m2',
			 			  'male2'  : ' -ven+m3'}
	
	####################################
	# Main voice loop	
	####################################
		
	def voiceLoop(self):
		while True:
			self.voiceLock.acquire()
			if self.voiceQueue.empty():
				pass
			elif self.lastProcess is None:
				message = self.voiceQueue.get()
				self.sayMsg(message)
			elif self.currPriority < self.priority:
				os.killpg(self.lastProcess.pid, signal.SIGTERM)
				message = self.voiceQueue.get()
				self.sayMsg(message)
			elif (not self.lastProcess is None) and self.isProcessDone():
				message = self.voiceQueue.get()
				self.sayMsg(message)
			self.voiceLock.release()
			time.sleep(1)
		
# 	def mainLoop(self):
# 		count = 0
# 		while True:
# 			self.voiceLock.acquire()
# 			print 'queueing low priority'
# 			self.addToQueue("low priority message 1", 0)
# 			self.addToQueue("low priority message 2", 0)
# # 			if count % 2 == 0:
# # 				print 'queueing high priority'
# # 				self.addToQueue("high priority message", 2)
# 			count += 1
# 			self.voiceLock.release()
# 			time.sleep(1)
		
	####################################
	# Helper Functions
	####################################
	def addToQueue(self, message, msgPriority):
		self.voiceLock.acquire()
		if self.voiceQueue.empty():
			print "queue empty"
			self.voiceQueue.put(message)
			self.priority = msgPriority
			self.prevMessage = message
		elif (msgPriority == self.priority) and not (message == self.prevMessage):
			self.voiceQueue.put(message)
			self.prevMessage = message
		elif (msgPriority > self.priority) and not (message == self.prevMessage):
			self.voiceQueue.queue.clear()
			self.voiceQueue.put(message)
			self.priority = msgPriority
			self.prevMessage = message
		self.voiceLock.release()
	
	def sayMsg(self, message):
		print "Voice Output: " + message
		print "myself is " + str(self.voiceQueue.qsize())
		voiceCmd = messages.VOICE_CMD_TEMPLATE.format(volume = 100, 
													  voice = self.variation.get('female1'),
													  msg = message)
		self.lastProcess = subprocess.Popen(voiceCmd,
											shell=True,
								   			stdout=subprocess.PIPE, 
								   			preexec_fn = os.setsid)
		self.currPriority = self.priority
		
	def isProcessDone(self):
		response = self.lastProcess.poll()
		if response is None:
			return False
		else: 
			return True

# if __name__ == "__main__":
# 	myVoiceHandler = VoiceHandler()
# 	voiceThread = threading.Thread(target=myVoiceHandler.voiceLoop)
# 	voiceThread.start() # Temperature loop function starts running w/ 30 second intervals
# 	myVoiceHandler.mainLoop()  # Web handler starts running in main thread
# 	# At this point both threads should be running indefinitely

