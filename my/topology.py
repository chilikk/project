from my.router import RouterSnmp

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
			router = RouterSnmp(host)
			router.getTopologyInfo()
			for item in router.neighbours:
				if not item in self.tovisit and not item in self.visited:
					self.tovisit.append(item)
			self.visited += router.ips
			self.routers.append(router)
		del(self.tovisit)
		del(self.visited)
