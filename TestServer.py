#SERVER WILL RECEIVE INFO AND ACK
import socket 
import pickle
import sys
from collections import namedtuple
import random
import time
import datetime

MSS = 1024 # Max Segment Size (needs to be re-addressed)

TCP_IP = "127.0.0.1"
TCP_PORT = 7735

#LISTEN ON PORT 7735
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))

while 1:
	s.listen(1)
	c, addr = s.accept()

	entire_data = c.recv(MSS)
	print entire_data
	#check checksum is correct, if not, do nothing
	#check to see if in sequence, if not do nothing
	#elsif checksum and in sequence then send ACK
	#then create file and add passed info into it
	writefile = open("newfile.txt", "w")
	#write to new file file 
	writefile.write(entire_data)
	writefile.close() 
