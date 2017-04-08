#SERVER WILL RECEIVE INFO AND ACK
import socket 
import pickle
import sys
from collections import namedtuple
import random
import time
import datetime

global zeros
zeros = 0000000000000000
global ack_id
ack_id = 1010101010101010


MSS = 1024 # Max Segment Size (needs to be re-addressed)

IP = "127.0.0.1"
PORT = 7735

#LISTEN ON PORT 7735
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((IP, PORT))

while 1:
	# s.listen(1)
	packet, addr = s.recvfrom(MSS)
	entire_data = pickle.loads(packet)
	print entire_data
	#check checksum is correct, if not, do nothing
	#check to see if in sequence, if not do nothing
	#elsif checksum and in sequence then send ACK
	#then create file and add passed info into it
	to_send=[]
	#sequence number
	to_send.append(entire_data[0])
	to_send.append(zeros)
	to_send.append(ack_id)

	packet = pickle.dumps(to_send)
	s.sendto(packet, addr)

	# writefile = open("newfile.txt", "w")
	# #write to new file file 

	# writefile.write(entire_data[3])

	# writefile.close() 
