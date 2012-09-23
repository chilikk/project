#!/usr/bin/python

if __name__=='__main__':
	import pickle,sys
	try:
		routers = pickle.load(open('routers.dat','r'))
	except Exception:
		from my.debug import printerrmsg
		import sys
		printerrmsg('routers.dat not found! run main.py first')
		sys.exit()
	for router in routers:
		print router
