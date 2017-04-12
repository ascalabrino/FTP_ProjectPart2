import socket  
import sys
from collections import namedtuple
import pickle
import threading
import inspect
import time
import signal

global entire_list
global sequence_number
global window_size
global file_start 
global original_sequence
global copy_sequence
original_sequence = []
copy_sequence = []

sequence_number = 00000000000000000000000000000000
checksum = 0000000000000000
data_packet = 0101010101010101
SERVER_IP = "127.0.0.1"

#READ IN FROM COMMAND LINE --> Simple_ftp_server server-host-nae server-port# file-name N MSS
server_host_name = sys.argv[1]
server_port = sys.argv[2]
file_name = sys.argv[3]
window_size = sys.argv[4]
MSS = sys.argv[5]

server_port = int(server_port)
window_size = int(window_size)
MSS = int(MSS)

#ESTABLISHED CONNECTION BASED OFF OF PORT SENT
c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# c.connect((SERVER_IP, server_port))
#c.send("HELLO FROM THE CLIENT")
#hello = c.recv(MSS)
#print hello 
# data = 

def read_file(file):
	file_start=0
	access = open( file , "r")
	entire_list = access.read()
	access.close()

	entire_list = str(entire_list)

	if entire_list == "":
		sock.close()
	else:
		rdt_send()

def rdt_send(file, size, check, dta, sock):
	#  Caluclate sequence number
	file_start = sequence_number * (size-8)

	#clear the original seq. array 
	original_sequence = []	
	index = 0
	while index < window_size:
		if file_start >= len(entire_list):
			sock.close()
			break
		else:
			to_send = []
			to_send.append(sequence_number)
			to_send.append(check)
			to_send.append(dta)
			if (file_start+(size-8)) > len(entire_list):
				to_send.append(entire_list[file_start:len(entire_list)])
				packet = pickle.dumps(to_send)
				sock.sendto(packet, (SERVER_IP, server_port))
				file_start=file_start+(size-8)
				original_sequence.append(sequence_number)
				sequence_number+=1
				print "TO SEND ",to_send
				index+=1
			else:
				to_send.append(entire_list[file_start:file_start+(size-8)])
				packet = pickle.dumps(to_send)
				sock.sendto(packet, (SERVER_IP, server_port))
				file_start=file_start+(size-8)
				original_sequence.append(sequence_number)
				sequence_number+=1
				print "TO SEND ",to_send
				index+=1
	# Start Timer
	timer = time.time()
	wait_for_ack(sock)

def wait_for_ack(sock):
	
	ack_count=0
	
	for i in original_sequence:
		copy_sequence[i] = original_sequence[i]
	#used to be while 1:
	while (time.time() - timer) >= 10:
		recv_packet, addr = s.recvfrom(MSS)
		recv_packet = pickle.loads(recv_packet)

		ack_sequence = recv_packet[0]
		zeros = recv_packet[1]
		ack_indicator = recv_packet[2]

		# Ensure that ack_sequence has a proper value before executing LOC below
		if ack_sequence < sequence_number:
			if ack_indicator != "1010101010101010":
			    print "waiting for ack"
			else:
				# Handlre multiple ACKS and timers
				for i in copy_sequence:
					if ack_sequence == copy_sequence[i]:
						# Remove this
						copy_sequence.remove(copy_sequence[i])
						ack_count+=1

				if ack_count == window_size:
					break
				# if timer expired break ASAP
				# else wait until ack_count = window size and then break
				
		else:
			# Handle error - ACK number out of bounds
			print "ACK number out of bound!"

	sequence_number = min(copy_sequence)
	copy_sequence = []
	rdt_send(sock)



# #PROVIDES INFO FROM A FILE ON A BYTE BASIS
# def rdt_send(file, size, seq, check, dta):
	

# 	#while the file has info, lets send them
# 	while True:
# 		#read in HEADER + (MSS - 8 byte Header amount of info)
# 		file = str(seq) + str(check) + str(dta) + str(access.read(size-8))
# 		#if no info break 
		# if file == "":
		# 	access.close()
		# 	#c.close()
		# 	break
		# #if info, we want to send at MSS data
		# else:
			#Need to wait until next ACK and window to advance to send next
			#if window == 1 
			#c.sendall(file)		
read_file(file_name)
# rdt_send(file_name, window_size, MSS, sequence_number, checksum, data_packet, c)
