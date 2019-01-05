#! /usr/bin/python3.5
class Ferrari():
	def speed(self):
		print("Ferrari : 349 km/h")

class Mclern():
	def speed(self):
		print("Mclern : 362 km/h")

def printSpeed(carType):
	carType.speed()

f=Ferrari()
m=Mclern()
printSpeed(f)
printSpeed(m)


