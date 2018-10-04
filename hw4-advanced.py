import socket
import json
import sys

ip = "127.0.0.1"
port = 5566
bank = [[0 for x in range(5)] for x in range(10000)] #name action id port money
i = 0
save = [[0 for x in range(3)] for x in range(10000)] #save port money
remit = [[0 for x in range(3)] for x in range(10000)] #remit port money
bomb = [0 for x in range(10000)] #bomb
sa = 1
r = 2
b = 4
a = -1

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((ip, port))

while True:
	data,addr = s.recvfrom(1024)
	data = data.decode("UTF-8")
	data = json.loads(data)
	ip = addr[0]
	port = addr[1]
	sa = sa+1
	r = r+1
	b = b+1
	a = a+1
	if(bomb[a] == 1):
		j = -1
		while j < i:
			j = j+1
			bank[j][4] = 0
	if(remit[a][0] == 1):
		bank[remit[a][1]][4] = bank[remit[a][1]][4]+remit[a][2]
	if(save[a][0] == 1):
		bank[save[a][1]][4] = bank[save[a][1]][4]+save[a][2]
		print(a)
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
				save[sa][0] = 1
				save[sa][1] = j
				save[sa][2] = data['money']
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
							remit[r][0] = 1
							remit[r][1] = k
							remit[r][2] = data['money']
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
		bomb[b] = 1;
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
		j = -1
		while j <= a:
			j = j+1
			save[j][0] = 0
			remit[j][0] = 0
			bomb[j] = 0
		a = -1
		sa = 1
		r = 2
		b = 4
		i = 0
		data = {'message' : 'end'}
		data = json.dumps(data)
		s.sendto(bytes( "%s" % data,"UTF-8"),addr)