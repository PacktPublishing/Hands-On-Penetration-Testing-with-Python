#!/usr/bin/python3.5
class ASP_Parent():
	def __init__(self,pub,prot,priv):
		self.public=pub
		self._protected=prot
		self.__private=priv
class ASP_child(ASP_Parent):
	def __init(self,pub,prot,priv):
		super().__init__(pub,prot,priv)
	def printMembers(self):
		try:
			print("Public is :" + str(self.public))
			print("Protected is : " + str(self._protected))
			print("Private is : " + str(self.__private))
		except Exception as ex:
			print("Ex: " +str(ex))
			#pr=ASP_Parent()
			print("Private is : " +str(self._ASP_Parent__private))

ch=ASP_child(1,2,3)
ch.printMembers()
print("Public outside :"+str(ch.public))
print("Protceted outside :"+str(ch._protected))			
print("Private outside :"+str(ch._ASP_Parent__private))		




