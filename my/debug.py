if __debug__:
	import sys,time
	starttime = None

def debugmsg(msg):
	if __debug__:
                global starttime
                if not starttime:
                        starttime = time.time()
                        now = 0
                else:
                        now = time.time()-starttime
                sys.stderr.write("%f :: %s\n" % (now, msg))
