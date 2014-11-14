'''
Created on 12 Nov, 2014

@author: AdminNUS
'''
from threadTest import VoiceHandler
from anotherClass import TestClass
import threading

test = TestClass()
voice = VoiceHandler()
voiceThread = threading.Thread(target = voice.voiceLoop)
# testThread = threading.Thread(target= test.startTest)
voiceThread.start()
test.startTest(voice)