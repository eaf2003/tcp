import os
import re
import socket
import collections
from subprocess import Popen, PIPE, STDOUT

#-------INIT-----------------------
#get hostname-->> 'import socket; print socket.gethostname()'
#get ipbyhostname -->import socket;print socket.gethostbyname(socket.gethostname())

#Set run parameters----
secs ='18' # notice I used timeout linux command to get it simple
iface = 'wlan1'
cmd = ['sudo', 'timeout', secs, 'tcpdump', '-nli', iface]
print cmd

#I decided to look up by using reg.exps
#reg = re.compile(r"IP (?P<IP1>(?:\d{1,3}\.){3}\d{1,3})") # IP1, source grp
reg = re.compile(r"(?P<IP1>(?:\d{1,3}\.){3}\d{1,3})") # IPS ALL, source grp
reg2 = re.compile(r"(?P<length>length) (?P<size>\d{1,10})") #Size group
reg3 = re.compile(r"> (?P<IP2>(?:\d{1,3}\.){3}\d{1,3})") #IPdest 
tmplist = []
tmplist2 = []	
vSize = 0	#then global var to get total size
#global gTxRec
gTxRec = 0
gTcSent = 0

#Functions----
#Collect IPs
def GetAllIPs(lineToRead): 
	for match in reg.finditer(lineToRead):
		vIp = match.group("IP1")
		tmplist.append(str(vIp)) #updating array
		#print str(vIp)
		#print "%s: %s" % (match.start(), match.group("IP1"))
		#isGpIP1 = re.search("IP1",lineToRead) 
		
def GetIP2(lineToRead): 
	for match in reg3.finditer(lineToRead):
		vIp2 = match.group("IP2")
		print "CACACACACACA ingresa"
		print 'vIp2xxx:', vIp2
		print 'gmyifip:', gmyIfip
		if set(vIp2.split())==set(gmyIfip.split()): #set convert string to sets to compare splited by ''
			TxRecUpdate(lineToRead)
			print "BYTES RECCC" , gTxRec
		tmplist2.append(str(vIp2)) #updating array

#sum sizes

def TxRecUpdate(lineToRead):
	global gTxRec	
	for match in reg2.finditer(lineToRead):
		#print match.group("size")
		gTxRec = gTxRec + int(match.group("size"))
	#return gTxRec


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


def GetMyIfIp(ifacename): #"get ip by iface name use ifconfig cmd"
	#vCmd = ['sudo','ifconfig',ifacename,'| grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1']
	f = os.popen('sudo ifconfig wlan1 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
	myIP = f.read()
	return myIP
		
def GetMyPubIP(): # test with gmail.com, useless without a pub inet conn, NOT USING it
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com",80))
	return (s.getsockname()[0])
#	print(s.getsockname()[0])
	s.close()


#--EXEC-------
#Start parsing, open std out not sure if the best way, for real time it just worked at first
gmyIfip = GetMyIfIp(iface) #got my if ip, so then i measure incoming tx to it.
p = Popen(cmd, stdout=PIPE, stderr=PIPE)

	#read lines	
for line in iter(p.stdout.readline, b''): #parse by line		
#	print line #debug
	GetAllIPs(line)
	GetIP2(line)
	GetTotalSize(line)
		
#	print "in loop" 
#print tmplist
c2 = collections.Counter(tmplist)	#contar ips py using py funcs				
#c3 = collections.Counter(tmplist2)	#contar ips py using py funcs				
print 'My If IP:' , gmyIfip
print  '\n', 'IP Lists:', c2
print '---------------------'
print 'Tx Rec:', gTxRec, ' Bytes'
print 'Tx Total:', vSize, ' Bytes'


p.stdout.close()
p.wait()
