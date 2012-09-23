#!/usr/bin/python

from my.topology import Topology
from my.debug import debugmsg
from multiprocessing import Pool

def getRouterInfo(router):
	router.getInfo()
	return router

topology = Topology('192.168.1.10')
debugmsg('Started')
topology.get()
routers = topology.routers
debugmsg('Topology identified')
if __name__=='__main__':
	pool = Pool(processes = len(routers))
	routers = pool.map(getRouterInfo,routers)
	debugmsg('Routers info collected')
	for router in routers:
		print router
		print

