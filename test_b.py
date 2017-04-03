import os,sys,subprocess
from subprocess import Popen
pid = Popen(["python","test_other.py"]).pid
print(pid)


