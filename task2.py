#!/usr/bin/python

from task1 import routers
import time, sys
if __debug__:
	from task1 import starttime
from my.polling import Polling

if __name__=='__main__':
	polling = Polling(routers)
	for i in range(5):
		nexttime = time.time()+10
		network_state = polling.polling()
		if __debug__:
			sys.stderr.write("%f :: " % (time.time()-starttime))
		if network_state:
			print "+%f\t\t%d" % network_state
		else:
			sys.stderr.write("start polling\ntime difference\t\ttotal network bandwidth\n")
		try:
			time.sleep(nexttime-time.time())
		except Exception:
			sys.exc_clear()
