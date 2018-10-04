import sys
import multiprocessing

map = [[0 for x in range(2000)] for y in range(2000)]

def func(a,b):
	mine = 0
	i = a
	j = b
	if(a==0):
		if(b==0):
			while map[i][j]!="-":
				while map[i][j]!="|":
					if map[i][j]=="*":
						mine = mine+1
					j = j+1
				i = i+1
				j = b
		else:
			while map[i][j]!="-":
				while map[i][j]!="|":
					if map[i][j]=="*":
						mine = mine+1
					j = j-1
				i = i+1
				j = b
	else:
		if(b==0):
			while map[i][j]!="-":
				while map[i][j]!="|":
					if map[i][j]=="*":
						mine = mine+1
					j = j+1
				i = i-1
				j = b	
		else:
			while map[i][j]!="-":
				while map[i][j]!="|":
					if map[i][j]=="*":
						mine = mine+1
					j = j-1
				i = i-1
				j = b
	return mine

def readmap():	
	i = 0
	j = 0
	name = input('Map:')
	file = open(name,'r')
	while True:
		line=file.readline()
		a = 0
		if not line:
			break
		for char in line:
			if char=="#" and j==0:
				a = 1
			if char=="#":
				if a==1:
					map[i][j] = "-"
				else:
					map[i][j] = "|"
			else:
				map[i][j] = char
			j = j+1
		i = i+1
		width = j-1
		j = 0
	length = i
	file.close()
	return length,width

def drawmap(length,width):
	i = 0
	j = 0
	print(" ",end="")
	while j<width :
		print("-",end="")
		j = j+1
	print(" ")
	j = 0
	while i<length :
		print("|",end="")
		while j<width :
			print(map[i][j],end="")
			j = j+1
		print("|")
		i = i+1
		j = 0
	print(" ",end="")
	while j<width :
		print("-",end="")
		j = j+1
	print(" ")
	print("map size: %d*%d" % (width,length))
	
if __name__== "__main__":
	length,width = readmap()
	drawmap(length,width)
	pool = multiprocessing.Pool(processes=4)
	mine = []
	results = []
	results.append(pool.apply_async(func,(0,0)))
	results.append(pool.apply_async(func,(0,width-1)))
	results.append(pool.apply_async(func,(length-1,0)))
	results.append(pool.apply_async(func,(length-1,width-1)))
	pool.close()
	pool.join()
	for result in results:
		mine.append(result.get())
	max = mine.index(max(mine))
	i = 0
	top = []
	for a in mine:
		if mine[max]==mine[i]:
			top.append(i)
		i = i+1
	i = 0
	j = 0
	for a in mine:
		print("Miner#%d: %d " % (i+1,mine[i]),end="")
		if i==top[j]:
			if(len(top)>1):
				print("(draw)")
				j = j+1
			else:
				print("(win)")
		else:
			print()
		i = i+1