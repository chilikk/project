from defaults import storeNetStates
from numpy import std, mean, median

class NetStatistics(object):
	""" the class computes the network state from the set of link states, stores the 
	defined number of network states and implements outlier detection techniques """
	def __init__(self, **kwargs):
		self.state = 'initialization' # also 'training', 'detection'
		self.net_states = [] # array of previous network states
		self.prevtime, self.prevload, self.prevpps = (None, None, None) # the previous network state
		self.netstate = None # the current network state
		self.stdevthreshold = None # Standard Deviation method threshold
		self.medianthreshold = None # Median rule threshold
		self.madethreshold = None # MADe method threshold
		self.alarm = "" # can be "" or "alarm"
		self.alarmprobability = 0 # in percents
		self.attacktype = "" # can be "DoS attack" or "Flash crowd"
		self.states_to_store = storeNetStates # number of network states to store, loaded from defaults.py
		self.methods = (kwargs['methods'] if 'methods' in kwargs else ('stdev',)) # only Standard Deviation method by default
		self.methodprobability = 100./len(self.methods) # the 'weight' of a single method when counting total probability of alarm
		
	def addSample(self,pollresult):
		""" input: array of network load values obtained from all the routers
		    calculate total load and detecting an attack
		    save the result in the object variables
		"""
		try:
			avgtime, totload, totpps = self.calc_totload(pollresult)
		except Exception:
			raise
		if self.state == 'initialization': # only the 1st step
			self.netstate = 'start'
			self.state = 'training'
		elif self.state == 'training': # next storeNetStates steps
			self.netstate = self.calc_bandwidth(avgtime, totload, totpps)
			self.net_states.append(self.netstate)
			if len(self.net_states)==self.states_to_store:
				self.state = 'detection'
		elif self.state == 'detection': # fully functional operation
			self.netstate = self.calc_bandwidth(avgtime, totload, totpps)
			self.detectOutlier() # apply the outlier detection techniques
			if not self.alarm:
				del self.net_states[0]
				self.net_states.append(self.netstate)
			else:
				self.attacktype = self.attack_type() if self.netstate[1]!=0 else "" # determine the type of the attack in case of alarm
		self.prevtime, self.prevload, self.prevpps = (avgtime, totload, totpps)
	
	def getNetState(self):
		return (self.netstate[0], self.stdevthreshold, self.alarm)

	def getAdvParams(self):
		return (self.netstate[1], self.medianthreshold, self.madethreshold)

	def getAlarmParams(self):
		return (self.alarmprobability, self.attacktype)

	def calc_totload(self,pollresult):
		""" calculate the global network state out of single values received from the routers """
		avgtime, totload, totpps = (.0,0,0)
		try:
	                for polltime, load, packetload in pollresult:
	                        avgtime+=polltime # calculating average time of response among all the routers
	                        totload+=int(load) # total load
				totpps+=int(packetload) # total amount of packets
		except Exception:
			raise
                avgtime/=len(pollresult)
		return (avgtime, totload, totpps)

	def calc_bandwidth(self, avgtime, totload, totpps):
		""" calculate the total network load in BPS and average packet size based on network state information """
		while totload <= self.prevload:
			totload+=2**32 # in case the counter on the router was reset
		while totpps <= self.prevpps:
			totpps+=2**32 # in case the counter on the router was reset
                bandwidth = (totload-self.prevload)*1./(avgtime-self.prevtime)
		packetsize = 0 if totpps==0 else (totload-self.prevload)*1./(totpps-self.prevpps)
		return (int(bandwidth), int(packetsize))

	def detectOutlier(self):
		""" run one or more outlier detection methods according to the settings """
		self.alarmprobability = 0.
		if ('stdev' in self.methods):
			self.alarmprobability += self.stdev_method()
		if ('median' in self.methods):
			self.alarmprobability += self.median_rule()
		if ('made' in self.methods):
			self.alarmprobability += self.made_method()
		self.alarmprobability *= self.methodprobability # calculate total alarm probability
		self.alarmprobability = int(self.alarmprobability)
		self.alarm = ("ALARM" if self.alarmprobability > 50 else "") # raise alarm is probability if over 50%
		
	def stdev_method(self):
		""" Standard deviation outlier detection method """
		values = [i[0] for i in self.net_states]
		stdev = std(values)
		self.stdevthreshold = mean(values) + 3*stdev
		return (1 if self.netstate[0] >= self.stdevthreshold else 0)

	def median_rule(self):
		""" Median rule outlier detection method """
		values = sorted([i[0] for i in self.net_states])
		nval1 = len(values)+1
		median_value = values[nval1/2-1]
		iqr = values[nval1*3/4-1]-values[nval1/4-1]
		self.medianthreshold = median_value + int(2.3*iqr)
		return (1 if self.netstate[0] >= self.medianthreshold else 0)

	def made_method(self):
		""" MADe method outlier detection method """
		values = [i[0] for i in self.net_states]
		median_value = median(values)
		made = 1.483 * median([abs(v-median_value) for v in values])
		self.madethreshold = median_value + 3*made
		return (1 if self.netstate[0] >= self.madethreshold else 0)

	def attack_type(self):
		""" attack type detection using Standard deviation method applied to the average packet size in the network """
		values = [i[1] for i in self.net_states]
		threshold = mean(values)-3*std(values)
		threshold = threshold if threshold>=0 else 0
		return ("DoS attack" if self.netstate[1] <= threshold else "Flash crowd")+" (packet size threshold %d)" % threshold
