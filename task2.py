#!/usr/bin/python -O

from task1mp import routers
from multiprocessing import Pool
import time
if __debug__:
	import sys
	from task1mp import starttime

def poll(router):
	polltime, load = router.pollLinksLoad()
	if __debug__:
		sys.stderr.write("Polled %s (links load %s): %f\n" % (router.host,load,polltime-starttime))
	return router

if __name__=='__main__':
	pool = Pool(processes = len(routers))
	for i in range(5):
		routers = pool.map(poll,routers)
		time.sleep(10)
	for router in routers:
		print router.linksLoad
		print
