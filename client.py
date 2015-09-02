#! /usr/bin/python
#######Client code for remote shell  #########
#################Coded By: Jagmohan Singh#################################
########for use : See README####################
import signal 
import time
import socket
import sys
import threading
global target 
global port 
port =1337 ##port of the server on which client has top connect
global servers 
global connectedServers 
servers=sys.argv[1:]  ##command line IPS or hostname of the servers
connectedServers=[]  ###Initialize empty list for connected servers
def multiple_connections_server():   ###fucntion to create connection to multiple servers
	j=0
	for i in servers:
		client=socket.socket(socket.AF_INET,socket.SOCK_STREAM) ##creating socket for connecting to server
		try:
			client.connect((i,port))
			connectedServers.append([client,i])     ###adding the connected server to the list of connected server 
		except:
			print "Could not connect to the server %s"%i			 
			client.close()
		j+=1	
	client_sender()		###calling the function for each connection to accept command as input giving back the result	
def client_sender():   ######fucntion to implement the shell interface
		#print connectedServers
		sys.stdout.write("shell:~#")
		buffer=raw_input()      ####taking the command as input
		buffer+="\n"
		while(1):
			index=0            ###falg for keeping the count of alive connections
			if not connectedServers:        
				sys.exit("No connected servers Exiting the program")
			else:
				for connection in connectedServers:    #####iterative for each connection 
					connectionStatus=1
					closedflag=0
					index+=1
					ip=connection[1]+":~#"           ####server name or IP for each line
					if(len(buffer)):          
						try:
							connection[0].send(buffer)
						except:
							print "Some error in input"						
					recv_len=1
					response=""
					while recv_len:
						try:
							data = connection[0].recv(1024)
						except:
							#connection[0].close()
							#closedflag=1
							print "connection terminated on %s"	%connection[1]						
						if(len(data)==0 ):
							connection[0].close()			####closing the connection
							print "connection on %s is closed" %connection[1]   
							connectedServers.pop(index-1)
							connectionStatus=0
							index-=1
							if not connectedServers:
								sys.exit("No alive connection Exiting the program")
						else:							
							response+=data						##making the response with received data
							recv_len=len(data)
							if(recv_len<1024):
								break
					
					response=response.split('\n')
					if(connectionStatus==0):
						pass
					else:						
						for i in response:					###printing the response
							print ip+i
			sys.stdout.write("shell:~#")				
			buffer=raw_input("")
			buffer+="\n"
		for i in connectedServers:
			i[0].close()					####closing all the connections
		sys.exit("Exiting the program")


multiple_connections_server()###calling the primary function to connect to the servers


