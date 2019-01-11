#! /usr/bin/python3.6
from abc import ABC, abstractmethod

class QueueAbs(ABC):
	def __init__(self):
		self.buffer=[]

	def printItems(self):
		for item in self.buffer:
			print(item)
	@abstractmethod
	def enqueue(self,item):
		pass
	@abstractmethod
	def dequeue(self):
		pass

class Queue(QueueAbs):

	def __init__(self,length):
		super().__init__()
		self.length=length

	def enqueue(self,item):
		is_full=self.length <= len(self.buffer)
		if is_full:
			print("Queue is full")
			return
		self.buffer.append(item)
		
	
	def dequeue(self):
		if len(self.buffer) == 0:
			print("Empty Queue")
			return 
		item=self.buffer[0]
		del self.buffer[0]
		return item


class Driver():
	def main(self):
		q=Queue(10)
		print("Enqueing")
		for item in range(0,10):
			q.enqueue(item)
		print("Printing")
		q.printItems()
		print("Dequeing")
		for item in range(0,10):
			item=q.dequeue()
			print(item)
		

d=Driver()
d.main()

			
		
		

		

