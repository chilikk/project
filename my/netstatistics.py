class NetStatistics(object):
	def __init__(self):
		self.net_states = []
		self.prevtime, self.prevload = (None, None)
		self.netstate = None
		self.states_to_store = 40
		
	def addSample(self,pollresult):
		avgtime, totload = self.calc_totload(pollresult)
		if self.netstate:
			self.netstate = self.calc_bandwidth(avgtime, totload)
			self.net_states.append(self.netstate)
			if len(self.net_states)>self.states_to_store:
				del self.net_states[0]
		else:
			self.netstate = "start"
		self.prevtime, self.prevload = (avgtime, totload)
	
	def getNetState(self):
		return self.netstate

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
