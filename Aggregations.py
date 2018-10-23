class Address():
	def __init__(self,couyntry,state,Area,street,zip_code):
		self.country=country
		self.state=
	def DepartmentInfo(self):
		return "Department Name : " +str(self.name) +", Location : " +str(self.loc)

class Manager():
	def __init__(self,m_id,name):
		self.m_id=m_id
		self.name=name
	def ManagerInfo(self):
		return "Manager Name : " +str(self.name) +",  Manager id : " +str(self.m_id)
class Employee():
    def __init__(self,Name,id_gen,dept=None,manager=None):
        self.Id=id_gen.generate()
        self.Name=Name
        self.D_id=None
        self.Salary=None
        self.dept=dept
        self.manager=manager
    def printDetails(self):


