import subprocess
import os
import sys
import collections
import socket
import signal


p = subprocess.Popen(["ps", "-A"], stdout = subprocess.PIPE)
p.wait()
for string in p.stdout.read().split('\n'):
	if ("unrealircd" in string):
		pid = string.split(' ')[1]
		print "the pid of the unrealircd is " + str(pid)
		break


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ("10.0.2.8", 8000)
sock.connect(server_address)
print "connected to the server!"
num = 0

while num < 10000:
	res = sock.recv(100)
	if (res == 'ready') :
		p = subprocess.Popen(["sudo","strace", "-f", "-tt", "-s", "10000", "-o", "output" + str(num) + ".txt", "-p", str(pid)], stdout = subprocess.PIPE)
		pidOfStrace = p.pid
		print "the pid of strace is " + str(pidOfStrace)
		sock.sendall('start')
		res = sock.recv(100)
		os.kill(pidOfStrace, signal.SIGINT)
		if (res == 'success'):
			num += 1
			print "the server returns success!!"
		else:
			print "the server returns failure :("
			os.unlink("output" + str(num)+ ".txt")

sock.sendall('stop')
sock.close()
