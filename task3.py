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
	stats = NetStatistics(methods=('stdev','median','made'))
	nrouters = len(routers)
	pool = Pool(processes = nrouters)
	for i in range(num_samples):
		nexttime = time.time()+pollinterval
		sample = pool.map(poll, range(nrouters))
		stats.addSample(sample)
		netstate, stdevthreshold, alarm = stats.getNetState()
		medianthreshold, madethreshold = stats.getThresholds()
		if netstate != "start":
			if stdevthreshold:
				msg = "%7d\t| %7d  %7d  %7d |\t%s" % (netstate, stdevthreshold, medianthreshold, madethreshold, alarm)
				if alarm=='ALARM':
					msg+="\t%3d\t%s" % stats.getAlarmParams()
				printmsg(msg)
			else:
				printerrmsg("\t%7d" % netstate)
		else:
			printerrmsg("start polling\ntime\t\tnetwork load\tthresholds")
		try:
			time.sleep(nexttime-time.time())
		except Exception:
			pass
