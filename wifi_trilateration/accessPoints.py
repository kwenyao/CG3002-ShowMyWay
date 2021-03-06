import subprocess
import re
import math

class AccessPoints():
	def __init__(self):
		self.scannedAPDict = {}
		self.FREE_SPACE_CONSTANT = 27.55
			
	def calculateDistanceFromAP(self, signal, freq):
		freq = float(freq)*1000
		result = (float(self.FREE_SPACE_CONSTANT) - 20*math.log10(float(freq)) - float(signal))/20
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
		proc = subprocess.Popen('sudo iwlist scan 2>/dev/null', shell=True, stdout = subprocess.PIPE, )
		stdout_str = proc.communicate()[0]
		stdout_list = stdout_str.split('\n')
		return stdout_list
	
	def getAccessPoints(self):
		ap = {}
		ap_list = []
		freq1 = 0
		self.scannedAPDict.clear()
		wifiScanList = self.scanWifiData()
		elementCount = 0
		# print wifiScanList
		for item in wifiScanList:
			item = item.strip()
			match = re.search('Address: (\S+)', item)
			if match:
				macAddr = match.group(1)[0:14]
				isAlreadyFound = self.scannedAPDict.get(macAddr)
				if isAlreadyFound is None:
					ap['address'] = macAddr
					self.scannedAPDict[macAddr] = macAddr
					elementCount += 1 
				else:
					continue
			match = re.search('Frequency:(\S+)', item)
			if match:
				freq1 = match.group(1)
				ap['freq'] = freq1
				elementCount += 1
			found = re.search('Signal level=(\S+)',item)
			if found:
				match = found.group(1)
				sig = int(match)
				ap['signal'] = sig
				ap['distance'] = self.calculateDistanceFromAP(sig,freq1)
				elementCount += 1
			if elementCount == 3:
				elementCount = 0
				ap_list.append(ap)
				ap = {}
		ap_list = self.sortAccessPoints(ap_list)
		return ap_list
	
	def sortAccessPoints(self, ap_list):
		# Sort by signal strength
		return sorted(ap_list, key = self.getKey )
	
	def getKey(self, item):
		return math.fabs(float(item['signal']))