#! /usr/bin/python3.5
import xml.etree.ElementTree as ET
import sys
class XML_parser():
	def __init__(self,xml):
		self.xml=xml
		
	def parse(self,parse_type="doc"):
		#root=ET.fromstring(country_data_as_string)
		if parse_type =="doc":
			root = ET.parse(self.xml).getroot()
		else:
			root=ET.fromstring(self.xml)
		tag = root.tag
		print("Root tag is :"+str(tag))
		attributes = root.attrib
		print("Root attributes are :")
		for k,v in attributes.items():
			print("\t"+str(k) +"  : "+str(v))
		print("\nPrinting Node Details without knowing subtags :")
		for employee in root: #.findall(tag)
			# access all elements in node
			print("\n-----------------------------")
			for element in employee:
				ele_name = element.tag
				ele_value = employee.find(element.tag).text
				print("\t\t"+ele_name, ' : ', ele_value)

		print("\n\nPrinting Node Details specifying subtags :")
		for employee in root.findall("employee"):
			print("\n-----------------------------")
			print("\t\tName :" +str(employee.find("name").text))
			print("\t\tSalary :" +str(employee.find("salary").text))
			print("\t\tAge :" +str(employee.find("age").text))
			print("\t\tManager Id :" +str(employee.find("manager_id").text))
			print("\t\tDOJ :" +str(employee.find("doj").text))		
obj=XML_parser(sys.argv[1])
obj.parse()

xml="""<employees department="IT"  location="Dubai">
    <employee id="1">
        <name>Emp1</name>
	<age>32</age>
	<salary>30000</salary>
	<doj>06/06/2016</doj>
	<manager_id>33</manager_id>
    </employee>
    <employee id="2">
        <name>Emp2</name>
	<age>28</age>
	<salary>27000</salary>
	<doj>18/02/2017</doj>
	<manager_id>33</manager_id>
    </employee>
</employees>"""
#obj=XML_parser(xml)
#obj.parse("string")

