#! /usr/bin/python3.5

import threading
import time
import logging
import random

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',)
class ResourceControl():
	def __init__(self):
		self.counter=0
		self.lock=threading.Lock()

	def increment_counter(self):
		self.lock.acquire()
		try:
			logging.debug('Acquired lock -- ' +str(self.counter))
			self.counter=self.counter+1
		finally:
			logging.debug("Releasing Lock -- " +str(self.counter))
			self.lock.release()
        
	def execute(self):
		th=threading.currentThread()
		self.increment_counter()
	

	def start_threads(self,count):
		for i in range(count):
			t=threading.Thread(name="Thread_"+str(i),target=self.execute)
			t.start()
r=ResourceControl()
r.start_threads(5)
for t in threading.enumerate():
    if t is not threading.currentThread():
        t.join()
print("Counter value : " +str(r.counter))

