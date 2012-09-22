#!/usr/bin/python

from my.router import RouterSnmp
from multiprocessing import Pool

def list_union(a,b):
	for item in b:
		if not item in a:
			a.append(item)
	return a

def getTopology():
	tovisit, visited, routers = (['192.168.1.10'],[],[])
	for host in tovisit:
		if host in visited:
			continue
		router = RouterSnmp(host)
		router.getTopologyInfo()
		tovisit = list_union(tovisit,router.neighbours)
		visited += router.ips
		routers.append(router)
	return routers

def getRouterInfo(router):
	router.getInfo()

if __name__=='__main__':
	if __debug__: 
		starttime = time()
		sys.stderr.write("Program started: %f\n" % 0)
	routers = getTopology()
	if __debug__:
		sys.stderr.write("Topology discovered: %f\n" % (time()-starttime))
	pool = Pool(processes = len(routers))
	if __debug__:
		sys.stderr.write("Pool started: %f\n" % (time()-starttime))
	info = pool.map(getRouterInfo,routers)
	if __debug__:
		sys.stderr.write("Pool finished: %f\n" % (time()-starttime))
	for router in routers:
		print router
		print

