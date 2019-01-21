#! /usr/bin/python3.6
import threading
import time
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )
class Multi_Threads():
	def __init__(self):
		pass
	def execute(self):
		t = threading.currentThread()
		logging.debug("Enter : " +str(t.name))
		logging.debug("Executing : " +str(t.name))
		time.sleep(2)
		logging.debug("Exit : " +str(t.name))
		return
class Driver():
	def __init__(self):
		self.counter=0
	def main(self):
		m=Multi_Threads()
		total=6
		my_threads=[]
		while True:
			all_threads=threading.enumerate()
			if len(all_threads) < 4 and self.counter < 6:
				t=threading.Thread
				(name="Thread "+str(self.counter),target=m.execute)
				my_threads.append(t)
				t.start()
				self.counter=self.counter+1
			else:
				pass
			if self.counter >= 6:
				logging.debug("Exiting loop as 6 threads executed")
				break
		for t in my_threads:
			if t.isAlive():
				logging.debug("Thread :" + t.name +" is alive .Joining !")
				t.join()
			else:
				logging.debug("Thread : " +t.name + " Executed ")
		print("\nExiting main")
obj=Driver()
obj.main()
				
		
		
		
		
				
		
