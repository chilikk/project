from defaults import storeNetStates

class NetStatistics(object):
	def __init__(self, **kwargs):
		self.state = 'initialization' # also 'training', 'detection'
		self.net_states = []
		self.prevtime, self.prevload = (None, None)
		self.netstate = None
		self.stdevthreshold = None
		self.medianthreshold = None
		self.madethreshold = None
		self.alarm = ""
		self.alarmprobability = 0
		self.attacktype = ""
		self.states_to_store = storeNetStates
		if 'methods' in kwargs:
			self.methods = kwargs['methods']
		else:
			self.methods = ('stdev',)
		self.methodprobability = 100./len(self.methods)
		
	def addSample(self,pollresult):
		avgtime, totload, totpps = self.calc_totload(pollresult)
		if self.state == 'initialization':
			self.netstate = 'start'
			self.state = 'training'
		elif self.state == 'training':
			self.netstate = self.calc_bandwidth(avgtime, totload)
			self.net_states.append(self.netstate)
			if len(self.net_states)==self.states_to_store:
				self.state = 'detection'
		elif self.state == 'detection':
			self.netstate = self.calc_bandwidth(avgtime, totload)
			self.detectOutlier()
			if not self.alarm:
				del self.net_states[0]
				self.net_states.append(self.netstate)
		self.prevtime, self.prevload, self.pps = (avgtime, totload, totpps)
	
	def getNetState(self):
		return (self.netstate, self.stdevthreshold, self.alarm)

	def getThresholds(self):
		return (self.medianthreshold, self.madethreshold)

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

	def calc_bandwidth(self, avgtime, totload):
                return int((totload-self.prevload)/(avgtime-self.prevtime))

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
		from numpy import std, mean
		values = self.net_states
		stdev = std(values)
		self.stdevthreshold = mean(values) + 3*stdev
		return (1 if self.netstate >= self.stdevthreshold else 0)

	def median_rule(self):
		values = sorted(self.net_states)
		nval1 = len(values)+1
		median = values[nval1/2-1]
		iqr = values[nval1*3/4-1]-values[nval1/4-1]
		self.medianthreshold = median + int(2.3*iqr)
		return (1 if self.netstate >= self.medianthreshold else 0)

	def made_method(self):
		from numpy import median
		values = self.net_states
		median_value = median(values)
		made = 1.483 * median([abs(v-median_value) for v in values])
		self.madethreshold = median_value + 3*made
		return (1 if self.netstate >= self.madethreshold else 0)
