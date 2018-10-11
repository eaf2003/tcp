import os
import re
import socket
import collections
from subprocess import Popen, PIPE, STDOUT

#-------INIT-----------------------
#get hostname-->> 'import socket; print socket.gethostname()'
#get ipbyhostname -->import socket;print socket.gethostbyname(socket.gethostname())

#Set run parameters----
secs ='10' # notice I used timeout linux command to get it simple
iface = 'wlan1'
cmd = ['sudo', 'timeout', secs, 'tcpdump', '-nli', iface]
print cmd

#I decided to look up by using reg.exps
reg = re.compile(r"(?P<IPS>(?:\d{1,3}\.){3}\d{1,3})") # IPS ALL, source grp
reg2 = re.compile(r"(?P<length>length) (?P<size>\d{1,10})") #Size group
reg3 = re.compile(r"> (?P<IP2>(?:\d{1,3}\.){3}\d{1,3})") #IPdest 
reg4 = re.compile(r"IP (?P<IP1>(?:\d{1,3}\.){3}\d{1,3})") # IP1, source grp
tmplist = []	#all ips
listIP2 = []	#all dest ips
listIP1 = []	#all source ips
vSize = 0	#accumulated 'length'
gRx = 0  # counter Rx
gTx = 0  # counter Tx

#Functions----
#Collect IPs
def GetAllIPs(lineToRead): 
	for match in reg.finditer(lineToRead):
		vIp = match.group("IPS")
		tmplist.append(str(vIp)) #updating array
		#print str(vIp)
		#print "%s: %s" % (match.start(), match.group("IP1"))
		#isGpIP1 = re.search("IP1",lineToRead) 
		
def GetIP1(lineToRead): 
	for match in reg4.finditer(lineToRead):
		vIp1 = match.group("IP1")
		listIP1.append(str(vIp1)) #updating array
		if set(vIp1.split())==set(gmyIfip.split()): #set convert string to sets to compare splited by ''
			TxUpdate(lineToRead)
		listIP1.append(str(vIp1)) #updating array all ingoing ips
				
def GetIP2(lineToRead): 
	for match in reg3.finditer(lineToRead):
		vIp2 = match.group("IP2")
		print "CACACACACACA ingresa"
		print 'vIp2xxx:', vIp2
		print 'gmyifip:', gmyIfip
		if set(vIp2.split())==set(gmyIfip.split()): #set convert string to sets to compare splited by ''
			RxUpdate(lineToRead)
		listIP2.append(str(vIp2)) #updating array all ingoing ips

#sum sizes

def RxUpdate(lineToRead):
	global gRx	
	#print gRx
	for match in reg2.finditer(lineToRead):
		#print match.group("size")
		gRx = gRx + int(match.group("size"))
		print "BYTES RECCC" , gRx
	return gRx

def TxUpdate(lineToRead):
	global gTx	
	for match in reg2.finditer(lineToRead):
		gTx = gTx + int(match.group("size"))
		print "BYTES SENT" , gTx
	return gTx


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
	#f = Popen(vCmd) #popen is deprecated py216 change to Popen
	myIP = f.read()
	return myIP
		
def GetMyPubIP(): # test with gmail.com, useless without a pub inet conn, NOT USING it
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com",80))
	return (s.getsockname()[0])
#	print(s.getsockname()[0])
	s.close()

def ListCounter(listado):
	for i in listado:
		return None


#--EXEC-------
#Start parsing, open std out not sure if the best way, for real time it just worked at first
gmyIfip = GetMyIfIp(iface) #got my if ip, so then i measure incoming tx to it.
p = Popen(cmd, stdout=PIPE, stderr=PIPE)

	#read lines	
for line in iter(p.stdout.readline, b''): #parse by line		
#	print line #debug
	GetAllIPs(line)
	GetIP2(line)
	GetIP1(line)
	GetTotalSize(line)
		
#	print "in loop" 
#print tmplist
c2 = collections.Counter(tmplist)	#count all ips				
c3 = collections.Counter(listIP2)	#contar ip2 dest ips py using py funcs				
c4 = collections.Counter(listIP1)   #coult source

print  '\n', 'ALL IPs:', c2
print  '\n', 'IN IPs Lists:', c3
print  '\n', 'OUT IPs Lists:', c4
print 'My Interface IP:' , gmyIfip
print '---------------------'
print 'Total IPs:',len(set(tmplist)) #total items in list
print 'Total Src IPs:',len(set(listIP1)) #total items in list
print 'Total Dest IPs:',len(set(listIP2)) #total items in list
print 'Rx:', gRx, ' Bytes'
print 'Tx:', gTx, ' Bytes'
print 'RxTx Raw Total:', vSize, ' Bytes'


p.stdout.close()
p.wait()
