#!/usr/bin/python

from my.router import Router
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
		router = Router(host)
		router.getTopologyInfo()
		tovisit = list_union(tovisit,router.neighbours)
		visited += router.ips
		routers.append(router)
	return routers

def getRouterInfo(router):
	print router
	router.getInfo()
	print router
	return router

def debugmsg(msg):
	if __debug__:
		global starttime
		if not starttime:
			starttime = time()
			now = 0
		else:
			now = time()-startime
		sys.stderr.write("%f :: %s\n" % (now, msg))

starttime = None
debugmsg('Started')
routers = getTopology()
debugmsg('Topology identified')
if __name__=='__main__':
	pool = Pool(processes = len(routers))
	routers = pool.map(getRouterInfo,routers)
	debugmsg('Routers info collected')
	for router in routers:
		print router
		print

