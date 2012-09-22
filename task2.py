#!/usr/bin/python -O

from task1mp import routers
from multiprocessing import Pool
if __debug__:
	import sys
	from task1mp import starttime

def poll(router):
	time, load = router.pollLinksLoad()
	sys.stderr.write("Polled %s (links load %s): %f\n" % (router.host,load,time-starttime))
	return router

if __name__=='__main__':
	pool = Pool(processes = len(routers))
	routers = pool.map(poll,routers)
