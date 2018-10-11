import os
import re
from subprocess import Popen, PIPE, STDOUT

#cmd = ['df', '-h', '/mnt']

secs='10'
cmd = ['sudo', 'timeout', secs, 'tcpdump', '-nli', 'wlan1']
reg = re.compile(r"IP (?P<IP1>(?:\d{1,3}\.){3}\d{1,3})\.(?P<Port1>\d+) > (?P<IP2>(?:\d{1,3}\.){3}\d{1,3})\.(?P<Port2>\d+): (?:tc|ud)p (?P<size>\d+)")
#reg = re.compile(r"IP (?P<IP1>(?:\d{1,3}\.){3}\d{1,3})")

print cmd
#in from console
p = Popen(cmd, stdout=PIPE, stderr=PIPE)
for line in iter(p.stdout.readline, b''):
	print "in loop" 
	print line
    #m = reg.match(line)
    #print(m.group("IP1"))
    #print(m.group("Port1"))
    #print(m.group("IP2"))
    #print(m.group("Port2"))
    #print(m.group("size"))
	
p.stdout.close()
p.wait()

#print "OUTPUT"
#print output
