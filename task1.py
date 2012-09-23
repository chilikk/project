#!/usr/bin/python

if __name__=='__main__':
	import pickle,sys
	try:
		routers = pickle.load(open('routers.dat','r'))
	except Exception:
		from main import routers
	for router in routers:
		print router
