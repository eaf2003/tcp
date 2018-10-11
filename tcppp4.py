import os
import re
import collections
from subprocess import Popen, PIPE, STDOUT

#Set run parameters----
secs ='3' # notice I used timeout linux command to get it simple
iface = 'wlan1'
cmd = ['sudo', 'timeout', secs, 'tcpdump', '-nli', iface]
print cmd

#I decided to look up by using reg.exps
#reg = re.compile(r"IP (?P<IP1>(?:\d{1,3}\.){3}\d{1,3})") # IP1, source grp
reg = re.compile(r"(?P<IP1>(?:\d{1,3}\.){3}\d{1,3})") # IP1, source grp
reg2 = re.compile(r"(?P<length>length) (?P<size>\d{1,10})") #Size group
reg3 = re.compile(r"> (?P<IP2>(?:\d{1,3}\.){3}\d{1,3})") #IPdest 
tmplist = []
tmplist2 = []	
vSize = 0	#then global var to get total size

#Functions----
#Collect IPs
def GetIP1(lineToRead): 
	for match in reg.finditer(lineToRead):
		vIp = match.group("IP1")
		tmplist.append(str(vIp)) #updating array
		#print str(vIp)
		#print "%s: %s" % (match.start(), match.group("IP1"))
		#isGpIP1 = re.search("IP1",lineToRead) 
		
def GetIP2(lineToRead): 
	for match in reg3.finditer(lineToRead):
		vIp2 = match.group("IP2")
		print "CACACACACACA"
		tmplist2.append(str(vIp2)) #updating array

#sum sizes
def GetTotalSize(lineToRead):
	global vSize		
	for match in reg2.finditer(lineToRead):
		#vSize = match.group("size")
		vSize = vSize + int(match.group("size"))

def CounterOld(ArrayToCount):#useless
	vTmpc = [] #init array temp
	counta= 0
	for i in ArrayToCount:
		if vTmpc.__contains__(i):
			counta=counta + 1
		else:
			vTmpc.append(i)
			print i			
	return None



#--EXEC-------
#Start parsing, open std out not sure if the best way, for real time it just worked at first
p = Popen(cmd, stdout=PIPE, stderr=PIPE)

	#read lines	
for line in iter(p.stdout.readline, b''): #parse by line		
	print line #debug
	GetIP1(line)
	GetIP2(line)
	GetTotalSize(line)
		
#	print "in loop" 
#print tmplist
c2 = collections.Counter(tmplist)	#contar ips py using py funcs				
c3 = collections.Counter(tmplist2)	#contar ips py using py funcs				

print  '\n', 'IP Lists:', c2
print '---------------------'
print 'Tx Total:', vSize, ' Bytes'

p.stdout.close()
p.wait()
