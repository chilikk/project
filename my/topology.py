from my.router import RouterSnmp

class Topology(object):
	""" the object discovers the topology of the network and stores the array of the routers found in the network """
	def __init__(self,starting_router):
		self.tovisit = [starting_router] # list of router IP's that are yet to be visited
		self.visited = [] # list of router IP's that have already been visited
		self.routers = [] # array of discovered routers (Router objects)
	
	def get(self):
		""" discover the network topology """
		for host in self.tovisit:
			if host in self.visited:
				continue # don't visit the router twice
			index = len(self.routers)
			router = RouterSnmp(host)
			router.getTopologyInfo() # query the router for the information which is relevant to topology
			for item in router.neighbours:
				if not item in self.tovisit and not item in self.visited:
					self.tovisit.append(item)
			self.visited += router.ips
			self.routers.append(router) # put the discovered router into the list
		del(self.tovisit)
		del(self.visited)
