from time import time

class Router(object):
	def __init__(self,ip):
		self.host = ip
		self.name = None
		self.ips = None
		self.neighbours = None
		self.num_ifs = None
		self.interfaces = None
		from snmpiface import SnmpIface
		self.snmpiface = SnmpIface(host=ip)

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

	def getTopologyInfo(self):
		self.neighbours = self.snmpiface.getSubtree(self.snmpiface.oid_ipRouteNextHop).values()
	        self.ips = self.snmpiface.getSubtree(self.snmpiface.oid_ipAdEntAddr).values()
	        self.neighbours = list(set(self.neighbours).difference(self.ips))

	def getNumIfs(self):
	        self.num_ifs = int(self.snmpiface.getObject(self.snmpiface.oid_ifNumber))

	def getInfo(self):
		print self.snmpiface
		
		self.name = self.snmpiface.getObject(self.snmpiface.oid_sysName)
		print self.name
		self.getNumIfs()
	        self.interfaces = self.snmpiface.getBulk(self.snmpiface.oid_ifDescr,self.num_ifs).values()

	def pollLinksLoad(self):
		if not self.num_ifs:
			self.getNumIfs()
	        currLinksLoad=self.snmpiface.getBulk(self.snmpiface.oid_ifInOctets,self.num_ifs).values()
		currTime = time()
		return (currTime, currLinksLoad)
