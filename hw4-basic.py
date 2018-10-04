import socket
import json
import sys

ip = "127.0.0.1"
port = 5566
bank = [[0 for x in range(5)] for x in range(10000)] #name action id port money
i = 0

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((ip, port))

while True:
	data,addr = s.recvfrom(1024)
	data = data.decode("UTF-8")
	data = json.loads(data)
	ip = addr[0]
	port = addr[1]
	if(data['action'] == "init"):
		j = -1
		while j < i :
			j = j+1
			if(bank[j][2] == data['account_id']):
				data = {'message' : 'account_id has been registered'}
				data = json.dumps(data)
				s.sendto(bytes( "%s" % data,"UTF-8"),addr)
				break
		if j == i:
			bank[i][0] = data['account_name']
			bank[i][1] = data['action']
			bank[i][2] = data['account_id']
			bank[i][3] = port
			bank[i][4] = 0
			i = i+1
			data = {'message' : 'OK'}
			data = json.dumps(data)
			s.sendto(bytes( "%s" % data,"UTF-8"),addr)
	elif(data['action'] == "save"):
		j = -1
		while j < i:
			j = j+1
			if(bank[j][3] == port):
				bank[j][4] = bank[j][4]+data['money']
				data = {'message' : 'OK'}
				data = json.dumps(data)
				s.sendto(bytes( "%s" % data,"UTF-8"),addr)
				break
	elif(data['action'] == "withdraw"):
		j = -1
		while j < i:
			j = j+1
			if(bank[j][3] == port):
				if(bank[j][4] < data['money']):
					data = {'message' : 'invalid transaction'}
					data = json.dumps(data)
					s.sendto(bytes( "%s" % data,"UTF-8"),addr)
				else:
					bank[j][4] = bank[j][4]-data['money']
					data = {'message' : 'OK'}
					data = json.dumps(data)
					s.sendto(bytes( "%s" % data,"UTF-8"),addr)
				break
	elif(data['action'] == "remit"):
		j = -1
		k = -1
		while j < i:
			j = j+1
			if(bank[j][3] == port):
				if(bank[j][4] < data['money'] or bank[j][0] == data['destination_name']):
					data = {'message' : 'invalid transaction'}
					data = json.dumps(data)
					s.sendto(bytes( "%s" % data,"UTF-8"),addr)
					break
				else:
					while k < i:
						k = k+1
						if(bank[k][0] == data['destination_name']):
							bank[j][4] = bank[j][4]-data['money']
							bank[k][4] = bank[k][4]+data['money']
							data = {'message' : 'OK'}
							data = json.dumps(data)
							s.sendto(bytes( "%s" % data,"UTF-8"),addr)
							break
					if k == i:
						data = {'message' : 'invalid transaction'}
						data = json.dumps(data)
						s.sendto(bytes( "%s" % data,"UTF-8"),addr)
						break
	elif(data['action'] == "show"):
		j = -1
		while j < i:
			j = j+1
			if(bank[j][3] == port):
				data = {'message' : bank[j][4]}
				data = json.dumps(data)
				s.sendto(bytes( "%s" % data,"UTF-8"),addr)
				break
		if j == i:
			data = {'message' : 'account not find'}
			data = json.dumps(data)
			s.sendto(bytes( "%s" % data,"UTF-8"),addr)
	elif(data['action'] == "bomb"):
		j = -1
		while j < i:
			j = j+1
			bank[j][4] = 0
		data = {'message' : 'OK'}
		data = json.dumps(data)
		s.sendto(bytes( "%s" % data,"UTF-8"),addr)
	elif(data['action'] == "end"):
		j = -1
		while j < i:
			j = j+1
			bank[j][0] = 0
			bank[j][1] = 0
			bank[j][2] = 0
			bank[j][3] = 0
			bank[j][4] = 0
		i = 0
		data = {'message' : 'end'}
		data = json.dumps(data)
		s.sendto(bytes( "%s" % data,"UTF-8"),addr)