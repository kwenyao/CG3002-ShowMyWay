import subprocess
import re
import math

class AccessPoints():
	def calculateDistanceFromAP(self, signal, freq):
		FreeSpaceConstant = 27.55
		freq = float(freq)*1000
		result = (float(FreeSpaceConstant) - 20*math.log10(float(freq)) - float(signal))/20
		distance = math.pow(10,result)
		return distance 
	
	def determineUsableAp(self, ap_list, wifi_nodes):
		selection = []
		selected_address = {}
		for j in range(0, len(ap_list)):
			if len(selection) >= 3:
				break
			mac_addr = ap_list[j]['address']
			node = wifi_nodes[mac_addr]
			if node != None:
				found = {}
				found['ap'] = ap_list[j]
				found['node'] = node
				if selected_address.get(mac_addr) is None:
					selected_address[mac_addr] = ""
					selection.append(found)
	
		return selection # [{ 'ap': AP, 'node': NODE }, {}...]
	
	def scanWifiData(self):
		proc = subprocess.Popen('iwlist scan 2>/dev/null', shell=True, stdout=subprocess.PIPE, )
		stdout_str = proc.communicate()[0]
		stdout_list = stdout_str.split('\n')
		return stdout_list
	
	def getAccessPoints(self):
		ap_list = []
		count = 0
		ap = {}
		wifiScanList = self.scanWifiData()
		for item in wifiScanList:
			item = item.strip()
			match = re.search('Address: (\S+)', item)
			if match:
				ap['address'] = match.group(1)
				# address.append(match.group(1))
				count+=1
	
			match = re.search('ESSID:"(\S+)"', item)
			if match:
				ap['essid'] = match.group(1)
				# essid.append(match.group(1))
				count+=1
	
			match = re.search('Frequency:(\S+)', item)
			if match:
				ap['freq'] = match.group(1)
				freq1 = match.group(1)
				# frequency.append(match.group(1))
				count+=1
	
			found = re.search('Signal level=(\S+)',item)
			if found:
				match = found.group(1).split('/')[0]	
				sig = (int(match)/2) - 100
				ap['signal'] = sig
				# signal_str.append(str(sig) + " dBm")
				ap['distance'] = self.calculateDistanceFromAP(sig,freq1)
				count+=1
			if count == 4:
				ap_list.append(ap)
				count = 0
				ap = {}
			
			
		return ap_list
	
	def sortAccessPoints(self, ap_list):
		# Sort by signal strength
		return sorted(ap_list, key = self.getKey )
	
	def getKey(self, item):
		return math.fabs(float(item['signal']))