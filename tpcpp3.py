import os
import re
import collections
from subprocess import Popen, PIPE, STDOUT

#cmd = ['df', '-h', '/mnt']

secs='5'
cmd = ['sudo', 'timeout', secs, 'tcpdump', '-nli', 'wlan1']
#reg = re.compile(r"IP (?P<IP1>(?:\d{1,3}\.){3}\d{1,3})\.(?P<Port1>\d+) > (?P<IP2>(?:\d{1,3}\.){3}\d{1,3})\.(?P<Port2>\d+): (?:tc|ud)p (?P<size>\d+)")
reg = re.compile(r"IP (?P<IP1>(?:\d{1,3}\.){3}\d{1,3})") # IP1source
reg2 = re.compile(r"(?P<length>length) (?P<size>\d{1,10})")

print cmd
#in from console
p = Popen(cmd, stdout=PIPE, stderr=PIPE)
#c = collections.Counter()
tmplist = []	
tmplist2 = []
vSize = 0	

#print 'Initial :', c

for line in iter(p.stdout.readline, b''): #parse by line

#	print line #debug
	def GetIP1(lineToRead): #IPsource
		for match in reg.finditer(lineToRead):
			vIp = match.group("IP1")
##			c.update(str(vIp))
			tmplist.append(str(vIp)) #updating array
#			print str(vIp)
##			print 'Sequence:', c
#			print "%s: %s" % (match.start(), match.group("IP1"))
		isGpIP1 = re.search("IP1",lineToRead) 
		#leo que exista el grupo de busqueda sino sera error
##		if isGpIP1 is None:
##			print isGpIP1
##			return None
##		print isGpIP1
##		m = regA.match(lineToRead)
##		print(m.group("IP1"))	
		#---
#		#c.update({'a':1, 'd':5})
		#print 'Dict    :', c
		#---
	def GetTotalSize(lineToRead): #
		global vSize		
		for match in reg2.finditer(lineToRead):
			#vSize = match.group("size")
			vSize = vSize + int(match.group("size"))
			#print vSize
			#tmplist2.append(str(vSize)) #updating array
#		isGpIP1 = re.search("size",lineToRead) 

	GetIP1(line)
	GetTotalSize(line)
	

	#def GetIP2(liteToRead): #IPDest
		#igual que arriba para leer el dest
	
#	print "in loop" 
#print tmplist
c2 = collections.Counter(tmplist)	#uso una func de python para contar				
print  '\n', 'IP Lists:', c2
#c3 = collections.Counter(tmplist2)	#uso una func de python para contar				
print '---------------------'
print 'Tx Total:', vSize, ' Bytes'


def CounterOld(ArrayToCount):
	vTmpc = [] #init array temp
	counta= 0
	for i in ArrayToCount:
		if vTmpc.__contains__(i):
			counta=counta + 1
		else:
			vTmpc.append(i)
			print i		
	
	return None
#CounterOld(tmplist)	

	#isGp = re.search(line,content)
    #m = reg.match(line)
    #print(m.group("IP1"))
    #print(m.group("Port1"))
    #print(m.group("IP2"))
    #print(m.group("Port2"))
    #print(m.group("size"))
	
	
	#return None
	
p.stdout.close()
p.wait()

#print "OUTPUT"
#print output
