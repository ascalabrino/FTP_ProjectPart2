#SERVER WILL RECEIVE INFO AND ACK
import socket 
import pickle
import sys
from collections import namedtuple
import random
import time
import datetime
import random

global zeros
zeros = 0000000000000000
global ack_id
ack_id = 1010101010101010
global sequence_num
sequence_num = 0
#a number 0<p<1
global PORT
PORT = sys.argv[0]
global file_name
str(file_name) = sys.argv[1]
global probability
probability = sys.argv[2]

MSS = 1024 # Max Segment Size (needs to be re-addressed)

IP = "127.0.0.1"


#LISTEN ON PORT 7735
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((IP, PORT))

# Carry bit used in one's combliment
def carry_checksum_addition(num_1, num_2):
    c = num_1 + num_2
    return (c & 0xffff) + (c >> 16)


# Calculate the checksum of the data only. Return True or False
def calculate_checksum(dta):
    checksum = 0
    for i in range(0, len(dta), 2):
        my_message = str(dta)
        w = ord(my_message[i]) + (ord(my_message[i+1]) << 8)
        checksum = carry_checksum_addition(checksum, w)
    return (not checksum) & 0xffff

while 1:
	# s.listen(1)

	packet, addr = s.recvfrom(MSS)
	entire_data = pickle.loads(packet)
	print entire_data
	r = random.random()
	#entire_data[0] = sequence number, entire_data[1] = checksum, entire_data[2] = data packet indicator, entire_data[3] = actual data
	
	#check probability if packet made it
	if r <= probability:
		print "Packet loss, sequence number = " + str(entire_data[0])
	#check checksum passed is correct, if not, do nothing
	elif entire_data[1]!= calculate_checksum(entire_data[2]):
		print "PACKET IS CORRUPT ... DROPPING PACKET!"
		#do nothing else

	#check to see if in sequence, if not do nothing
	elif sequence_num != entire_data[0]:
		print "OUT OF ORDER PACKET DETECTED!"
		#do nothing else

	#elsif checksum and in sequence then send ACK
	else:
		to_send=[]
		#sequence number
		to_send.append(entire_data[0])
		to_send.append(zeros)
		to_send.append(ack_id)
		#then create file and add passed info into it	

		packet = pickle.dumps(to_send)
		s.sendto(packet, addr)
		sequence_num+=1

		# #write to new file file 
		# writefile = open(file_name + ".txt", "w")
		# writefile.write(entire_data[3])
		# writefile.close() 
