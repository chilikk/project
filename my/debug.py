import sys,time
starttime = None

def gettime():
	global starttime
        if not starttime:
                starttime = time.time()
        	now = 0
	return time.time()-starttime
	
def printerrmsg(msg):
	sys.stderr.write("%4.2f\t::\t%s\n" % (gettime(), msg))

def debugmsg(msg):
	if __debug__:
		printerrmsg(msg)

def printmsg(msg):
	print "%4.2f\t::\t%s" % (gettime(),msg)
