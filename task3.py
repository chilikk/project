#!/usr/bin/python

from my.netstatistics import NetStatistics
from multiprocessing import Pool
import time, sys, pickle
from my.debug import debugmsg, printmsg, printerrmsg
from defaults import pollinterval, num_samples
from main import loadRouters

def poll(routerid):
	return routers[routerid].pollLinksOctetsPackets()

if __name__=='__main__':
	routers = loadRouters()
	stats = NetStatistics(methods=('stdev','median','dumb'))
	nrouters = len(routers)
	pool = Pool(processes = nrouters)
	for i in range(num_samples):
		nexttime = time.time()+pollinterval
		sample = pool.map(poll, range(nrouters))
		stats.addSample(sample)
		netstate, stdevthreshold, alarm = stats.getNetState()
		medianthreshold, dumbthreshold = stats.getThresholds()
		if netstate != "start":
			if stdevthreshold:
				msg = "%d\t(%d\t%d\t%d)\t%s" % (netstate, stdevthreshold, medianthreshold, dumbthreshold, alarm)
				if alarm=='ALARM':
					msg+="\t%d\t%s" % stats.getAlarmParams()
			else:
				msg = "\t%d" % netstate
			printmsg(msg)
		else:
			printerrmsg("start polling\ntime\t\tnetwork load\t\tthresholds")
		try:
			time.sleep(nexttime-time.time())
		except Exception:
			pass
