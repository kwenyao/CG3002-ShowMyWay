import subprocess
import re
import math

class AccessPoints():
	def __init__(self):
		self.scannedAPDict = {}
		self.FREE_SPACE_CONSTANT = 27.55
			
	def calculateDistanceFromAP(self, signal, freq):
		freq = float(freq)*1000
		result = (self.FREE_SPACE_CONSTANT - 20*math.log10(float(freq)) - float(signal))/20
		distance = math.pow(10,result)
		return distance 
	
	def determineUsableAp(self, apList, wifiNodes):
		selection = []
		selected_address = {}
		for j in range(0, len(apList)):
			if len(selection) >= 3:
				break
			macAddr = apList[j].get('address')
			node = wifiNodes.get(macAddr)
			if node != None:
				found = {}
				found['ap'] = apList[j]
				found['node'] = node
				if selected_address.get(macAddr) is None:
					selected_address[macAddr] = ""
					selection.append(found)
	
		return selection # [{ 'ap': AP, 'node': NODE }, {}...]
	
	def scanWifiData(self):
		proc = subprocess.Popen('sudo iwlist scan 2>/dev/null', shell=True, stdout=subprocess.PIPE, )
		stdout_str = proc.communicate()[0]
		stdout_list = stdout_str.split('\n')
		return stdout_list
	
	def getAccessPoints(self):
		ap = {}
		ap_list = []
		frequency = 0
		self.scannedAPDict.clear()
		wifiScanList = self.scanWifiData()
		elementCount = 0
		# print wifiScanList
		for item in wifiScanList:
			item = item.strip()
			print item
			macAddr = self.extractMACAddr(item)
			if macAddr is not None:
				ap['address'] = macAddr
				elementCount += 1
				
			isFrequency = self.extractFrequency(item)
			if isFrequency is not None:
				frequency = isFrequency
				ap['freq'] = frequency
				elementCount += 1
			
			signal = self.extractSignal(item)
			if signal is not None:
				print signal
				ap['signal'] = signal
				ap['distance'] = self.calculateDistanceFromAP(signal,frequency)
				elementCount += 1
				
			if elementCount == 3:
				elementCount = 0
				ap_list.append(ap)
				ap = {}
		ap_list = self.sortAccessPoints(ap_list)
		print ap_list
		return ap_list
	
	def extractMACAddr(self, item):
		isMatch = re.search('Address: (\S+)', item)
		if isMatch:
			macAddr = isMatch.group(1)[0:14]
			isAlreadyFound = self.scannedAPDict.get(macAddr)
			if isAlreadyFound is None:
				self.scannedAPDict[macAddr] = macAddr
				return macAddr
			else:
				return None
		else:
			return None
	
	def extractFrequency(self, item):
		isMatch = re.search('Frequency:(\S+)', item)
		if isMatch:
			return isMatch.group(1)
		else:
			return None
			
	def extractSignal(self, item):
		found = re.search('Signal level=(\S+)',item)
		if found:
			return int(found.group(1))
		else:
			return None

	def sortAccessPoints(self, ap_list):
		# Sort by signal strength
		return sorted(ap_list, key = self.getKey )
	
	def getKey(self, item):
		signal = item.get('signal')
		if signal is None:
			return None
		else:
			return math.fabs(float(item.get('signal')))
	