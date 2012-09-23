#!/usr/bin/python

from my.topology import Topology
from my.debug import debugmsg
from multiprocessing import Process

def getRouterInfo(router):
	router.getInfo()

def getTopology(initial_router):
	topology = Topology(initial_router)
	debugmsg('Started')
	topology.get()
	debugmsg('Topology identified')
	return topology.routers

if __name__=='__main__':
	routers = getTopology('192.168.1.10')
	workers = [ Process(target=getRouterInfo, args=(router,)) for router in routers ]
	[ worker.start() for worker in workers ]
	[ worker.join() for worker in workers ]
	debugmsg('Routers info collected')
	for router in routers:
		print router
		print

