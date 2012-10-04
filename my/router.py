from time import time

class Router(object):
	""" data structure for the router. stores the topology-related information and configuration information """
	def __init__(self,ip):
		self.host = ip # IP address to connect
		self.name = None # system name
		self.ips = [] # list of IP addresses assigned
		self.neighbours = [] # list of link-layer neighbours
		self.num_ifs = 0 # number of interfaces
		self.interfaces = [] # list of interface names

	def __str__(self):
		result = "Router %s:\n" % (self.name or 'N/A')
		try:
		        result += "        IP addresses:\n"
		        for item in self.ips:
	        	        result+="                %s\n" % item
		except Exception:
			pass
		try:
		        result+="        Interfaces:\n"
		        for item in self.interfaces:
		                result+="                %s\n" % item
		except Exception:
			pass
		try:
		        result+="        Link-layer neighbours:\n"
		        for item in self.neighbours:
		                result+="                %s\n" % item
		except Exception:
			pass
		return result

class RouterSnmp(Router):
	""" an extension for the Router data structure which binds a router object to an SNMP interface to this router """
	def __init__(self,ip):
		super(RouterSnmp,self).__init__(ip)
		self.restoresnmpiface() # create an SNMP interface

	def merge(self,router):
		""" copy the information from the passed object to self """
		if self.host == router.host:
			self.name = router.name
			self.ips = router.ips
			self.neighbours = router.neighbours
			self.num_ifs = router.num_ifs
			self.interfaces = router.interfaces

	def cleartopickle(self):
		""" return Router data structure without SNMP interface """
		del self.snmpiface
		return self
	
	def restoresnmpiface(self):
		""" bind to an SNMP interface """
		from snmpiface import SnmpIface
		self.snmpiface = SnmpIface(host=self.host)
		return self

	def getTopologyInfo(self):
		""" query the router for the topology-related information """
		for i in range(10):
			try:
				self.neighbours = self.snmpiface.getSubtree(self.snmpiface.oid_ipRouteNextHop).values() # all the routing table Next-Hop values
			        self.ips = self.snmpiface.getSubtree(self.snmpiface.oid_ipAdEntAddr).values()
			        self.neighbours = list(set(self.neighbours).difference(self.ips)) # neighbours are only those which do not belong to the router itself
				i=0
				break
			except Exception:
				pass
		if i>0:
			raise Exception("Router did not respond for 10 retries")

	def getNumIfs(self):
		""" get the number of network interfaces """
		try:
	        	self.num_ifs = int(self.snmpiface.getObject(self.snmpiface.oid_ifNumber))
		except Exception:
			raise

	def getInfo(self):
		""" get the configuration information of the router """
		for i in range(10):
			try:
				self.name = self.snmpiface.getObject(self.snmpiface.oid_sysName)
				self.getNumIfs()
				self.interfaces = self.snmpiface.getBulk(self.snmpiface.oid_ifDescr,self.num_ifs).values()
				i=0
				break
			except Exception:
				pass
		if i>0:
			raise Exception("Router did not respond for 10 retries")

	def pollLinksLoad(self):
		""" poll the router for the link states and compute the total router state """
		try:
		        currLinksLoad=self.snmpiface.getBulk(self.snmpiface.oid_ifInOctets,self.num_ifs).values()
		except Exception:
			raise
		currTime = time()	
		return (currTime, sum([ int(item) for item in currLinksLoad ]), 0)

	def pollLinksOctetsPackets(self):
		""" poll the router for the number of bytes and number of packets received on each link 
		computing the total router state"""
                oid = self.snmpiface.oid_ifInOctets
		bulksize = 5*self.num_ifs # polling the router for ifInOctets, ifInUcastPackets, ifInNUcastPackets, ifInDiscards, ifInErrors in a single query using getbulk
		try:
			currLinksLoad=self.snmpiface.getBulk(oid,bulksize,dontmatch=1) # dontmatch=1 because they are not in the same subtree
		except Exception:
			raise
                octets, packets = (0,0)
                for key in currLinksLoad:
                        if key[:len(oid)]==oid:
                                octets+=int(currLinksLoad[key]) # calculate the total number of bytes received
                        elif key[:len(oid)] in [oid[:len(oid)-1]+s for s in ('1','2','3','4')]:
                                packets+=int(currLinksLoad[key]) # calculate the total number of packets received
                currTime = time()
                return (currTime, octets, packets)
