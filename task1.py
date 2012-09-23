#!/usr/bin/python

from my.topology import Topology
from my.debug import debugmsg
from multiprocessing import Pool

def getRouterInfo(routerid):
	router = routers[routerid]
	router.getInfo()
	return router.cleartopickle()
	
def getTopology(initial_router):
	topology = Topology(initial_router)
	debugmsg('Started')
	topology.get()
	debugmsg('Topology identified')
	return topology.routers

if __name__=='__main__':
	routers = getTopology('192.168.1.10')
	nrouters = len(routers)
	pool = Pool(processes = nrouters)
	routersinfo = pool.map(getRouterInfo,range(nrouters))
	for i in range(nrouters):
		routers[i].merge(routersinfo[i])
	debugmsg('Routers info collected')
	print routers.sort(key=lambda router: router.name)
	for router in routers:
		print router
		print

