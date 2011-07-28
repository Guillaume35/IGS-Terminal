#! /usr/bin/env python
# -*- coding: UTF-8 -*-

'''
    IGS-term is a tool to control Illusion Games Server
    Copyright (C) 2011  Guillaume Modard <guillaumemodard@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
'''

import os
import re, socket

VERSION		= (1,0,0,1) # Last number : 0 = Alpha, 1 = Beta, 2 = Stable
BETA		= 1 # Beta version
BUILTIN		= ['connect', 'add_server', 'ls_servers', 'rm_server', 'home_path', 'init']
SERVERS		= []
HOME		= os.getenv("HOME")
HOMECFG		= HOME+'/.illusion/igsterm'

def init():
	"""This function initialize IGS-term"""
	
	home_path()
	
	if not os.path.exists(HOMECFG+'/serverslist'):
		try:
			f = open(HOMECFG+'/serverslist','w')
			f.close()
		except:
			print ('ER: I/O error, unable to create '+HOMECFG+'/serverslist')
	return 0

def connect(host,port):
	"""This function connect IGS-term to a IGS server"""
	
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except:
		print ('ER: Unable to connect this server.')
	
	try:
		sock.connect((host,int(port)))
		main(host,port,sock)
		sock.close()
	except:
		print ('ER: Unable to connect this server.')
		
	
	return 0

def home_path():
	"""This function test and creat .illusion/igsterm if not exists"""
	
	if not os.path.exists(HOMECFG):
		try:
			os.makedirs(HOMECFG)
		except:
			print ('ER: I/O error, unable to create '+HOMECFG+' directory')
			return 0
	return 1

def ls_servers():
	"""Read the serverslist file"""
	
	global SERVERS
	SERVERS = []
	
	if not home_path():
		print ('ER: Unable to perform this operation')
		return 0
	
	try:
		f = open(HOMECFG+'/serverslist', 'r')
	except:
		print ('ER: I/O error, unable to open serverslist')
		return 0
	
	print ('Read and update registered servers list')
	
	i = 1
	for line in f:
		srv = re.sub(r'\s$', '', line)
	
		if not re.search(r'^#', srv) and srv and re.search(r'\w', srv):
			srv = srv.split(":")
		
			if [srv[0],srv[1]] not in SERVERS:
				SERVERS.append([srv[0],int(srv[1])])
				
				print ('\t'+str(i)+'. '+srv[0]+':'+str(srv[1]))
				i += 1
	
	f.close()
	
	return 0

def add_server(host,port):
	"""Register a server in serverslist file"""
	
	global SERVERS
	ls_servers() # update server list
	
	if not home_path():
		print ('ER: Unable to perform this operation')
		return 0
	
	# If not registered
	if [host,port] not in SERVERS:
		try:
			f = open(HOMECFG+'/serverslist','a')
		except:
			print ('ER: I/O error, unable to write serverslist file')
			return 0
		
		f.write (host+':'+str(port)+'\n')
		f.close()
		
		SERVERS.append([host,int(port)])
		
		print ('\t'+str(len(SERVERS))+'. '+host+':'+str(port))
		print ('The server has been added in serverslist.')
	
	else:
		print ('INF: This server is already registered')
	
	return 0
	

def rm_server(host,port):
	"""Remove a server from serverslist file"""
	
	if not home_path():
		print ('ER: Unable to perform this operation')
		return 0
	
	try:
		f = open(HOMECFG+'/serverslist','r')
	except:
		print ('ER: I/O error, serverslist file does not exist')
		return 0
	
	cont = f.read()
	cont = re.sub(host+':'+str(port), '', cont)
	
	f.close()
	
	try:
		f = open(HOMECFG+'/serverslist','w')
	except:
		print ('ER: I/O error, serverslist file is not writable')
		return 0
	
	f.write(cont)
	f.close()
	
	ls_servers()
	
	print (host+':'+str(port)+' has been removed.')
	
	return 0

