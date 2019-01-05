#! /usr/bin/python3.6
class Id_Generator():
	def __init__(self):
		self.id=0
	def generate(self):
		self.id=self.id + 1
		return self.id

class Employee():
	
	def __init__(self,Name,id_gen):
		self.Id=id_gen.generate()
		self.Name=Name
		self.D_id=None
		self.Salary=None
	
	def printDetails(self):
		print("\n")
		print("Employee Details : ")
		print("ID : " +str(self.Id))
		print("Name : " +str(self.Name))
		print("Salary : " + str(self.Salary))
		print("------------------------------")

class Programmer(Employee):
	def __init__(self,name,id_gen,lang=None,
		db=None,projects=None,**add_skills):
		self.languages=lang
		self.db=db
		self.projects=projects
		self.add_skils=add_skills
		super().__init__(name,id_gen)
	def printSkillDetails(self):
		print("ID : " +str(self.Id))
		print("Name : " +str(self.Name))
		print("Salary : " + str(self.Salary))
		print("Languages : ")
		for l in self.languages:
			print("\t" +str(l))
		print("Databases : ")
		for d in self.db:
			print("\t" +str(d))
		print("Projects : ")
		for p in self.projects:
			print("\t" +str(p))
		print("Add Skills : ")
		for k,v in self.add_skils.items():
			print("\t"+str(k) +" : ")
			for skill in v :
				print("\t\t"+str(skill))		
Id_gen=Id_Generator()
p=Programmer("Programmer1",Id_gen,["c","c++","java",
	"python","vb"],
	["mysql","sql server","oracle"],
	["PT Framework","Web scanning Framework",
	"SOC Orchestration Framework"],
	os=["windows","centos","kali"],
	nosql=["mongo db","redis","rabbit mq","basex"]
	,data_science=["machine learning","AI",
	"Regression Models","Classification Models",
	"Clustering","Neural Networks","NLP"])
p.printSkillDetails()


#emp1.printDetails()
#emp2.printDetails()


"""
emp1=Employee("Emp1",Id_gen)
emp1.Salary=20000
emp1.D_id=2
emp2=Employee("Emp2",Id_gen)
emp2.Salary=10000
emp2.D_id=1
"""

