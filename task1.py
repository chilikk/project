#!/usr/bin/python

if __name__=='__main__':
	import pickle,sys
	from defaults import fileRoutersData
	try:
		f = open(fileRoutersData,'r')
		routers = pickle.load(f)
		f.close()
	except Exception:
		from my.debug import printerrmsg
		import sys
		printerrmsg('%s not found! run main.py first' % fileRoutersData)
		sys.exit()
	for router in routers:
		print router
