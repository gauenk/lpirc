#!/usr/bin/env python

import time
import subprocess

#l = "hello"

p = subprocess.Popen(['python', 'test.py'], stdin = subprocess.PIPE)
l = [[0.5,0.1,0.3], 0.5]

for i in range(100):
	l.append(0.0023542)

p.stdin.write(str(l) + "\n")

time.sleep(0.5)

p.kill()

