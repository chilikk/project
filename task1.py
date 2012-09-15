#!/usr/bin/python

from my.snmpiface import SnmpIface

def list_union(a,b):
	for item in b:
		if not item in a:
			a.append(item)
	return a

def getRouterInfo(host):
	router = SnmpIface(host = host)
	routername = router.getObject(router.oid_sysName)
	num_ifs = int(router.getObject(router.oid_ifNumber))
	interfaces = router.getBulk(router.oid_ifDescr,num_ifs).values()
	neighbours = router.getSubtree(router.oid_ipRouteNextHop).values()
	return { 'ip':host, 'name':routername, 'interfaces':interfaces, 'neighbours': list(set(neighbours)) }

def printRouterInfo(info):
	print "Router %s:" % info['ip']
	print "        hostname: %s" % info['name']
	print "        interfaces: "
	for item in info['interfaces']:
		print "                %s" % item
	print
	print "        neighbours: "
	for item in info['neighbours']:
		print "                %s" % item
	print

if __name__=='__main__':
	routers = ['192.168.1.10']
	for router in routers:
		info = getRouterInfo(router)
		printRouterInfo(info)
		routers = list_union(routers,info['neighbours'])
