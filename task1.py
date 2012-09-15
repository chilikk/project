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
	num_ifs = router.getObject(router.oid_ifNumber)
	interfaces = [ value for key,value in router.getBulk(router.oid_ifDescr,num_ifs) ]
	neighbours = [ value for key,value in router.getSubtree(router.oid_ipRouteNextHop) ]
	return { 'name':routername, 'interfaces':interfaces, 'neighbours':neighbours }

def printRouterInfo(info):
	print "        hostname: %s" % info['name']
	print "        interfaces: ",
	for item in info['interfaces']:
		print item,
	print
	print "        neighbours: "
	for item in info['neighbours']:
		print "                %s" % item
	print

if __name__=='__main__':
	info = getRouterInfo('192.168.10.1')
	printRouterInfo(info)
