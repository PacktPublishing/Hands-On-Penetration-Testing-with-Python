#!/usr/bin/python3.5
class Car():
	def __init__(self,cat,mil,cap):
		self.category=cat
		self.milage=mil
		self.capacity=cap
class Ferarri(Car):
	def __init__(self,cat,mil,cap,HP,TS,ACC):
		super().__init__(cat,mil,cap)
		self.HorsePower=HP
		self.TopSpeed=TS
		self.Acceleration=ACC
	def printCarDetails(self):
		engine=Engine()
		print("Catagory : "+str(self.category))
		print("Milage : "+str(self.milage))
		print("Capacity : "+str(self.capacity))
		print("Horse Power : "+str(self.HorsePower))
		print("Top Speed : "+str(self.TopSpeed))
		print("Acc : "+str(self.Acceleration))
		print("Engine :")
		print("\t"+str(engine.Details()))
class Engine():
	def __init__(self):
		self.details=None
	def Details(self):
		self.details="""
	The 458 is powered by a 4,499 cc (274.5 cu in; 4.5 L) V8 engine of the 
	"Ferrari/Maserati" F136 engine family,producing 570 PS (419 kW; 562 hp) at 9,000
	rpm (redline) and 540 N⋅m (398 lb⋅ft) at 6,000 rpm with 80% torque available at 3,250 rpm"""
		return self.details
obj=Ferarri("Sports","4kmph","4 seater","660 horsepower","349 km/h","2.9 sec")
obj.printCarDetails()


