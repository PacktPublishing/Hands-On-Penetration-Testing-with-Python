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

	def execute(self,type_):
		logging.debug("Enter : " +str(type_))
		time.sleep(4)
		logging.debug("Exit  " +str(type_))

obj=Processes()
p=mp.Process(name="Non Demon",
	target=obj.execute,args=("Non Demonic",))
p.daemon = True
logging.debug("Main started")
p.start()
logging.debug("Main Ended")
