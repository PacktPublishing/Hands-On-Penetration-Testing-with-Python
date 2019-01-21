from libnessus.parser import NessusParser
import sys
class Nessus_Parser:
	def __init__(self,file_name):
		self.n_file=file_name

	def demo_print(self,nessus_obj_list):
		docu = {}
		OKGREEN = '\033[92m'
		OKBLUE = '\033[94m'
		OKRED = '\033[93m'
		for i in nessus_obj_list.hosts:
				print(OKRED +"Host : "+i.ip+"	Host Name : "+i.name +"	OS : "+i.get_host_property('operating-system'))	
				for v in i.get_report_items:
					print("\t"+OKGREEN+str("Plugin id :"+OKBLUE+str(v.plugin_id)))
					print("\t"+OKGREEN+str("Plugin name : "+OKBLUE+str(v.plugin_name)))
					print("\t"+OKGREEN+"Sevirity : "+OKBLUE+str(v.severity))
					print("\t"+OKGREEN+str("Service name :"+OKBLUE+str(v.service)))		
					print("\t"+OKGREEN+str("Protocol :"+OKBLUE+str(v.protocol)))
					print("\t"+OKGREEN+str("Port : "+OKBLUE+str(v.port)))
					print("\t"+OKGREEN+"Synopsis :"+OKBLUE+str(v.synopsis))
					print("\t"+OKGREEN+"Description : \n\t"+OKBLUE+str(v.description))
					print("\t"+OKGREEN+"Risk vectors :"+OKBLUE+str(v.get_vuln_risk))
					print("\t"+OKGREEN+"External references :"+OKBLUE+str(v.get_vuln_xref))
					print("\t"+OKGREEN+"Solution :"+OKBLUE+str(v.solution))
					print("\n")
	def parse(self):
			file_=self.n_file
			try:
				nessus_obj_list = NessusParser.parse_fromfile(file_)
			except Exception as eee:
				print("file cannot be imported : %s" % file_)
				print("Exception 1 :"+str(eee))
				return 
			self.demo_print(nessus_obj_list)
obj=Nessus_Parser(sys.argv[1])
obj.parse()
			
