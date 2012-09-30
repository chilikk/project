#!/usr/bin/python

if __name__=='__main__':
	from main import loadRouters
	routers = loadRouters()
	for router in routers:
		print router
