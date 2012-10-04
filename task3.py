#!/usr/bin/python

from my.netstatistics import NetStatistics
from multiprocessing import Pool
import time, sys, pickle
from my.messages import debugmsg, printmsg, printerrmsg
from defaults import pollinterval, num_samples
from main import loadRouters

def poll(routerid):
	""" subprocess for polling a single router for links load and the number of packets received """
	try:
		return routers[routerid].pollLinksOctetsPackets()
	except Exception:
		return None

if __name__=='__main__':
	routers = loadRouters() # load from the file
	stats = NetStatistics(methods=('stdev','median','made'), advanced=1) # init Statistics with multiple outlier detection methods
	nrouters = len(routers)
	pool = Pool(processes = nrouters)
	for i in range(num_samples):
		nexttime = time.time()+pollinterval
		sample = pool.map(poll, range(nrouters)) # running polling in multiple threads
		try:
			stats.addSample(sample) # put the polling results into the Network Statistics object
		except Exception:
			printerrmsg("Router(s) didn't respond")
			continue
		netstate, stdevthreshold, alarm = stats.getNetState() # get the current network state from the Statistics object
		packetsize, medianthreshold, madethreshold = stats.getAdvParams() # get the additional network state parameters
		if stats.netstate != "start":
			if stdevthreshold:
				msg = "%7d\t\t%4d\t\t| %7d  %7d  %7d |  %s" % (netstate, packetsize, stdevthreshold, medianthreshold, madethreshold, alarm)
				if alarm=='ALARM':
					msg+="\t%3d\t%s" % stats.getAlarmParams() # if there is an alarm -> get the probability and the attack type
				printmsg(msg)
			else:
				printerrmsg("%7d\t\t%4d\t\t|" % (netstate, packetsize))
		else:
			printerrmsg("start polling\n-----------------------------\ntime\t\tnetwork load, packetsize\t|\tthresholds")
		try:
			time.sleep(nexttime-time.time())
		except Exception:
			pass
