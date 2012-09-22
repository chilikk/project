#!/usr/bin/python

from my.snmpiface import SnmpIface
from multiprocessing import Pool
if __debug__:
	import sys
	from time import time

def list_union(a,b):
	for item in b:
		if not item in a:
			a.append(item)
	return a

def getTopologyInfo(host):
	if __debug__:
		sys.stderr.write('Getting topology info for %s: %f',(host,time()-starttime))
	router = SnmpIface(host = host)
	neighbours = router.getSubtree(router.oid_ipRouteNextHop).values()
	ips = router.getSubtree(router.oid_ipAdEntAddr).values()
	neighbours = list(set(neighbours).difference(ips))
	return { 'ips':ips, 'neighbours':neighbours }


def getRouterInfo(host):
	if __debug__:
		sys.stderr.write('Getting info for %s: %f',(host,time()-starttime))
	router = SnmpIface(host = host)
	routername = router.getObject(router.oid_sysName)
	num_ifs = int(router.getObject(router.oid_ifNumber))
	interfaces = router.getBulk(router.oid_ifDescr,num_ifs).values()
	return { 'name':routername, 'interfaces':interfaces }

def printRouterInfo(info):
	print "Router %s:" % info['name']
	print "        IP addresses: "
	for item in info['ips']:
		print "                %s" % item
	print "        Interfaces: "
	for item in info['interfaces']:
		print "                %s" % item
	print "        Link-layer neighbours: "
	for item in info['neighbours']:
		print "                %s" % item
	print

def getRouterTopologyInfo():
	routers = ['192.168.1.10']
	visited = []
	routerinfo = {}
	for router in routers:
		if router in visited:
			continue
		info = getTopologyInfo(router)
		routers = list_union(routers,info['neighbours'])
		visited += info['ips']
		routerinfo[router]=info
	return routerinfo

if __name__=='__main__':
	if __debug__: 
		starttime = time()
		sys.stderr.write("Program started: %f" % 0)
	routerinfo = getRouterTopologyInfo()
	if __debug__:
		sys.stderr.write("Topology discovered: %f" % (time()-starttime))
	routers = routerinfo.keys()
	pool = Pool(processes = len(routers))
	if __debug__:
		sys.stderr.write("Pool started: %f" % (time()-starttime))
	info = pool.map(getRouterInfo,routers)
	if __debug__:
		sys.stderr.write("Pool finished: %f" % (time()-starttime))
	info = zip(routers,info)
	for router, data in info:
		for key in data.keys():
			routerinfo[router][key]=data[key]
		printRouterInfo(routerinfo[router])


