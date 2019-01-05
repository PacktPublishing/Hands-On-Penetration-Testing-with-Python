#! /usr/bin/python3.5
class Id_Generator():
    def __init__(self):
        self.id=0
    def generate(self):
        self.id=self.id + 1
        return self.id
class Department():
	def __init__(self,name,location):
		self.name=name
		self.loc=location
	def DepartmentInfo(self):
		return "Department Name : " +str(self.name) +", Location : " +str(self.loc)

class Manager():
	def __init__(self,m_id,name):
		self.m_id=m_id
		self.name=name
	def ManagerInfo(self):
		return "Manager Name : " +str(self.name) +",  Manager id : " +str(self.m_id)
class Address():
	def __init__(self,country,state,area,street,zip_code):
		self.country=country
		self.state=state
		self.area=area
		self.street=street
		self.zip_code=zip_code
	def AddressInfo(self):
		return "Country : " +str(self.country)+", State : " +str(self.state)+", Street : "+str(self.area)	
class Employee():
    def __init__(self,Name,id_gen,dept=None,manager=None,address=None):
        self.Id=id_gen.generate()
        self.Name=Name
        self.D_id=None
        self.Salary=None
        self.dept=dept
        self.manager=manager
        self.address=address
    def printDetails(self):
        print("\n")
        print("Employee Details : ")
        print("ID : " +str(self.Id))
        print("Name : " +str(self.Name))
        print("Salary : " + str(self.Salary))
        print("Department :\n\t"+str(self.dept.DepartmentInfo()))
        print("Manager : \n\t" +str(self.manager.ManagerInfo()))
        print("Address : \n\t" +str(self.address.AddressInfo()))
        print("------------------------------")
Id_gen=Id_Generator()
m=Manager(100,"Manager X")
d=Department("IT","Delhi")
a=Address("UAE","Dubai","Silicon Oasis","Lavista 6","xxxxxx")
emp1=Employee("Emp1",Id_gen,d,m,a)
emp1.Salary=20000
emp1.D_id=2
emp1.printDetails()
"""emp2=Employee("Emp2",Id_gen)
emp2.Salary=10000
emp2.D_id=1
emp1.printDetails()
emp2.printDetails()"""
