#!/usr/bin/python

from my.topology import Topology
from my.debug import debugmsg
from multiprocessing import Pool#Process

def getRouterInfo(routerid):
	router = routers[routerid]
	router.getInfo()
	return router
	
def getTopology(initial_router):
	topology = Topology(initial_router)
	debugmsg('Started')
	topology.get()
	debugmsg('Topology identified')
	return topology.routers

if __name__=='__main__':
	routers = getTopology('192.168.1.10')
	#workers = [ Process(target=getRouterInfo, args=(router,)) for router in routers ]
	#[ worker.start() for worker in workers ]
	#[ worker.join() for worker in workers ]
	nrouters = len(routers)
	pool = Pool(processes = nrouters)
	routers = pool.map(getRouterInfo,range(nrouters))
	debugmsg('Routers info collected')
	for router in routers:
		print router
		print

