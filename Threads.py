#! /usr/bin/python3.6
import threading
import time
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )
class Threads():
	def __init__(self):
		pass

	def execute(self,type_):
		logging.debug("Enter : " +str(type_))
		time.sleep(4)
		logging.debug("Exit  " +str(type_))

obj=Threads()
t=threading.Thread(name="Demon",
	target=obj.execute,args=("Demonic",))
t.setDaemon(True)
logging.debug("Main started")
t.start()
logging.debug("Main Ended")
#
