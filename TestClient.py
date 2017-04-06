import socket  
import sys
from collections import namedtuple
import pickle
import threading
import inspect
import time
import signal

sequence_number = 00000000000000000000000000000000
checksum = 0000000000000000
data_packet = 0101010101010101
SERVER_IP = "127.0.0.1"

#Start Socket connection to server



#READ IN FROM COMMAND LINE --> Simple_ftp_server server-host-nae server-port# file-name N MSS
server_host_name = sys.argv[1]
int(server_port) = sys.argv[2]
file_name = sys.argv[3]
window_size = sys.argv[4]
MSS = sys.argv[5]


#ESTABLISHED CONNECTION BASED OFF OF PORT SENT
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((SERVER_IP, server_port)
#c.send("HELLO FROM THE CLIENT")
#hello = c.recv(MSS)
#print hello 

rdt_send(file_name, MSS, sequence_number, checksum, data_packet)

#PROVIDES INFO FROM A FILE ON A BYTE BASIS
def rdt_send(file, size, seq, check, dta):
	
	access = open( file , "r")
	#while the file has info, lets send them
	while True:
		#read in HEADER + (MSS - 8 byte Header amount of info)
		file = str(seq) + str(check) + str(dta) + str(access.read(size-8))
		#if no info break 
		if file == "":
			access.close()
			#c.close()
			break
		#if info, we want to send at MSS data
		else:
			#Need to wait until next ACK and window to advance to send next
			#if window == 1 
			c.sendall(file)		
