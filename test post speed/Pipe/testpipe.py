#!/usr/bin/env python

import subprocess,time

#++++++++++++++++++++++++++++ simulate_work: internal Function ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# This function simulates the processing of images

# Functionality : 
# The function performs floating point operations that take roughly 0.02 seconds
# 
# Usage: thread.start_new_thread(process_thread)
# 
# Inputs: 
#         None
#
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def simulate_work(num):

	i = 0
	temp = 1
	while(i < num):
		temp = temp * 0.9
		i += 1
	
if __name__ == "__main__":

	start_time = time.time()
	
	p = subprocess.Popen(['python', 'testclient-pipe-buffered.py'], stdin=subprocess.PIPE)

	for i in range(1000):

		simulate_work(300000)
		p.stdin.write(str(i) + ", 100, 0.88, 1.51, 1.51, 1.51, 1.51\n")

	

	time.sleep(0.5)

	p.kill()
 	
	print("--- %s seconds ---" % (time.time() - start_time))

