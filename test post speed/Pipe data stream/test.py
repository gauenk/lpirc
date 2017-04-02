#!/usr/bin/env python

import time,sys

while (True):

	try:
		line = raw_input()
		l = eval(line)
		print (l[0])
	except:
		time.sleep(0.1)
	
	
