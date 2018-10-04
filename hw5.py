import socket
import json
import sys
import re
import time
from _thread import *

ip = "127.0.0.1"
port = 5566
no = -1
name = [0 for x in range(40)]
mail = [[0 for x in range(40)] for x in range(40)]
read = [[0 for x in range(40)] for x in range(40)]
title = [[0 for x in range(40)] for x in range(40)]
sender = [[0 for x in range(40)] for x in range(40)]
num = [0 for x in range(40)]
to = ""
titlez = ""
content = ""

z = 0
y = 0
while y < 40:
	while z < 40:
		mail[y][z] = 0
		read[y][z] = 2
		title[y][z] = 0
		sender[y][z] = 0
		z = z+1
	name[y] = 0
	num[y] = 0
	y = y+1
		
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((ip, port))
s.listen(1)

def clientthread(conn,no):
	while True:
		space = 0
		d = 0
		data = conn.recv(1024)
		data = data.decode("UTF-8")
		data = data.strip()
		p = re.compile('\s+')
		data = p.split(data)
		print(data)
		if data[d] == "exit":
			d = d+1
			if len(data)>1:
				data = "option error\n"
				data = data.encode("UTF-8")
				conn.send(data)
			else:
				i = 0
				while i < 40:
					mail[no][i] = 0
					read[no][i] = 0
					title[no][i] = 0
					sender[no][i] = 0
					i = i+1
				name[no] = 0
				num[no] = 0
				data = "exit\n"
				data = data.encode("UTF-8")
				conn.send(data)
				conn.close()
				break
		elif data[d] == "init":
			d = d+1
			if data[d] == "-u":
				d = d+1
				tmp = ""
				if data[d][0] == "\"":
					space = 1
					while data[d][-1] != "\"":
						tmp = tmp+data[d]+" "
						d = d+1
					tmp = tmp+data[d]
					tmp = tmp[1:-1]
				else:
					tmp = data[d]
				if space == 1:
					if re.search("[^a-zA-Z0-9_\-\s]",tmp):
						data = "args error\n"
						data = data.encode("UTF-8")
						conn.send(data)
					else:
						if tmp in name:
							data = "This account has been registered\n"
							data = data.encode("UTF-8")
							conn.send(data)
						else:
							name[no] = tmp
							data = tmp + "@nctu.edu.tw\n"
							data = data.encode("UTF-8")
							conn.send(data)
				else:
					if re.search("[^a-zA-Z0-9_\-]",tmp):
						data = "args error\n"
						data = data.encode("UTF-8")
						conn.send(data)
					else:
						if tmp in name:
							data = "This account has been registered\n"
							data = data.encode("UTF-8")
							conn.send(data)
						else:
							name[no] = tmp
							data = tmp + "@nctu.edu.tw\n"
							data = data.encode("UTF-8")
							conn.send(data)
				space = 0
			else:
				data = "option error\n"
				data = data.encode("UTF-8")
				conn.send(data)
		elif data[d] == "ls":
			d = d+1
			if data[d] == "-u":
				d = d+1
				if len(data)>2:
					data = "args error\n"
					data = data.encode("UTF-8")
					conn.send(data)
				elif len(name) == 0:
					data = "no accounts\n"
					data = data.encode("UTF-8")
					conn.send(data)
				else:
					data = ""
					i = 0
					while i < 40:
						if name[i] != 0:
							data = data+str(name[i])+"@nctu.edu.tw\n"
						i = i+1
					data = data.encode("UTF-8")
					conn.send(data)
			elif data[d] == "-l":
				d = d+1
				if len(data)>2:
					data = "args error\n"
					data = data.encode("UTF-8")
					conn.send(data)
				elif num[no] == 0:
					data = "no mail\n"
					data = data.encode("UTF-8")
					conn.send(data)
				else:
					i = 0
					j = 0
					data = ""
					while j < num[no]:
						if read[no][j] == 0:
							i = i+1
							data = data+str(i)+"."+str(title[no][j])+"(new)\n"
						elif read[no][j] == 1:
							i = i+1
							data = data+str(i)+"."+str(title[no][j])+"\n"
						j = j+1
					data = data.encode("UTF-8")
					conn.send(data)
			elif data[d] == "-a":
				d = d+1
				if len(data)>2:
					data = "args error\n"
					data = data.encode("UTF-8")
					conn.send(data)
				elif name[no] == 0:
					data = "init first\n"
					data = data.encode("UTF-8")
					conn.send(data)
				else:
					data = "Account:"+str(name[no])+"\nMail address:"+str(name[no])+"@nctu.edu.tw\nNumber of mails:"+str(num[no])+"\n"
					data = data.encode("UTF-8")
					conn.send(data)
			else:
				data = "option error\n"
				data = data.encode("UTF-8")
				conn.send(data)
		elif data[d] == "rm":
			d = d+1
			if data[d] == "-d":
				d = d+1
				if data[d][0] == "\"":
					data = "args error\n"
					data = data.encode("UTF-8")
					conn.send(data)
				elif read[no][int(data[d])-1] == 2:
					data = "args error\n"
					data = data.encode("UTF-8")
					conn.send(data)
				else:
					read[no][int(data[d])-1] = 2
					mail[no][int(data[d])-1] = 0
					num[no] = num[no]-1
					data = "done\n"
					data = data.encode("UTF-8")
					conn.send(data)
			elif data[d] == "-D":
				d = d+1
				if len(data)>2:
					data = "args error\n"
					data = data.encode("UTF-8")
					conn.send(data)
				else:
					i = 0
					while i < 40:
						read[no][i] = 2
						mail[no][i] = 2
						i = i+1
					num[no] = 0
					data = "done\n"
					data = data.encode("UTF-8")
					conn.send(data)
			else:
				data = "option error\n"
				data = data.encode("UTF-8")
				conn.send(data)
		elif data[d] == "rd":
			d = d+1
			if data[d] == "-r":
				d = d+1
				if data[d][0] == "\"":
					data = "args error\n"
					data = data.encode("UTF-8")
					conn.send(data)
				elif read[no][int(data[d])-1] == 2:
					data = "args error\n"
					data = data.encode("UTF-8")
					conn.send(data)
				else:
					read[no][int(data[d])-1] = 1
					data = mail[no][int(data[d])-1]
					data = data.encode("UTF-8")
					conn.send(data)
			else:
				data = "option error\n"
				data = data.encode("UTF-8")
				conn.send(data)
		elif data[d] == "wt":
			i = 0
			mesg = "From:" + str(name[no]) + "@nctu.edu.tw\n"
			t = time.time()
			t = "Date:"+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))+"\n"
			while d < len(data)-1:
				d = d+1
				if data[d] == "-d":
					d = d+1
					tmp = ""
					if data[d][0] == "\"":
						space = 1
						while data[d][-1] != "\"":
							tmp = tmp+data[d]+" "
							d = d+1
						tmp = tmp+data[d]
						tmp = tmp[1:-1]
					else:
						tmp = data[d]
					tmp = tmp.split("@")
					if space == 1:
						if re.search("[^a-zA-Z0-9_\-\:\.\@\s]",tmp[0]):
							data = "args error\n"
							data = data.encode("UTF-8")
							conn.send(data)
							break
						else:
							while i < len(name):
								if name[i] == tmp[0]:
									break
								i = i+1
							if i == len(name):
								data = "args error\n"
								data = data.encode("UTF-8")
								conn.send(data)
								break
							else:
								to = "To:" + str(tmp[0]) + "@nctu.edu.tw\n"
					else:
						if re.search("[^a-zA-Z0-9_\-\:\.\@]",tmp[0]):
							data = "args error\n"
							data = data.encode("UTF-8")
							conn.send(data)
							break
						else:
							while i < len(name):
								if name[i] == tmp[0]:
									break
								i = i+1
							if i == len(name):
								data = "args error\n"
								data = data.encode("UTF-8")
								conn.send(data)
								break
							else:
								to = "To:" + str(tmp[0]) + "@nctu.edu.tw\n"
					space = 0
				elif data[d] == "-t":
					d = d+1
					tmp = ""
					if data[d][0] == "\"":
						space = 1
						while data[d][-1] != "\"":
							tmp = tmp+data[d]+" "
							d = d+1
						tmp = tmp+data[d]
						tmp = tmp[1:-1]
					else:
						tmp = data[d]
					if space == 1:
						if re.search("[^a-zA-Z0-9_\-\:\.\@\s]",tmp):
							data = "args error\n"
							data = data.encode("UTF-8")
							conn.send(data)
							break
						else:
							titlez = tmp
					else:
						if re.search("[^a-zA-Z0-9_\-\:\.\@]",tmp):
							data = "args error\n"
							data = data.encode("UTF-8")
							conn.send(data)
							break
						else:
							titlez = tmp
					space = 0
				elif data[d] == "-c":
					d = d+1
					tmp = ""
					if data[d][0] == "\"":
						space = 1
						while data[d][-1] != "\"":
							tmp = tmp+data[d]+" "
							d = d+1
						tmp = tmp+data[d]
						tmp = tmp[1:-1]
					else:
						tmp = data[d]
					if space == 1:
						if re.search("[^a-zA-Z0-9_\-\:.\@\s]",tmp):
							data = "args error\n"
							data = data.encode("UTF-8")
							conn.send(data)
							break
						else:
							content = "Content:" + str(tmp) + "\n"
					else:
						if re.search("[^a-zA-Z0-9_\-\:.\@]",tmp):
							data = "args error\n"
							data = data.encode("UTF-8")
							conn.send(data)
							break
						else:
							content = "Content:" + str(tmp) + "\n"
					space = 0
				else:
					data = "option error\n"
					data = data.encode("UTF-8")
					conn.send(data)	
					break
			if d == len(data)-1:
				title[i][num[i]] = titlez
				mail[i][num[i]] = mesg + to + t + "Title:" + titlez + "\n" + content
				read[i][num[i]] = 0
				sender[i][num[i]] = name[no]
				num[i] = num[i]+1
				data = "done\n"
				data = data.encode("UTF-8")
				conn.send(data)
		elif data[d] == "re":
			r = 0
			i = 0
			t = time.time()
			t = "Date:"+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))+"\n"
			while d < len(data)-1:
				d = d+1
				space = 0
				if data[d] == "-n":
					d = d+1
					if data[d][0] == "\"":
						data = "args error\n"
						data = data.encode("UTF-8")
						conn.send(data)
					else:
						r = int(data[d])
						while i < 40:
							if name[i] == sender[no][r-1]:
								break
							i = i+1
				elif data[d] == "-c":
					d = d+1
					tmp = ""
					if data[d][0] == "\"":
						space = 1
						while data[d][-1] != "\"":
							tmp = tmp+data[d]+" "
							d = d+1
						tmp = tmp+data[d]
						tmp = tmp[1:-1]
					else:
						tmp = data[d]
					if space == 1:
						if re.search("[^a-zA-Z0-9_\-\:.\@\s]",tmp):
							data = "args error\n"
							data = data.encode("UTF-8")
							conn.send(data)
							break
						else:
							content = "Content:" + str(tmp) + "\n----\n"
					else:
						if re.search("[^a-zA-Z0-9_\-\:.\@]",tmp):
							data = "args error\n"
							data = data.encode("UTF-8")
							conn.send(data)
							break
						else:
							content = "Content:" + str(tmp) + "\n----\n"
					space = 0
				else:
					data = "option error\n"
					data = data.encode("UTF-8")
					conn.send(data)	
					break
			if d == len(data)-1:
				tmp = str(title[no][r-1]).split(":")
				if len(tmp) == 1:
					titlez = "re:" + str(tmp[0])
				else:
					j = 1
					titlez = "re:"
					while j < len(tmp):
						titlez = titlez + str(tmp[j])
						j = j+1
				content = "From:" + str(name[no]) + "@nctu.edu.tw\nTo:" + str(sender[no][r-1]) + "@nctu.edu.tw\n" + t + "Title:" + titlez + "\n" + content
				sender[i][num[i]] = name[no]
				mail[i][num[i]] = content + str(mail[no][r-1])
				read[i][num[i]] = 0
				title[i][num[i]] = titlez
				num[i] = num[i]+1
				data = "done\n"
				data = data.encode("UTF-8")
				conn.send(data)
		elif data[d] == "fwd":
			fwd = 0
			i = 0
			t = time.time()
			t = "Date:"+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))+"\n"
			while d < len(data)-1:
				d = d+1
				space = 0
				if data[d] == "-n":
					d = d+1
					if data[d][0] == "\"":
						data = "args error\n"
						data = data.encode("UTF-8")
						conn.send(data)
					else:
						fwd = int(data[d])
				elif data[d] == "-c":
					d = d+1
					tmp = ""
					if data[d][0] == "\"":
						space = 1
						while data[d][-1] != "\"":
							tmp = tmp+data[d]+" "
							d = d+1
						tmp = tmp+data[d]
						tmp = tmp[1:-1]
					else:
						tmp = data[d]
					if space == 1:
						if re.search("[^a-zA-Z0-9_\-\:.\@\s]",tmp):
							data = "args error\n"
							data = data.encode("UTF-8")
							conn.send(data)
							break
						else:
							content = "Content:" + str(tmp) + "\n----\n"
					else:
						if re.search("[^a-zA-Z0-9_\-\:.\@]",tmp):
							data = "args error\n"
							data = data.encode("UTF-8")
							conn.send(data)
							break
						else:
							content = "Content:" + str(tmp) + "\n----\n"
					space = 0
				elif data[d] == "-d":
					d = d+1
					tmp = ""
					if data[d][0] == "\"":
						space = 1
						while data[d][-1] != "\"":
							tmp = tmp+data[d]+" "
							d = d+1
						tmp = tmp+data[d]
						tmp = tmp[1:-1]
					else:
						tmp = data[d]
					tmp = tmp.split("@")
					if space == 1:
						if re.search("[^a-zA-Z0-9_\-\:\.\@\s]",tmp[0]):
							data = "args error\n"
							data = data.encode("UTF-8")
							conn.send(data)
							break
						else:
							while i < len(name):
								if name[i] == tmp[0]:
									break
								i = i+1
							if i == len(name):
								data = "args error\n"
								data = data.encode("UTF-8")
								conn.send(data)
								break
							else:
								to = "To:" + str(tmp[0]) + "@nctu.edu.tw\n"
					else:
						if re.search("[^a-zA-Z0-9_\-\:\.\@]",tmp[0]):
							data = "args error\n"
							data = data.encode("UTF-8")
							conn.send(data)
							break
						else:
							while i < len(name):
								if name[i] == tmp[0]:
									break
								i = i+1
							if i == len(name):
								data = "args error\n"
								data = data.encode("UTF-8")
								conn.send(data)
								break
							else:
								to = "To:" + str(tmp[0]) + "@nctu.edu.tw\n"
					space = 0
				else:
					data = "option error\n"
					data = data.encode("UTF-8")
					conn.send(data)	
					break
			if d == len(data)-1:
				tmp = str(title[no][fwd-1]).split(":")
				if len(tmp) == 1:
					titlez = "fwd:" + str(tmp[0])
				else:
					j = 1
					titlez = "fwd:"
					while j < len(tmp):
						titlez = titlez + str(tmp[j])
						j = j+1
				content = "From:" + str(name[no]) + "@nctu.edu.tw\n" + to + t + "Title:" + titlez + "\n" + content
				sender[i][num[i]] = name[no]
				mail[i][num[i]] = content + str(mail[no][fwd-1])
				read[i][num[i]] = 0
				title[i][num[i]] = titlez
				num[i] = num[i]+1
				data = "done\n"
				data = data.encode("UTF-8")
				conn.send(data)
		else:
			data = "command error\n"
			data = data.encode("UTF-8")
			conn.send(data)
while True:
	conn,addr = s.accept()
	no = no + 1
	start_new_thread(clientthread,(conn,no))
	
s.close()