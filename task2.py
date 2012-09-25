#!/usr/bin/python

from my.netstatistics import NetStatistics
from multiprocessing import Pool
import time
from my.debug import printmsg, printerrmsg
from defaults import pollinterval, num_samples
from main import loadRouters

def poll(routerid):
	return routers[routerid].pollLinksLoad()

if __name__=='__main__':
	routers = loadRouters()
	stats = NetStatistics()
	nrouters = len(routers)
	pool = Pool(processes = nrouters)
	for i in range(num_samples):
		nexttime = time.time()+pollinterval
		sample = pool.map(poll, range(nrouters))
		stats.addSample(sample)
		netstate, threshold, alarm = stats.getNetState()
		if netstate != "start":
			if threshold:
				printmsg("%7d\t|  %7d  |  %s" % (netstate, threshold, alarm))
			else:
				printerrmsg("\t%7d" % netstate)
		else:
			printerrmsg("start polling\n--------------------------\ntime\t\tnetwork load\t\talarm threshold")
		try:
			time.sleep(nexttime-time.time())
		except Exception:
			pass
