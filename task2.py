#!/usr/bin/python

from my.netstatistics import NetStatistics
from multiprocessing import Pool
import time, sys, pickle
from my.debug import debugmsg, printmsg, printerrmsg

def poll(routerid):
	return routers[routerid].pollLinksLoad()

if __name__=='__main__':
	try:
		routers = pickle.load(open('routers.dat','r'))
		routers = [router.restoresnmpiface() for router in routers]
	except Exception:
		import main
	stats = NetStatistics()
	nrouters = len(routers)
	pool = Pool(processes = nrouters)
	for i in range(5):
		nexttime = time.time()+10
		sample = pool.map(poll, range(nrouters))
		stats.addSample(sample)
		netstate = stats.getNetState()
		if netstate != "start":
			printmsg("%d" % network_state)
		else:
			printerrmsg("start polling\ntime\t\ttotal network load")
		try:
			time.sleep(nexttime-time.time())
		except Exception:
			pass