def main(host='',port='',sock='',options=()):
	"""IGS-term main command"""
	
	if not host and not port:
		print ('Use registered servers :')
			
		i = 0
		for srv in SERVERS:
			i += 1
			if 'do not list' not in options:
				print ('\t'+str(i)+'. '+srv[0]+':'+str(srv[1]))

		if i == 0:
			print ('\tNo registered servers.')
			print ('\tUse igst.add_server(host,port) to register a new server.')
			print ('\tUse igst.ls_servers() to update this list.')
		else:
			print ('To use one of these registered server, just enter its number in the command line')
	
	while True:
		serv = ''
		then = 0
		
		if host and port:
			serv = ' '+host+':'+str(port)
		
		q = input ("igst"+serv+"~$ ") # igst command line
		
		exit	= ['exit', 'quit']
		
		if not q or q in exit:
			break
		
		if re.search(r'^[0-9]+$', q):
			srv_id = int(q) - 1
			
			if srv_id < len(SERVERS) and srv_id >= 0:
				connect(SERVERS[srv_id][0], SERVERS[srv_id][1])
				then = 1
				break
		
		if q == 'show w':
			print ('')
			print ('    THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY')
			print ('    APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT')
			print ('    HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY')
			print ('    OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,')
			print ('    THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR')
			print ('    PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM')
			print ('    IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF')
			print ('    ALL NECESSARY SERVICING, REPAIR OR CORRECTION.')
			print ('')
			
			then = 1
			break
		if q == 'show c':
			
			print ('')
			print ('    This program is free software: you can redistribute it and/or modify')
			print ('    it under the terms of the GNU General Public License as published by')
			print ('    the Free Software Foundation, either version 3 of the License, or')
			print ('    (at your option) any later version.')
			print ('')
			print ('    This program is distributed in the hope that it will be useful,')
			print ('    but WITHOUT ANY WARRANTY; without even the implied warranty of')
			print ('    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the')
			print ('    GNU General Public License for more details.')
			print ('')
			print ('    You should have received a copy of the GNU General Public License')
			print ('    along with this program.  If not, see <http://www.gnu.org/licenses/>.')
			print ('')
			
			then = 1
			break
		
		cmd = re.sub (r'^(\w+).*$', r'\1', q)
		
		# igst built in method
		if cmd == 'igst':
			method = re.sub(r'^igst\.(\w+)\(.*\).?$', r'\1', q)
			
			# execute the built in method
			if  method in BUILTIN:
				cmd = re.sub(r'^igst\.', r'', q)
				
				try:
					back = eval (cmd)
					print (back)
					
				except:
					print ('ER: Unable to excute the command. Check the syntax')
			
			else:
				print ('ER: Unknown command')
		
		else:
			if host and port:
				sock.send(bytes(q, "utf-8"))
				
				r = sock.recv(1024)
				r = str(r)
				r = re.sub(r"^b'","",r)
				r = re.sub(r"'$","",r)
				
				print ("IGS> "+r)
				
			else:
				print ('ER: You are not connected to any server. This command is not available')
	
	if then:
		main(host,port,sock)
		return 0
	
	# User enter quit command
	if host and port:
		msg = 'Disconnect from '+host+':'+str(port)+' ? (yes/no) '
	else:
		msg = 'Exit IGS-term ? (yes/no) '
	
	q = input (msg)
	
	if q != 'yes' and q != 'y' and q != '1':
		main(host,port,sock) # Reload igst

if __name__ == "__main__":
	print ('')
	print ('		* WELCOME ON IGS-term *')
	print ('		     Version '+str(VERSION[0])+'.'+str(VERSION[1])+'.'+str(VERSION[2]))
	
	v_type = ('Alpha', 'Beta', 'Stable')
	if VERSION[3] == 0:
		v1 = ALPHA
	elif VERSION[3] == 1:
		v1 = BETA
	else:
		v1 = ''
	
	print ('		          '+v_type[VERSION[3]]+str(v1))
	
	print ('')
	print ('    IGS-term  Copyright (C) 2011  Guillaume Modard <guillaumemodard@gmail.com>')
	print ('    This program comes with ABSOLUTELY NO WARRANTY; for details type \'show w\'.')
	print ('    This is free software, and you are welcome to redistribute it')
	print ('    under certain conditions; type \'show c\' for details.')
	print ('')
	print ('    IGS-term is a client that permit you to connect to an Illusion Games ')
	print ('    Server. Read the manual corresponding to your version.')
	print ('')
	print ('    CAUTION: This is a Beta version. Thank\'s to report bugs to')
	print ('    developpers.')
	print ('')
	
	init()
	
	ls_servers()
	main(options=('do not list'))
