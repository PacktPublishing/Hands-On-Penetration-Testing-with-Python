#! /usr/bin/python3.6
import multiprocessing as mp
import time
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='(%(processName)-10s) %(message)s',
                    )
class Processes():
	def __init__(self):
		pass

	def execute(self,id):
		time.sleep(1)
		logging.debug("Executed Process : " +str(id))
obj=Processes()
process_list=[]
for i in range(10):
	p=mp.Process(name="Process_"+str(i),target=obj.execute,args=(i,))
	process_list.append(p)
	p.start()


main_process=mp.current_process()
logging.debug("Waiting for 3 seconds")
counter =0
for p in process_list:
	if p.is_alive() and counter < 1:
		p.join(3)
		counter=counter + 1
	else:
		if p.is_alive():
			logging.debug("Killing process: " +p.name )
			p.terminate()
	
logging.debug("Main Ended")
