import requests

class Detect_CJ():
	def __init__(self,target):
		self.target=target

	def start(self):
		try:
			resp=requests.get(self.target)
			headers=resp.headers
			print ("\n\nHeaders set are : \n" )
			for k,v in headers.iteritems():
				print(k+":"+v)

			if "X-Frame-Options" in headers.keys():
				print("\n\nClick Jacking Header present")
			else:
				print("\n\nX-Frame-Options is missing ! ")

		except Exception as ex:
			print("EXception caught : " +str(ex))

obj=Detect_CJ("http://192.168.250.1/dvwa")
obj.start()


