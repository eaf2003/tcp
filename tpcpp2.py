import os
import re
import collections
from subprocess import Popen, PIPE, STDOUT

#cmd = ['df', '-h', '/mnt']

secs='10'
cmd = ['sudo', 'timeout', secs, 'tcpdump', '-nli', 'wlan1']
#reg = re.compile(r"IP (?P<IP1>(?:\d{1,3}\.){3}\d{1,3})\.(?P<Port1>\d+) > (?P<IP2>(?:\d{1,3}\.){3}\d{1,3})\.(?P<Port2>\d+): (?:tc|ud)p (?P<size>\d+)")
reg = re.compile(r"IP (?P<IP1>(?:\d{1,3}\.){3}\d{1,3})") # IP1source
#reg2 =

print cmd
#in from console
p = Popen(cmd, stdout=PIPE, stderr=PIPE)
#c = collections.Counter()
tmplist = []	
print 'Initial :', c

for line in iter(p.stdout.readline, b''):

	#print line
	def GetIP1(lineToRead): #IPsource
		for match in reg.finditer(lineToRead):
			vIp = match.group("IP1")
#			c.update(str(vIp))
			tmplist.append(str(vIp))
			print str(vIp)
			print 'Sequence:', c
			print "%s: %s" % (match.start(), match.group("IP1"))
		isGpIP1 = re.search("IP1",lineToRead) 
		#leo que exista el grupo de busqueda sino sera error
#		if isGpIP1 is None:
#			print isGpIP1
#			return None
#		print isGpIP1
#		m = regA.match(lineToRead)
#		print(m.group("IP1"))	
		#---


		#c.update({'a':1, 'd':5})
		#print 'Dict    :', c
		#---

	GetIP1(line)

	#def GetIP2(liteToRead): #IPDest
		#igual que arriba para leer el dest
	
	print "in loop" 
print tmplist
c2 = collections.Counter(tmplist)					
print c2
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
