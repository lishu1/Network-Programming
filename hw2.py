import socket
import json
import sys

ip = 0
port = 0
action = ""
connect = 0
new = 0
data = ""
success = 0

ip = input("server_ip:")
port = input("server_port:")
port = int(port)

print ("Welcome to Game 2048!")
print ("enter \'help\' to get mor information")

while True:
	z = 0
	if new == 0:
		action = input(">")
	elif new == 1:
		action = input("move>")
	if action == "help":
		print ("Enter keyboard")
		print ("\'connect\' - connect to game server")
		print ("\'disconnect\' - disconnect from game server")
		print ("\'new\' - new a game round")
		print ("\'end\' - close the game")
		print ("\'w\' - move bricks up")
		print ("\'s\' - move bricks down")
		print ("\'a\' - move bricks left")
		print ("\'d\' - move bricks right")
		print ("\'u\' - undo the last move")
	elif action == "connect":
		if connect == 0:
			connect = 1
			s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			s.connect((ip,port))
			print ("connect to game server")
		elif connect == 1:
			print ("Have already connectted to server")
	elif action == "disconnect":
		if connect == 0:
			print ("Please connect to server first")
		elif connect == 1:
			connect = 0
			new = 0
			s.close()
			print ("disconnect from game server")
	elif action == "new":
		if connect == 0:
			print ("Please connect to server first")
		elif connect == 1:
			if new == 0:
				new = 1
				data = {'action' : 'New'}
				data = json.dumps(data)
				s.send(bytes( "%s" % data,"UTF-8"))
				data = s.recv(1024).decode("UTF-8")
				data = json.loads(data)
				data = data['message'].split(',')
				print ("---------------------")
				print ("|%4s|%4s|%4s|%4s|" % (data[0],data[1],data[2],data[3]))
				print ("---------------------")
				print ("|%4s|%4s|%4s|%4s|" % (data[4],data[5],data[6],data[7]))
				print ("---------------------")
				print ("|%4s|%4s|%4s|%4s|" % (data[8],data[9],data[10],data[11]))
				print ("---------------------")
				print ("|%4s|%4s|%4s|%4s|" % (data[12],data[13],data[14],data[15]))
				print ("---------------------")
			elif new == 1:
				print ("Have already in a game round")
	elif action == "end":
		if connect == 0:
			print ("Please connect to server first")
		elif connect == 1:
			if new == 0:
				print ("No game to close")
			elif new == 1:
				new = 0
				data = {'action' : 'End'}
				data = json.dumps(data)
				s.send(bytes( "%s" % data,"UTF-8"))
				data = s.recv(1024).decode("UTF-8")
				data = json.loads(data)
				print (data['message'])
	elif action == "w":
		if connect == 0:
			print ("Please connect to server first")
		elif connect == 1:
			if new == 0:
				print ("Please new a game round first")
			elif new == 1:
				data = {'action' : 'moveUp'}
				data = json.dumps(data)
				s.send(bytes( "%s" % data,"UTF-8"))
				data = s.recv(1024).decode("UTF-8")
				data = json.loads(data)
				data = data['message'].split(',')
				if len(data) == 1:
					print ("not change")
				else:
					print ("---------------------")
					print ("|%4s|%4s|%4s|%4s|" % (data[0],data[1],data[2],data[3]))
					print ("---------------------")
					print ("|%4s|%4s|%4s|%4s|" % (data[4],data[5],data[6],data[7]))
					print ("---------------------")
					print ("|%4s|%4s|%4s|%4s|" % (data[8],data[9],data[10],data[11]))
					print ("---------------------")
					print ("|%4s|%4s|%4s|%4s|" % (data[12],data[13],data[14],data[15]))
					print ("---------------------")
					while z < 16:
						if data[z] == "2048":
							print ("Congrats! You win the game!")
							new = 0
							break
						z = z+1
	elif action == "s":
		if connect == 0:
			print ("Please connect to server first")
		elif connect == 1:
			if new == 0:
				print ("Please new a game round first")
			elif new == 1:
				data = {'action' : 'moveDown'}
				data = json.dumps(data)
				s.send(bytes( "%s" % data,"UTF-8"))
				data = s.recv(1024).decode("UTF-8")
				data = json.loads(data)
				data = data['message'].split(',')
				if len(data) == 1:
					print ("not change")
				else:
					print ("---------------------")
					print ("|%4s|%4s|%4s|%4s|" % (data[0],data[1],data[2],data[3]))
					print ("---------------------")
					print ("|%4s|%4s|%4s|%4s|" % (data[4],data[5],data[6],data[7]))
					print ("---------------------")
					print ("|%4s|%4s|%4s|%4s|" % (data[8],data[9],data[10],data[11]))
					print ("---------------------")
					print ("|%4s|%4s|%4s|%4s|" % (data[12],data[13],data[14],data[15]))
					print ("---------------------")
					while z < 16:
						if data[z] == "2048":
							print ("Congrats! You win the game!")
							new = 0
							break
						z = z+1
	elif action == "a":
		if connect == 0:
			print ("Please connect to server first")
		elif connect == 1:
			if new == 0:
				print ("Please new a game round first")
			elif new == 1:
				data = {'action' : 'moveLeft'}
				data = json.dumps(data)
				s.send(bytes( "%s" % data,"UTF-8"))
				data = s.recv(1024).decode("UTF-8")
				data = json.loads(data)
				data = data['message'].split(',')
				if len(data) == 1:
					print ("not change")
				else:
					print ("---------------------")
					print ("|%4s|%4s|%4s|%4s|" % (data[0],data[1],data[2],data[3]))
					print ("---------------------")
					print ("|%4s|%4s|%4s|%4s|" % (data[4],data[5],data[6],data[7]))
					print ("---------------------")
					print ("|%4s|%4s|%4s|%4s|" % (data[8],data[9],data[10],data[11]))
					print ("---------------------")
					print ("|%4s|%4s|%4s|%4s|" % (data[12],data[13],data[14],data[15]))
					print ("---------------------")
					while z < 16:
						if data[z] == "2048":
							print ("Congrats! You win the game!")
							new = 0
							break
						z = z+1
	elif action == "d":
		if connect == 0:
			print ("Please connect to server first")
		elif connect == 1:
			if new == 0:
				print ("Please new a game round first")
			elif new == 1:
				data = {'action' : 'moveRight'}
				data = json.dumps(data)
				s.send(bytes( "%s" % data,"UTF-8"))
				data = s.recv(1024).decode("UTF-8")
				data = json.loads(data)
				data = data['message'].split(',')
				if len(data) == 1:
					print ("not change")
				else:
					print ("---------------------")
					print ("|%4s|%4s|%4s|%4s|" % (data[0],data[1],data[2],data[3]))
					print ("---------------------")
					print ("|%4s|%4s|%4s|%4s|" % (data[4],data[5],data[6],data[7]))
					print ("---------------------")
					print ("|%4s|%4s|%4s|%4s|" % (data[8],data[9],data[10],data[11]))
					print ("---------------------")
					print ("|%4s|%4s|%4s|%4s|" % (data[12],data[13],data[14],data[15]))
					print ("---------------------")
					while z < 16:
						if data[z] == "2048":
							print ("Congrats! You win the game!")
							new = 0
							break
						z = z+1
	elif action == "u":
		if connect == 0:
			print ("Please connect to server first")
		elif connect == 1:
			if new == 0:
				print ("Please new a game round first")
			elif new == 1:
				data = {'action' : 'unDo'}
				data = json.dumps(data)
				s.send(bytes( "%s" % data,"UTF-8"))
				data = s.recv(1024).decode("UTF-8")
				data = json.loads(data)
				data = data['message'].split(',')
				print ("---------------------")
				print ("|%4s|%4s|%4s|%4s|" % (data[0],data[1],data[2],data[3]))
				print ("---------------------")
				print ("|%4s|%4s|%4s|%4s|" % (data[4],data[5],data[6],data[7]))
				print ("---------------------")
				print ("|%4s|%4s|%4s|%4s|" % (data[8],data[9],data[10],data[11]))
				print ("---------------------")
				print ("|%4s|%4s|%4s|%4s|" % (data[12],data[13],data[14],data[15]))
				print ("---------------------")
	elif action == "whosyourdaddy":
		if connect == 0:
			print ("Please connect to server first")
		elif connect == 1:
			if new == 0:
				print ("Please new a game round first")
			elif new == 1:
				data = {'action' : 'whosyourdaddy'}
				data = json.dumps(data)
				s.send(bytes( "%s" % data,"UTF-8"))
				data = s.recv(1024).decode("UTF-8")
				data = json.loads(data)
				data = data['message'].split(',')
				if len(data) == 1:
					print ("not change")
				else:
					print ("---------------------")
					print ("|%4s|%4s|%4s|%4s|" % (data[0],data[1],data[2],data[3]))
					print ("---------------------")
					print ("|%4s|%4s|%4s|%4s|" % (data[4],data[5],data[6],data[7]))
					print ("---------------------")
					print ("|%4s|%4s|%4s|%4s|" % (data[8],data[9],data[10],data[11]))
					print ("---------------------")
					print ("|%4s|%4s|%4s|%4s|" % (data[12],data[13],data[14],data[15]))
					print ("---------------------")
					while z < 16:
						if data[z] == "2048":
							print ("Congrats! You win the game!")
							new = 0
							break
						z = z+1