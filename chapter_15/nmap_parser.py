from libnmap.parser import NmapParser
import sys

class nmap_parser:
	def __init__(self,report_file):
		self.report_file=report_file

	def parse(self):
		report=NmapParser.parse_fromfile(self.report_file)
		bulk_list=""
		hosts=report.hosts
		for host in hosts:
			if host.is_up():
				
				portso=host.get_open_ports()
				if portso:
					print("Up Host with service : " +str(host.address))
				for port_service in portso:
					
					service =host.get_service(port_service[0],port_service[1])
					print("\t Address : "+ str(host.address))
					print("\t Open Port : "+ str(port_service[0]))
					print("\t Service : "+ str(service.service))
					print("\t State : "+ str(service.state))
					print("\t Version /Banner: "+ str(service.banner))
					print("\n")
					
			else:
				print("Down Host : " +str(host.address))
obj=nmap_parser(sys.argv[1])
obj.parse()
