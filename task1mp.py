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
	return router

if __name__=='__main__':
	routers = getTopology()
	pool = Pool(processes = len(routers))
	routers = pool.map(getRouterInfo,routers)
	for router in routers:
		print router
		print

