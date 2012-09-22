#!/usr/bin/python -O

from task1mp import routers
from multiprocessing import Pool

def poll(router):
	router.pollLinksLoad()
	return router

if __name__=='__main__':
	pool = Pool(processes = len(routers))
	routers = pool.map(poll,routers)
