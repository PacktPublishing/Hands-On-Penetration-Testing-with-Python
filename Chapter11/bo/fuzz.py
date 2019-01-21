#!/usr/bin/python
import subprocess as sp
import time
def fuzz():
	i=1
	while 1:
		
		fuzz_str='a'*i
		p=sp.Popen("echo "+fuzz_str+" | ./buff",stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.PIPE,shell=True)
		out=p.communicate()[0]
		output=out.split("\n")
		if "What" in output[0]:
			print(output[0]+"\n"+output[1]+"\n")
			print("Fuzz passed at : Length : "+str(len(fuzz_str)))
			i=i+10
		else:
			print(output)
			print("Application crashed at input length : " +str(len(fuzz_str)))
			break
		#time.sleep(2)

fuzz()
