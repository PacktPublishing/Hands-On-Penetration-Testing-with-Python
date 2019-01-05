import requests
import json
from urlparse import urljoin
import socket
import ast
import time
class Burp_automate():
	def __init__(self):
		self.result=""
		self.api_key="odTOmUX9mNTV3KRQ4La4J1pov6PEES72"
		self.api_url="http://127.0.0.1:1337"
	
	def start(self):
		try:
			
			data='{"application_logins":[{"password":"password","username":"admin"}],"scan_callback":{"url":"http://127.0.0.1:8001"},"scope":{"exclude":[{"rule":"http://192.168.250.1/dvwa/logout.php","type":"SimpleScopeDef"}],"include":[{"rule":"http://192.168.250.1/dvwa/","type":"SimpleScopeDef"}]},"urls":["http://192.168.250.1/dvwa/"]}'
			request_url=urljoin(self.api_url,self.api_key)
			request_url=str(request_url)+"/v0.1/scan"
			resp=requests.post(request_url,data=data)
			
			self.call_back_listener()
		except Exception as ex:
			print("EXception caught : " +str(ex))

	def poll_details(self,task_id):
		try:
			#curl -vgw "\n" -X GET 'http://127.0.0.1:1337/odTOmUX9mNTV3KRQ4La4J1pov6PEES72/v0.1/scan/11'
			while 1:
				data_json={}
				time.sleep(10)
				request_url=urljoin(self.api_url,self.api_key)
				request_url=str(request_url)+"/v0.1/scan/"+str(task_id)
				resp=requests.get(request_url)
				data_json=resp.json()
			
				issue_events=data_json["issue_events"]
				for issues in issue_events:
				
					if issues["issue"]["severity"] != "info":
						print("------------------------------------")
						print("Severity : " + issues["issue"].get("severity",""))
						print("Name : " + issues["issue"].get("name",""))
						print("Path : " + issues["issue"].get("path",""))
						print("Description : " + issues["issue"].get("description",""))
						if issues["issue"].get("evidence",""):
							print("URL : " + issues["issue"]["evidence"][0]["request_response"]["url"])
						print("------------------------------------")
						print("\n\n\n")
				if data_json["scan_status"]=="succeeded":
					break
			
		except Exception as ex:
			print(str(ex))

	def call_back_listener(self):
		try:
			if 1 :
				task_id=0
				s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.bind(('127.0.0.1', 8001))
				s.listen(10)
				
				conn, addr = s.accept()
				
				if conn:
					
					while True:
						data = conn.recv(2048)
						if not data:
							break
						try:
							index=str(data).find("task_id")
							task_id=str(data)[index:index+12]
							task_id=task_id.replace('"',"")
							splitted=task_id.split(":")
							t_id=splitted[1]
							t_id=t_id.lstrip().rstrip()
							t_id=int(t_id)
							if t_id:
								task_id=t_id
								break
						except Exception as ex:
							print("\n\n\nNot found" +str(ex))
							
				if task_id:
					print("Task id : " +str(task_id))
					self.poll_details(task_id)
				else:
					print("No task id obtaimed , Exiting : " )
						
		except Exception as ex:
			print("\n\n\n@@@@Call back exception :" +str(ex))

obj=Burp_automate()
obj.start()
		
