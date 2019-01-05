from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import datetime

import time
class Automation :
	def __init__(self):
		self.browser=webdriver.Firefox();
		self.opt=''
		self.allocation_name=''
		self.allocation_details=''
		self.un=''
		self.lines=[]
		with open("input.txt","r+") as input:
			self.lines=input.readlines()
		
		self.email=str(self.lines[0])
		self.password=str((self.lines[1]))
		
		
	def automate(self):
		try:
			browser=self.browser
			browser.get('https://login.microsoftonline.com/paladionitsecurity.onmicrosoft.com/wsfed?wa=wsignin1.0&wtrealm=https%3a%2f%2fpaladionitsecurity.onmicrosoft.com%2fResourcePlanner&wctx=rm%3d0%26id%3dpassive%26ru%3d%252f&wct=2017-02-28T08%3a27%3a26Z#');
			element_username=browser.find_element_by_name("login");
			element_username.clear()
			element_username.send_keys(self.email)
			element_username.click()
			element_password=browser.find_element_by_name("passwd");
			element_password.clear()
			element_password.send_keys(self.password)
			element_password.click()
			try:
				element_submit = WebDriverWait(browser, 30).until(
					EC.element_to_be_clickable((By.ID, "cred_sign_in_button"))
				)
				print " Elemet submit found !! "
				time. sleep(5)
				element_submit.click()
			except Exception ,ee:
						print "Exception : "+str(ee)
						browser.quit()
			otp=raw_input("\n\n Enter OTP ")
			try:
				element_otp = WebDriverWait(browser, 30).until(
					EC.visibility_of_element_located((By.ID, "tfa_code_inputtext"))
				)
				element_otp.clear()
				element_otp.send_keys(otp)
			except Exception ,ee:
					print "Exception : "+str(ee)
					browser.quit()
			try:
				element_submit_ = WebDriverWait(browser, 30).until(
					EC.element_to_be_clickable((By.ID, "tfa_signin_button"))
				)
				element_submit_.click()
			except Exception ,ee:
						print "Exception : "+str(ee)
						browser.quit()
			try:
				WebDriverWait(browser, 30).until(EC.alert_is_present(),
											   'Timed out waiting for PA creation ' +
											   'confirmation popup to appear.')

				alert = browser.switch_to_alert()
				alert.accept()
				print "alert accepted"
			except TimeoutException:
				print "no alert"
			time.sleep(2)
			today=datetime.datetime.today().day
			
			rows=WebDriverWait(browser, 30).until(
					EC.visibility_of_element_located((By.CLASS_NAME, "fc-border-separate")))
			self.processed_rows=0
			self.processed_cols=0
			
			
			while True:
				try:
					return_val=self.create_magic(browser,rows)
					if return_val ==1:
						print "Obtained Return Value is : 1"
						break
					else:
						try:
							browser.refresh();
							rows=WebDriverWait(browser, 30).until(
								EC.visibility_of_element_located((By.CLASS_NAME, "fc-border-separate")))
							print "Located again Lets start @@@@"
						except Exception ,exx:
							print "Unable to load the UI in 30 seconds Exiting " +str(exx)
							break
				except Exception ,ex:
					print "Exception Stale " +str(ex)
					#.navigate().refersh();
					try:
						rows=WebDriverWait(browser, 30).until(
							EC.visibility_of_element_located((By.CLASS_NAME, "fc-border-separate")))
						print "Located again Lets start "
						ret_val=self.create_magic(browser,rows)
						print ret_val
					except Exception ,exx:
						print "Unable to load the UI in 30 seconds Exiting " +str(exx)
						
			
					
			
		except Exception ,excep:
			print "Caught exception :"+str(excep)
			
			
	def create_magic(self,browser,rows):
		print "Processed Rows are : "+str(self.processed_rows)
		print "Processed Cols are :" +str(self.processed_cols)
		today=datetime.datetime.today().day
		row_count=0;
		col_count=0;
		for row in rows.find_elements_by_tag_name('tr'):
			
			if 1:#row_count >= self.processed_rows :
				try:
					print "Row found for processing \n\n"
					time.sleep(2);
					cell = row.find_elements_by_tag_name("td")
					
					print "cell found \n\n "
					
					for c in cell :
						try :
								col_text=c.text
								col_count=int(c.text)
								
								print "Found cell : "+str(c.text)
								is_other = "other-month" in c.get_attribute("class")
								print "Obtained Other month for element cell :"+str(c.text) +"  " +str(is_other)
								if is_other :#and (col_count != 27 and col_count !=28):
									continue
								#fc-tue fc-widget-content fc-day2 fc-other-month
						except Exception ,exc:
								print "Exception while reading text looks gone :" +str(exc)
								return 0
						
						if col_count >= self.processed_cols :#or col_count==1 :
							
							if (int(col_text)) <= 100 :#or int (c.text)==27 or int (c.text)==28 :
								
								try:
									print(c.text)
									c.click()
									time.sleep(3)
								except Exception ,eex:
									print "Eelemnt seems to have gone : "+str(eex)
									return 0
								try:
									print "Attempting to browse elements in dialog :"
									dayType=Select(browser.find_element_by_name('dayType'))
									dayType.select_by_value("Working Day")
									activityType= Select(browser.find_element_by_name('activityType'))
									activityType.select_by_value("Offsite")
									timespent= Select(browser.find_element_by_name('timespent'))
									timespent.select_by_value("10")
									allocation=Select(browser.find_element_by_name('ProjectResourceId'))
									allocation.select_by_index(1)
									time_hours=Select(browser.find_element_by_id('TimeInHours'))
									time_hours.select_by_value("10")
									time_minutes=Select(browser.find_element_by_id('TimeInMinutes'))
									time_minutes.select_by_value("30")
									time_hours_out=Select(browser.find_element_by_id('TimeOutHours'))
									time_hours_out.select_by_value("8")
									time_minutes_out=Select(browser.find_element_by_id('TimeOutMinutes'))
									time_minutes_out.select_by_value("30")
									element_task=browser.find_element_by_name("task");
									element_task.clear()
									element_task.send_keys(str(self.lines[2]))
									element_description=browser.find_element_by_name("description")
									element_description.clear()
									element_description.send_keys(str(self.lines[3]))
									element_save=browser.find_element_by_id("Save")
									self.processed_cols=int(c.text)
									element_save.click()
									time.sleep(3)
									print "Clicked and closed"
								except Exception ,exc:
									print "Exception occured Col " +str(exc)
									print "If Open Making Attempt To close it "
									try:
										element_close=WebDriverWait(browser, 10).until(
										EC.visibility_of_element_located((By.CLASS_NAME,"ui-icon.ui-icon-closethick")))
										element_close.click()
										time.sleep(2)
									except Exception , ex:
										print "Close icon not found !! "+str(ex)
								
								
								
								#col_count=col_count+1
								
					print "Incrementing Row count "			
					self.processed_rows=self.processed_rows +1
					row_count  = row_count +1
					
				except Exception ,exc_row:
					print "Exception Row : "+str(exc_row)
					return 0
		
		return 1
		
		
obj=Automation()
obj.automate()