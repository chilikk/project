#!/usr/bin/python -O

from task1mp import routers,pool

def poll(router):
	router.pollLinksLoad()
	return router

if __name__=='__main__':
	routers = pool.map(poll,routers)
