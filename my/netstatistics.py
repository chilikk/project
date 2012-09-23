class NetStatistics(object):
	def __init__(self, **kwargs):
		self.net_states = []
		self.prevtime, self.prevload = (None, None)
		self.netstate = None
		self.stdev = None
		self.alarm = ""
		self.states_to_store = 10
		if 'methods' in kwargs:
			self.methods = kwargs['methods']
		else:
			self.methods = ('stdev',)
		
	def addSample(self,pollresult):
		avgtime, totload = self.calc_totload(pollresult)
		if self.netstate:
			self.netstate = self.calc_bandwidth(avgtime, totload)
			if len(self.net_states)==self.states_to_store:
				self.detectOutlier()
				del self.net_states[0]
			self.net_states.append(self.netstate)
		else:
			self.netstate = "start"
		self.prevtime, self.prevload = (avgtime, totload)
	
	def getNetState(self):
		return (self.netstate, self.stdev, self.alarm)

	def calc_totload(self,pollresult):
		avgtime, totload = (.0,0)
                for polltime, loads in pollresult:
                        avgtime+=polltime
                        for load in loads:
                                totload+=int(load)
                avgtime/=len(pollresult)
		return (avgtime, totload)

	def calc_bandwidth(self, avgtime, totload):
                return int((totload-self.prevload)/(avgtime-self.prevtime))

	def detectOutlier(self):
		from numpy import std, mean
		self.stdev = std(self.net_states)
		self.mean = mean(self.net_states)
		self.alarm = "ALARM" if self.netstate >= self.mean+3*self.stdev else ""
		return (self.stdev, self.alarm)
