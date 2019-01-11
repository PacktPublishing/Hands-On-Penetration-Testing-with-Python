#! /usr/bin/python3.6
import json,sys
class JsonParse():
	def __init__(self,json_):
		self.json=json_
	def print_file(self):
		json_data=""
		with open(self.json,"r") as json_file:
			json_data=json.loads(json_file.read())
		if json_data:
			print("Type of loaded File is :"+str(type(json_data)))
			employee_root=json_data.get("employees",None)
			if employee_root:
				print("Department : " + employee_root["department"])
				print("Location : " + employee_root["location"])
				print("Employees : ")
				for emp in employee_root["data"]:
					print("\n--------------------------------")
					for k,v in emp.items():
						print("\t"+str(k)+" : " +str(v))		
	def process(self):
		with open(self.json,"r") as json_file:
			json_data=json.loads(json_file.read())
		if json_data:
			print("\nSlab Processing started")
			for index,emp in enumerate(json_data["employees"]["data"]):
				if emp["salary"] >= 30000:
					json_data["employees"]["data"][index]["slab"]="A"
				else:
					json_data["employees"]["data"][index]["slab"]="B"
			print("Slab Processing Ended \nSaving Results :")
			with open(self.json,"w") as json_file:
				json.dump(json_data, json_file , indent=4, sort_keys=True)
			print("Results saved \nNow reprinting : ")
			self.print_file()
obj=JsonParse(sys.argv[1])
obj.print_file()
obj.process()
