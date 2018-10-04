import socket
import sys

host = 0
S1 = 0
up = 60000
down = 3000
msg = ""

host = input("host:")
S1 = input("port:")
S1 = int(S1)
socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
socket.connect((host,S1))


while True:
    num = int((up+down)/2)
    guess = '{"guess":' + str(num) + '}'
    print(guess)
    socket.send(bytes( "%s" % guess,"UTF-8"))
    msg = socket.recv(1024)
    msg = str(msg)
    print(msg[2:-1])
    msg = msg.split("\"")[3]
    if msg == "larger":
        down = num
    elif msg == "smaller":
        up = num
    elif msg == "bingo!":
        S2 = num
        break

socket.connect((host,S2))

studentid = '{"student_id": "0116322"}'
print(studentid)
socket.send(bytes( "%s" % studentid,"UTF-8"))
msg = socket.recv(1024)
msg = str(msg)
print(msg[2:-1])

socket.close()
