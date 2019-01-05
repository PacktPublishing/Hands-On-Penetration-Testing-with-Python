#! /usr/bin/python3.5
import subprocess
import datetime as dt
import sys
import chardet
import psutil
"""
process = psutil.Process(1)
print(process.status())
print(process.username())
"""
class SP():
	def execute(self,command=[]):
		try:
			p=subprocess.Popen(command,
			shell=False,stderr=subprocess.PIPE,
			stdout=subprocess.PIPE)
			print("ID of spawned process is :"+str(p.pid)+"\n")
			out,err=p.communicate()
			result = chardet.detect(out)
			out=str(out).encode('ascii')
			out=out.decode("utf-8") 
			splitted=str(out).split("\\n")
			for o in splitted:
				print(o)
			
			#print(dir(process))
		except Exception as ex:
			print("Exception caught :"+str(ex))			
obj=SP()
obj.execute(["ls","-l"])	

