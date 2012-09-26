from defaults import storeNetStates
from numpy import std, mean, median

class NetStatistics(object):
	def __init__(self, **kwargs):
		self.state = 'initialization' # also 'training', 'detection'
		self.net_states = []
		self.prevtime, self.prevload, self.prevpps = (None, None, None)
		self.netstate = None
		self.stdevthreshold = None
		self.medianthreshold = None
		self.madethreshold = None
		self.alarm = ""
		self.alarmprobability = 0
		self.attacktype = ""
		self.states_to_store = storeNetStates
		self.methods = (kwargs['methods'] if 'methods' in kwargs else ('stdev',))
		self.methodprobability = 100./len(self.methods)
		
	def addSample(self,pollresult):
		avgtime, totload, totpps = self.calc_totload(pollresult)
		if self.state == 'initialization':
			self.netstate = 'start'
			self.state = 'training'
		elif self.state == 'training':
			self.netstate = self.calc_bandwidth(avgtime, totload, totpps)
			self.net_states.append(self.netstate)
			if len(self.net_states)==self.states_to_store:
				self.state = 'detection'
		elif self.state == 'detection':
			self.netstate = self.calc_bandwidth(avgtime, totload, totpps)
			self.detectOutlier()
			if not self.alarm:
				del self.net_states[0]
				self.net_states.append(self.netstate)
			else:
				self.attacktype = self.attack_type() if self.netstate[1]!=0 else ""
		self.prevtime, self.prevload, self.prevpps = (avgtime, totload, totpps)
	
	def getNetState(self):
		return (self.netstate[0], self.stdevthreshold, self.alarm)

	def getAdvParams(self):
		return (self.netstate[1], self.medianthreshold, self.madethreshold)

	def getAlarmParams(self):
		return (self.alarmprobability, self.attacktype)

	def calc_totload(self,pollresult):
		avgtime, totload, totpps = (.0,0,0)
                for polltime, load, packetload in pollresult:
                        avgtime+=polltime
                        totload+=int(load)
			totpps+=int(packetload)
                avgtime/=len(pollresult)
		return (avgtime, totload, totpps)

	def calc_bandwidth(self, avgtime, totload, totpps):
                bandwidth = (totload-self.prevload)*1./(avgtime-self.prevtime)
		packetsize = None if totpps==0 else (totload-self.prevload)*1./(totpps-self.prevpps)
		return (int(bandwidth), int(packetsize))

	def detectOutlier(self):
		self.alarmprobability = 0.
		if ('stdev' in self.methods):
			self.alarmprobability += self.stdev_method()
		if ('median' in self.methods):
			self.alarmprobability += self.median_rule()
		if ('made' in self.methods):
			self.alarmprobability += self.made_method()
		self.alarmprobability *= self.methodprobability
		self.alarmprobability = int(self.alarmprobability)
		self.alarm = ("ALARM" if self.alarmprobability > 50 else "")
		
	def stdev_method(self):
		values = [i[0] for i in self.net_states]
		stdev = std(values)
		self.stdevthreshold = mean(values) + 3*stdev
		return (1 if self.netstate[0] >= self.stdevthreshold else 0)

	def median_rule(self):
		values = sorted([i[0] for i in self.net_states])
		nval1 = len(values)+1
		median_value = values[nval1/2-1]
		iqr = values[nval1*3/4-1]-values[nval1/4-1]
		self.medianthreshold = median_value + int(2.3*iqr)
		return (1 if self.netstate[0] >= self.medianthreshold else 0)

	def made_method(self):
		values = [i[0] for i in self.net_states]
		median_value = median(values)
		made = 1.483 * median([abs(v-median_value) for v in values])
		self.madethreshold = median_value + 3*made
		return (1 if self.netstate[0] >= self.madethreshold else 0)

	def attack_type(self):
		values = [i[1] for i in self.net_states]
		threshold = mean(values)-3*std(values)
		threshold = threshold if threshold>=0 else 0
		return ("DoS attack" if self.netstate[1] <= threshold else "Flash crowd")+" (packet size threshold %d)" % threshold
