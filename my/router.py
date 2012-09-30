from time import time

class Router(object):
	def __init__(self,ip):
		self.host = ip
		self.name = None
		self.ips = []
		self.neighbours = []
		self.num_ifs = 0
		self.interfaces = []

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
	def __init__(self,ip):
		super(RouterSnmp,self).__init__(ip)
		self.restoresnmpiface()

	def merge(self,router):
		if self.host == router.host:
			self.name = router.name
			self.ips = router.ips
			self.neighbours = router.neighbours
			self.num_ifs = router.num_ifs
			self.interfaces = router.interfaces

	def cleartopickle(self):
		del self.snmpiface
		return self
	
	def restoresnmpiface(self):
		from snmpiface import SnmpIface
		self.snmpiface = SnmpIface(host=self.host)
		return self

	def getTopologyInfo(self):
		for i in range(10):
			try:
				self.neighbours = self.snmpiface.getSubtree(self.snmpiface.oid_ipRouteNextHop).values()
			        self.ips = self.snmpiface.getSubtree(self.snmpiface.oid_ipAdEntAddr).values()
			        self.neighbours = list(set(self.neighbours).difference(self.ips))
				i=0
				break
			except Exception:
				pass
		if i>0:
			raise Exception("Router did not respond for 10 retries")

	def getNumIfs(self):
		try:
	        	self.num_ifs = int(self.snmpiface.getObject(self.snmpiface.oid_ifNumber))
		except Exception:
			raise

	def getInfo(self):
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
		try:
		        currLinksLoad=self.snmpiface.getBulk(self.snmpiface.oid_ifInOctets,self.num_ifs).values()
		except Exception:
			raise
		currTime = time()	
		return (currTime, sum([ int(item) for item in currLinksLoad ]), 0)

	def pollLinksOctetsPackets(self):
                oid = self.snmpiface.oid_ifInOctets
		bulksize = 5*self.num_ifs
		try:
			currLinksLoad=self.snmpiface.getBulk(oid,bulksize,dontmatch=1)
		except Exception:
			raise
                octets, packets = (0,0)
                for key in currLinksLoad:
                        if key[:len(oid)]==oid:
                                octets+=int(currLinksLoad[key])
                        elif key[:len(oid)] in [oid[:len(oid)-1]+s for s in ('1','2','3','4')]:
                                packets+=int(currLinksLoad[key])
                currTime = time()
                return (currTime, octets, packets)
