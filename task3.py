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
	stats = NetStatistics(methods=('stdev','median','made'), advanced=1)
	nrouters = len(routers)
	pool = Pool(processes = nrouters)
	for i in range(num_samples):
		nexttime = time.time()+pollinterval
		sample = pool.map(poll, range(nrouters))
		stats.addSample(sample)
		netstate, stdevthreshold, alarm = stats.getNetState()
		packetsize, medianthreshold, madethreshold = stats.getAdvParams()
		if stats.netstate != "start":
			if stdevthreshold:
				msg = "%7d %4d\t\t| %7d  %7d  %7d |  %s" % (netstate, packetsize, stdevthreshold, medianthreshold, madethreshold, alarm)
				if alarm=='ALARM':
					msg+="\t%3d\t%s" % stats.getAlarmParams()
				printmsg(msg)
			else:
				printerrmsg("%7d\t%4d\t\t|" % (netstate, packetsize))
		else:
			printerrmsg("start polling\n-----------------------------\ntime\t\tnetwork load, packetsize\t|\tthresholds")
		try:
			time.sleep(nexttime-time.time())
		except Exception:
			pass
