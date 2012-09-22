class Router(object):
	host = None
	name = None
	ips = None
	neighbours = None
	num_ifs = None
	interfaces = None

	def __init__(self,ip):
		self.host = ip

	def __str__(self):
		result = "Router %s:\n" % self.name
	        result += "        IP addresses:\n"
	        for item in self.ips:
	                result+="                %s\n" % item
	        result+="        Interfaces:\n"
	        for item in self.interfaces:
	                result+="                %s\n" % item
	        result+="        Link-layer neighbours:\n"
	        for item in self.neighbours:
	                result+="                %s\n" % item
		return result
	
class RouterSnmp(Router):
	snmpiface = None	

	def __init__(self, ip):
		super(RouterSnmp,self).__init__(ip)
		from snmpiface import SnmpIface
		self.snmpiface = SnmpIface(host=ip)

	def getTopologyInfo(self):
		self.neighbours = self.snmpiface.getSubtree(self.snmpiface.oid_ipRouteNextHop).values()
	        self.ips = self.snmpiface.getSubtree(self.snmpiface.oid_ipAdEntAddr).values()
	        self.neighbours = list(set(self.neighbours).difference(self.ips))

	def getInfo(self):
		self.name = self.snmpiface.getObject(self.snmpiface.oid_sysName)
	        self.num_ifs = int(self.snmpiface.getObject(self.snmpiface.oid_ifNumber))
	        self.interfaces = self.snmpiface.getBulk(self.snmpiface.oid_ifDescr,self.num_ifs).values()


