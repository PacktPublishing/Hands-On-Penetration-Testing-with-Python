#! /usr/bin/python3.5
import re
class RegularExpressions:
	def __init__(self,ip):
		self.input=ip
	def start(self,search_string,replace_str="@",replace=False):
		print("\n---------------------------------")
		print("Recievied Input : " +str(self.input))
		print("Searching and Matching for : " +str(search_string))			
		match_result=re.match(search_string,self.input,re.M|re.I|re.DOTALL)
		if match_result:
			print("Match results are (All group) : " +str(match_result.group()))
			print("Start index is :" +str(match_result.start()))
			print("End index is :" +str(match_result.end()))
		else:
			print("No match results found")
		search_result=re.search(search_string,self.input)
		if search_result:
			print("Search results are (All group)  : " +str(search_result.group()))
			print("Start index is :" +str(search_result.start()))
			print("End index is :" +str(search_result.end()))
		else:
			print("No Search results found")
		find_results=re.findall(search_string,self.input)
		if find_results:
			print("Find all List :")
			#for item in find_results:
			print("\t"+str(find_results))
		else:
			print("No Findall results found")
		if replace==True :
			sub_result=re.sub(search_string,replace_str,self.input)
			if sub_result:
				print("Sub results are : " +str(sub_result))
			else:
				print("No Sub  results found")
		print("----------------------------------------\n")

str1="Hello => (1) Python Regular Expressions. "
str2="(2) Enjoying Python to the fullest !"			
r=RegularExpressions(str1 + str2)
r.start("Hello")
r.start(r'\d')
r.start(r'(\D\d)+')
r.start(r'!$')
r.start(r'.*Reg')
r.start(r'^') 
r.start(r'[^0-9]+') 
r.start(r'[a-zA-Z]')
r.start("Python","Python3.5",True)
r.start(r'\D+',"#",True)
r.start(r'(\w+)') 

