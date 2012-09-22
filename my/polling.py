#!/usr/bin/python -O

from multiprocessing import Pool
import time

def poll(router):
	return router.pollLinksLoad()

class Polling(object):
	def __init__(self,routers):
		self.routers = routers
		self.pool = Pool(processes = len(routers))
		self.net_states = []
		self.prevtime, self.prevload = (None, None)
		self.notfirst = False
		
	def polling(self):
		pollresult = self.pool.map(poll, self.routers)
		avgtime, totload = self.calc_totload(pollresult)
		if self.notfirst:
			network_state = self.calc_bandwidth(avgtime, totload)
			self.net_states.append(network_state[1])
		else:
			self.notfirst = True
			network_state = None
		self.prevtime, self.prevload = (avgtime, totload)
		return network_state
		

	def calc_totload(self,pollresult):
		avgtime, totload = (.0,0)
                for polltime, loads in pollresult:
                        avgtime+=polltime
                        for load in loads:
                                totload+=int(load)
                avgtime/=len(pollresult)
		return (avgtime, totload)

	def calc_bandwidth(self, avgtime, totload):
		difftime = avgtime-self.prevtime
                bandwidth = int((totload-self.prevload)/difftime)
                return (difftime,bandwidth)
