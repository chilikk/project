from my.router import Router
from copy import deepcopy

class Topology(object):
	def __init__(self,starting_router):
		self.tovisit = [starting_router]
		self.visited = []
		self.routers = []
	
	def get(self):
		for host in self.tovisit:
			if host in self.visited:
				continue
			index = len(self.routers)
			self.routers.append(Router(host))
			self.routers[index].getTopologyInfo()
			for item in self.routers[index].neighbours:
				if not item in self.tovisit and not item in self.visited:
					self.tovisit.append(item)
			self.visited += self.routers[index].ips
			#self.routers.append(router)
			for router1 in self.routers:
				print router1.snmpiface.transport
		del(self.tovisit)
		del(self.visited)
