#!/usr/bin/python -O

from task1mp import routers
from multiprocessing import Pool
import time, sys
if __debug__:
	from task1mp import starttime

def poll(router):
	return router.pollLinksLoad()

class Polling(object):
	def __init__(self,routers):
		self.routers = routers
		self.pool = Pool(processes = len(routers))
		self.net_states = []
		self.prevtime, self.prevload = (None, None)
		self.notfirst = False
		
	def poll(router):
		return router.pollLinksLoad()

	def polling(self):
		pollresult = self.pool.map(Polling.poll, self.routers)
		avgtime, totload = self.calc_totload(pollresult)
		if self.notfirst:
			difftime, bandwidth = calc_bandwidth(avgtime, totload)
		else:
			self.notfirst = True
			difftime, bandwidth = (None, None)
		self.prevtime, self.prevload = (avgtime, totload)
		return (difftime, bandwidth)
		

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

if __name__=='ololo':
	pool = Pool(processes = len(routers))
	net_states = []
	prevtime, prevload = (None, None)
	for i in range(20):
		nexttime = time.time()+20
		pollresult = pool.map(poll,routers)
		avgtime, totload = (.0,0)
		for polltime, loads in pollresult:
			avgtime+=polltime
			for load in loads:
				totload+=int(load)
		avgtime/=len(pollresult)
		if prevtime and prevload:
			difftime = avgtime-prevtime
			bandwidth = int((totload-prevload)/difftime)
			net_states.append((difftime,bandwidth))
			print "+%f\t\t%d" % (difftime, bandwidth)
		else:
			sys.stderr.write("start\ntime difference\t\ttotal network bandwidth\n")
		prevtime, prevload = (avgtime, totload)
		try:
			time.sleep(nexttime-time.time())
		except Exception:
			sys.exc_clear()
	print net_states

if __name__=='__main__':
	polling = Polling(routers)
	for i in range(5):
		nexttime = time.time()+20
		network_state = polling.polling()
		if network_state[0]:
			print "+%f\t\t%d" % network_state
		else:
			sys.stderr.write("start polling\ntime difference\t\ttotal network bandwidth\n")
		try:
			time.sleep(nexttime-time.time())
		except Exception:
			sys.exc_clear()
	print polling.net_states
			
