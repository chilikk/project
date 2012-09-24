import sys,time
starttime = None

def gettime():
	global starttime
        if not starttime:
                starttime = time.time()
        	now = 0
	return time.time()-starttime
	
def printerrmsg(msg):
	sys.stderr.write("%f :: %s\n" % (gettime(), msg))

def debugmsg(msg):
	if __debug__:
		printerrmsg(msg)

def printmsg(msg):
	print "%.3f\t\t%s" % (gettime(),msg)
