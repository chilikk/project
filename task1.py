#!/usr/bin/python -O

from my.router import RouterSnmp
from multiprocessing import Pool

if __debug__:
	import sys
	from time import time

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
	return router

if __debug__:
	starttime = time()
	sys.stderr.write("%f :: Started\n" % 0)
routers = getTopology()
if __debug__:
	sys.stderr.write("%f :: Topology identified\n" % (time()-starttime))
if __name__=='__main__':
	pool = Pool(processes = len(routers))
	routers = pool.map(getRouterInfo,routers)
	if __debug__:
		sys.stderr.write("%f :: Routers info collected\n" % (time()-starttime))
	for router in routers:
		print router
		print

