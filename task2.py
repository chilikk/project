#!/usr/bin/python -O

from task1mp import routers
from multiprocessing import Pool
import time
if __debug__:
	import sys
	from task1mp import starttime

def poll(router):
	return router.pollLinksLoad()

if __name__=='__main__':
	pool = Pool(processes = len(routers))
	net_states = []
	prevtime, prevload = (None, None)
	for i in range(20):
		nexttime = time.time()+10
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
			print "%f\t\t%d\t\t%d" % (difftime, bandwidth ,totload)
		else:
			print "start\t\t\t%d" % totload
		prevtime, prevload = (avgtime, totload)
		time.sleep(nexttime-time.time())
	print net_states
