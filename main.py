#!/usr/bin/python

from my.topology import Topology
from my.debug import debugmsg
from multiprocessing import Pool
import pickle
from defaults import initialRouter

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

def saveRoutersData(routers):
	from defaults import fileRoutersData
	return pickle.dump([router.cleartopickle() for router in routers],open(fileRoutersData,'w'))

routers = getTopology(initialRouter)
nrouters = len(routers)
pool = Pool(processes = nrouters)
routersinfo = pool.map(getRouterInfo,range(nrouters))
for i in range(nrouters):
	routers[i].merge(routersinfo[i])
debugmsg('Routers info collected')
routers.sort(key=lambda router: int(router.name[1:]))
if __name__=='__main__':
	saveRoutersData(routers)
