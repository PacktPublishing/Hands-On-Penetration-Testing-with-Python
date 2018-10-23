#! /usr/bin/python3.5
import math
class Shape:
	def __init__(self,length=None,breadth=None,height=None,radius=None):    
		self.length=length
		self.breadth=breadth
		self.height=height
		self.radius=radius
	def area(self):             
		raise NotImplementedError("Not Implemented")

class Square(Shape):
	def __init__(self,l,b):
		super().__init__(l,b)
	def area(self):
		print("Square Area :" +str(self.length*self.breadth))

class Circle(Shape):
	def __init__(self,r):
		super().__init__(radius=r)
	def area(self):
		print("Circle Area :" +str(math.pi * self.radius**2))
s=Square(3,4)
s.area()
c=Circle(2)
c.area()

