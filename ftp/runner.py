import subprocess
import time
import os
import signal

p = subprocess.Popen(["ps", "-A"], stdout = subprocess.PIPE)
p.wait()
for string in p.stdout.read().split('\n'):
  if ("xinetd" in string):
    pid = string.split(' ')[1]
    print "the pid of the xinetd is " + str(pid)
    break
for i in range(1000):
	p = subprocess.Popen(["sudo","strace", "-f", "-tt", "-s", "10000", "-o", "output" + str(i) + ".txt", "-p", str(pid)], stdout = subprocess.PIPE)
	time.sleep(4)
	pidOfStrace = p.pid
	os.kill(pidOfStrace, signal.SIGINT)

	print "the pid of strace is " + str(pidOfStrace)