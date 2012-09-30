#!/usr/bin/python

from my.topology import Topology
from my.messages import debugmsg
from multiprocessing import Pool
import pickle
from defaults import initialRouter, fileRoutersData

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

def loadRouters():
	try:
                f = open(fileRoutersData, 'r')
                routers = pickle.load(f)
                f.close()
                routers = [router.restoresnmpiface() for router in routers]
        except Exception:
                from my.messages import printerrmsg
                printerrmsg(fileRoutersData+' not found! run main.py first')
                import sys
                sys.exit()
	return routers

if __name__=='__main__':
	routers = getTopology(initialRouter)
	nrouters = len(routers)
	pool = Pool(processes = nrouters)
	routersinfo = pool.map(getRouterInfo,range(nrouters))
	for i in range(nrouters):
		routers[i].merge(routersinfo[i])
	debugmsg('Routers info collected')
	routers.sort(key=lambda router: int(router.name[1:]))
	def saveRoutersData(routers):
		from defaults import fileRoutersData
		return pickle.dump([router.cleartopickle() for router in routers],open(fileRoutersData,'w'))
	saveRoutersData(routers)
