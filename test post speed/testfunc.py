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

	for i in range(1000):

		simulate_work(300000)

	time.sleep(0.5)
	
	total_time = time.time() - start_time
	avg_time = total_time/1000
 	
	print("---average time %s seconds ---" % (avg_time))

