from bs4 import BeautifulSoup
import requests
import multiprocessing as mp
from selenium import webdriver
import time
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class Csrf_automate():
	def __init__(self,target,base):
		self.target=target
		self.base=base
		self.email="admin"
		self.password="password"
		self.target_links=["vulnerabilities/csrf/"]
		self.cookies=["RequestVerificationToken","token","csrfToken","csrftoken"]
		self.hidden=["__RequestVerificationToken","token","_csrfToken","_csrftoken"]

	def start(self):
		try:
			browser = webdriver.PhantomJS()
			browser.get(self.target)
			element_username=browser.find_element_by_name("username");
			element_username.clear()
			element_username.send_keys(self.email)
			element_username.click()
			element_password=browser.find_element_by_name("password");
			element_password.clear()
			element_password.send_keys(self.password)
			element_password.click()

			try:
				element_submit = WebDriverWait(browser, 2).until(
					EC.element_to_be_clickable((By.NAME, "Login"))
				)
				time. sleep(2)
				element_submit.click()
			except Exception as ee:
					print("Exception : "+str(ee))
					browser.quit()
			html = browser.page_source
			cookie={'domain':'192.168.250.1','name': 'security','value':'low',
			'path': '/dvwa/','httponly': False, 'secure': False}
			browser.add_cookie(cookie)
			all_cookies = browser.get_cookies()				
			soup = BeautifulSoup(html, "html.parser")
			anchor_tags=soup.find_all("a")
			browser.save_screenshot('screen.png')
			print("\n Saved Screen shot Post Login.Note the cookie values : ")
			found_form=False
			forms=[]
			for i,link in enumerate(anchor_tags):
				try:
					
					actuall_link=link.attrs["href"]
					actuall_link=actuall_link.replace("/.","/")
					if actuall_link in self.target_links:
						nav_url=str(self.target)+str(actuall_link)
						browser.get(nav_url)
						browser.save_screenshot("screen"+str(i)+".png")
						page_source=browser.page_source
						soup = BeautifulSoup(page_source, "html.parser")
						forms_=soup.find_all("form")
						submit_button=""
						
						all_cookies = browser.get_cookies()
						for no,form in enumerate(forms_) :
							anti_csrf=False
							inputs=form.find_all("input")
							for ip in inputs:
								if ip.attrs["type"] in ["hidden"]:
									hidden=browser.find_element_by_name(ip.attrs["name"]);
									if hidden in self.hidden:
										for c,v in all_cookies.iteritems():
											if c in self.cookies:
												anti_csrf=True
							if anti_csrf==False:
								forms.append({"url":nav_url,"form":str(form)})	
								browser.save_screenshot('csrf_'+str(no)+".png")	
				except Exception as ex:
					print("## Exception caught : " +str(ex))
			
			if len(forms):
				print("Discovered folowing Forms without CSRF protection : ")
				for form in forms:
					print("URL : "+str(form["url"])+"\n")
					print("Form : " +str(form["form"]))
					print("\n\n\n\n")

			print("\n\nSucessfully executed and SCreenshots Saved")
			
		except Exception as ex:
			print(str(ex))

obj=Csrf_automate("http://192.168.250.1/dvwa/","http://192.168.250.1/")
obj.start()
