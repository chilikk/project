#!/usr/bin/python

from my.netstatistics import NetStatistics
from multiprocessing import Pool
import time, sys, pickle
from my.debug import debugmsg, printmsg, printerrmsg

def poll(routerid):
	return routers[routerid].pollLinksLoad()

pollinterval = 0
num_samples = 30

if __name__=='__main__':
	try:
		routers = pickle.load(open('routers.dat','r'))
		routers = [router.restoresnmpiface() for router in routers]
	except Exception:
		from my.debug import printerrmsg
		printerrmsg('routers.dat not found! run main.py first')
		import sys
		sys.exit()
	stats = NetStatistics()
	nrouters = len(routers)
	pool = Pool(processes = nrouters)
	for i in range(num_samples):
		nexttime = time.time()+pollinterval
		sample = pool.map(poll, range(nrouters))
		stats.addSample(sample)
		netstate, stdev, alarm = stats.getNetState()
		if netstate != "start":
			if stdev:
				printmsg("\t%d\t\t\t%d\t%s" % (netstate, stdev, alarm))
			else:
				printmsg("\t%d" % netstate)
		else:
			printerrmsg("start polling\ntime\t\tnetwork load\tstandard deviation")
		try:
			time.sleep(nexttime-time.time())
		except Exception:
			pass
