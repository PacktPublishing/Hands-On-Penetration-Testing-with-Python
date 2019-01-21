#! /usr/bin/python3.6


class Methods():
	class_var=200
	def __init__(self):
		self.variable=0

	def instance_method(self):
		self.variable=100
		print("------------------------------")
		print("Inside Instance Method")
		print("Instance is : " +str(self))
		print("Instance variable is : "+str(self.variable))
		print("Class variable is : " +str(self.__class__.class_var))
		print("------------------------------\n")
	@classmethod
	def class_method(cls):
		print("------------------------------")
		print("Inside Class Method")
		try:
			self.variable=22
			print("Instance variable is : "+str(Methods().variable))
		except Exception as ex:
			print("Cant access instance variable in class method")
		cls.class_var=33
		print("Class is : " +str(cls))
		print("Class variable is : "+str(cls.class_var))
		print("------------------------------\n")

	@staticmethod
	def static_method():
		print("Inside Static Method")
		try:
			print("Class=%s and Instance variable =%s : ",(class_var,str(self.variable)))
		except Exception as ex:
			print("Cant access class and  instance variable in static method")
class Driver():
	def main(self):
		o=Methods()
		o.instance_method()
		o.class_method()
		Methods.class_method()
		o.static_method()
		Methods.static_method()
		print("\n*****************************************************")
		print("Lets see variable access of class variables\n\n")
		print("--------------------------------------------------")
		print('Accessing class variable with Instance "o" : '+str(o.class_var))
		o.class_var=222
		print('Modifying class variable with Instance "o" : o.class_var = 222')
		print('Accessing modified class variable with Instance "o" : ' +str(o.class_var))
		print("--------------------------------------------------\n\n")
		print("-------------------------------------------------")
		oo=Methods()
		print('Accessing class variable with New instance  "oo" : '+str(oo.class_var))
		print('Changes not persisted thus modifying o.class_var created local copy for instance o')
		print("--------------------------------------------------\n\n")
		print("-------------------------------------------------")
		print('Accessing class variable with Class variable  : '+str(Methods.class_var))
		print('Changes not persisted thus modifying o.class_var created local copy for instance o')
		print("--------------------------------------------------\n\n")
		print("\n*****************************************************\n")
d=Driver();d.main()


			
		
		

		

