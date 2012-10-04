import sys,time
starttime = None

def gettime():
	""" get the time in seconds since the first message program outputs """
	global starttime
        if not starttime:
                starttime = time.time()
        	now = 0
	return time.time()-starttime
	
def printerrmsg(msg):
	""" output timestamp and message into stderr """
	sys.stderr.write("%7.2f\t::\t%s\n" % (gettime(), msg))

def debugmsg(msg):
	""" only in debug mode """
	if __debug__:
		printerrmsg(msg)

def printmsg(msg):
	""" output timestamp and message into stdout """
	print "%7.2f\t::\t%s" % (gettime(),msg)
