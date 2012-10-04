#!/usr/bin/python

""" loading the array of router objects from the file and displaying the information """

if __name__=='__main__':
	from main import loadRouters
	routers = loadRouters()
	for router in routers:
		print router
