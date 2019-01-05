#! /usr/bin/python3.5

import threading
import time
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',)
counter=0
class Communicate():
	def __init__(self):
		pass
	def wait_for_event(self,e):
		global counter
		logging.debug("Wait for counter to become 5")
		is_set=e.wait()
		logging.debug("Hurray !! Now counter has become %s",counter)
	def increment_counter(self,e,wait_time):
		global counter
		while counter < 10 :
			logging.debug("About to increment counter")
			if e.is_set() ==False:
				e.wait(wait_time)
			else:
				time.sleep(1)
			counter=counter +1
			logging.debug("Counter Incremented : %s ",counter)
			if counter == 5:
				e.set()	
obj=Communicate()
e=threading.Event()
t1=threading.Thread(name="Thread 1",target=obj.wait_for_event,args=(e,))
t2=threading.Thread(name="Thread 2",target=obj.increment_counter,args=(e,1))
t1.start()
t2.start()

