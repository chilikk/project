#!/usr/bin/python



from my.topology import Topology
from my.messages import debugmsg
from multiprocessing import Pool
import pickle
from defaults import initialRouter, fileRoutersData

def getRouterInfo(routerid): # this function is executed by each thread: passing the number of the router
	""" subprocess for getting router configuration information """
	router = routers[routerid]
	router.getInfo()
	return router.cleartopickle() # return router object
	
def getTopology(initial_router): # passing the IP address to start with
	""" discovering topology """
	topology = Topology(initial_router)
	debugmsg('Started')
	topology.get()
	debugmsg('Topology identified')
	return topology.routers # return array of the router objects

def loadRouters():
	""" read the array of router objects from the file """
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
	return routers #return array of the router objects

if __name__=='__main__':
	routers = getTopology(initialRouter) # getting topology
	nrouters = len(routers)
	pool = Pool(processes = nrouters)
	routersinfo = pool.map(getRouterInfo,range(nrouters)) # starting multiple subprocesses to acquire configuration information from all the routers
	for i in range(nrouters):
		routers[i].merge(routersinfo[i])
	debugmsg('Routers info collected')
	routers.sort(key=lambda router: int(router.name[1:]))
	def saveRoutersData(routers): # passing array of router objects
		""" save the array of router objects to the file """
		from defaults import fileRoutersData
		return pickle.dump([router.cleartopickle() for router in routers],open(fileRoutersData,'w')) # return result of the operation
	saveRoutersData(routers) # save the array of router objects in the file
