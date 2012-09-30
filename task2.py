#!/usr/bin/python

from my.netstatistics import NetStatistics
from multiprocessing import Pool
import time
from my.messages import printmsg, printerrmsg
from defaults import pollinterval, num_samples
from main import loadRouters

def poll(routerid):
	try:
		return routers[routerid].pollLinksLoad()
	except Exception:
		return None

if __name__=='__main__':
	routers = loadRouters()
	stats = NetStatistics()
	nrouters = len(routers)
	pool = Pool(processes = nrouters)
	for i in range(num_samples):
		nexttime = time.time()+pollinterval
		sample = pool.map(poll, range(nrouters))
		try:
			stats.addSample(sample)
		except Exception:
			printerrmsg("Router(s) didn't respond")
			continue
		netstate, threshold, alarm = stats.getNetState()
		if stats.netstate != "start":
			if threshold:
				printmsg("%7d\t\t|  %7d  |  %s" % (netstate, threshold, alarm))
			else:
				printerrmsg("%7d\t\t|" % netstate)
		else:
			printerrmsg("start polling\n-----------------------------\ntime\t\tnetwork load\t| threshold")
		try:
			time.sleep(nexttime-time.time())
		except Exception:
			pass
