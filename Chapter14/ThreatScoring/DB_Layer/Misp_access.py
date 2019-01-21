#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv
import itertools
import MySQLdb
import os
#import pymssql
import DB_Layer.Obs as Obs
import logging
from datetime import datetime as dt
import json
import time
from passlib.hash import pbkdf2_sha256
import datetime
from operator import itemgetter
import chardet


class MispDB():
	
	def __init__(self):
		self.log = logging.getLogger(__name__)

	def close_connection(self):
		try:
			if self.conn.open:
				self.conn.close()
		except Exception as ee:
			self.log.error("Exception occured while closing connection : "+str(ee))
	
	def init_connection(self):
		try:		
			user=''
			password=''
			host=''
			db=''
			self.folder_dir=os.path.dirname(os.path.realpath(__file__))
			try:				
				db_file=os.path.join(self.folder_dir,"db_file.txt")
				with open(db_file ,"r+") as db:	
					user_pass=db.read()
					user_pass=user_pass.replace("\n","").replace("\r\n","").replace("\r","")
					user_pass=user_pass.split("**##**")
					user=user_pass[0]
					password=Obs.decode(str(user_pass[1]))
					if type(password)!=type(str):
						password=password.decode("utf-8") 
					
					#print ("\n\nPassword is : "+str(password))
					host=user_pass[2]
					db=user_pass[3]
					
			except Exception as eex:
				self.log.error("Exception occured while Reading DB file : "+str(eex))

			self.conn=MySQLdb.connect(host,user,password,db)
			self.cursor = self.conn.cursor()
			self.cur=self.conn.cursor()

		except Exception as ee:
			print(str(ee))
			self.log.error("Exception occured in connection : "+str(ee))

	def getRole(self,user_key):
		
		try:
			#print ("User  key is : "+str(user_key))
			self.init_connection()	
			self.cur.execute("select name from roles where id in (select role_id from users where authkey = %s)",(str(user_key),))
			records=self.cur.fetchone()
			self.close_connection()
			if records :
				#print ("Pulled : " +str(records))
				return records[0]
			else:
				#print("In else !!")
				return 0

		except Exception as ee:
			self.log.error("Error in pulling the role data : "+str(ee))
			self.close_connection()
			return -1


	def getTasks(self):
		
		try:
			return_data={}
			return_data["status"]="success"
			record_list=[]
			self.init_connection()	
			self.cur.execute("select id,type,timer,scheduled_time ,process_id,description ,next_execution_time ,message from tasks")
			records=self.cur.fetchall()
			self.close_connection()
			put_date=True
			if records :
				for rec in records:
					if rec[1] =="threat_scoring":
						resp=self.getTaskid("threat_scoring")
						process_id=resp.get("process_id",343)
						last_run=PeriodicTask.objects.filter(id=int(process_id)).values_list('last_run_at',flat=True)[0]
						
						#print("Last run is : " +str(last_run))
						if last_run == None or last_run == " " or last_run == "":
								last_run=PeriodicTask.objects.filter(id=int(process_id)).values_list('date_changed',flat=True)[0]
								#last_run=str(datetime.datetime.now())[0:19]
								#put_date=False
								#print ("Now last run is : "+str(last_run))
						last_run=str(last_run)
						last_run=str(last_run[0:19])#2018-02-12 07:52:18.251207
						#print("Now Last run is : " +str(last_run))
						time_format = '%Y-%m-%d %H:%M:%S'
						date_delta= datetime.datetime.strptime(last_run, time_format)
						#print("Date Delta is : " +str(date_delta))
						#Note last run hours + 8 ,bacause the db time isutc 
						# and next run would be utc + 4
						date_delta+= datetime.timedelta(hours=int(rec[2])+4)
						#print("Now Date Delta is : " +str(date_delta))
						
						sc_tm=str(date_delta)[11:19]
						date_delta=str(date_delta)[0:10]
						#sc_tm=str(date_delta)
						#date_delta=int(time.mktime(date_delta.timetuple()))
						if put_date==False:
							date_delta=""
							sc_tm=""
						record_list.append({"id":rec[0],"type":rec[1],"timer":rec[2],"s_time":sc_tm,"p_id":rec[4],"desc":rec[5],"n_ex_tm":date_delta,"msg":rec[7]})
					else:
						record_list.append({"id":rec[0],"type":rec[1],"timer":rec[2],"s_time":rec[3],"p_id":rec[4],"desc":rec[5],"n_ex_tm":rec[6],"msg":rec[7]})
					
				return_data["value"]=record_list
			
				return return_data
			else:
				return_data["status"]="failure"
				return_data["error"]="empty"
				return_data["value"]="empty"
				return return_data

		except Exception as ee:
			self.log.error("Error in pulling the task data : "+str(ee))
			self.close_connection()
			return_data["status"]="failure"
			return_data["error"]=str(ee)
			return_data["value"]=str(ee)
			return return_data

	def getEnabledFeeds(self):
		try:
			return_data={}
			return_data["status"]="success"
			return_data["value"]={}
			self.init_connection()	
			self.cur.execute("select * from ((select count(id) from feeds) as t1,(select count(id) from feeds where enabled=1) as t2)")
			records=self.cur.fetchone()
			#print(str(records))
			self.close_connection()
			if records :
				return_data["value"]["total"]=int(records[0])
				return_data["value"]["enabled"]=int(records[1])				
			else:
				return_data["status"]="failure"
				return_data["error"]="empty"
				return_data["value"]="empty"

			return return_data
		except Exception as ee:
			self.log.error("Error in pulling the Feeds data : "+str(ee))
			self.close_connection()
			return_data["status"]="failure"
			return_data["error"]=str(ee)
			return_data["value"]=str(ee)
			return return_data

	def getTopUnique(self):
		try:
			return_data={}
			return_data["status"]="success"
			return_data["value"]=[]
			self.init_connection()	
			self.cur.execute("select count(id) from threat_scoring where comulative_score >=6;")
			records=self.cur.fetchone()
			if records:
				return_data["value"].append(int(records[0]))
			else:
				return_data["value"].append(0)

			self.cur.execute("select count(distinct(value1)) from attributes;")
			records=self.cur.fetchone()
			if records:
				return_data["value"].append(int(records[0]))
			else:
				return_data["value"].append(0)
			self.close_connection()

			return return_data
		except Exception as ee:
			self.log.error("Error in pulling the Feeds data : "+str(ee))
			self.close_connection()
			return_data["status"]="failure"
			return_data["error"]=str(ee)
			return_data["value"]=str(ee)
			return return_data
		


	def getSightings(self,attribute_id):
		try:
			return_data={}
			record_list=[]
			return_data["status"]="success"
			self.init_connection()	
			self.cur.execute("select id ,attribute_id , event_id , org_id , date_sighting , uuid ,source,type from sightings where attribute_id =%s",(int(attribute_id),))
			records=self.cur.fetchall()
			self.close_connection()
			if records :
				for rec in records:
					record_list.append({"id":rec[0],"attribute_id":rec[1],"event_id":rec[2],"org_id":rec[3],"date_sig":rec[4],"uuid":rec[5],"source":rec[6],"type":rec[7]})
				
				return_data["value"]=record_list
				return return_data	
				
			else:
				return_data["status"]="failure"
				return_data["error"]="empty"
				return_data["value"]="empty"
				return return_data

		except Exception as ee:
			self.log.error("Error in pulling the Sightings data : "+str(ee))
			self.close_connection()
			return_data["status"]="failure"
			return_data["error"]=str(ee)
			return_data["value"]=str(ee)
			return return_data

		
	def update_feeds(self,event_id):
		try:
			#print ("User  key is : "+str(user_key))
			self.init_connection()	
			self.cur.execute("update feeds set event_id = 0  where event_id = %s",(int(event_id),))
			self.conn.commit()
			self.close_connection()
			return 1

		except Exception as ee:
			self.log.error("Error in Updating : "+str(ee))
			self.close_connection()
			return -1	
	def getOrgs(self):
		try:
			return_data={}
			record_list=[]
			return_data["status"]="success"
			self.init_connection()	
			self.cur.execute("select id ,name,uuid from organisations")
			records=self.cur.fetchall()
			self.close_connection()
			if records :
				for rec in records:
					record_list.append({"id":rec[0],"name":rec[1],"uuid":rec[2]})
				
				return_data["value"]=record_list
				return return_data	
				
				#return return_data
			else:
				return_data["status"]="failure"
				return_data["error"]="empty"
				return_data["value"]="empty"
				return return_data

		except Exception as ee:
			self.log.error("Error in pulling the Org data : "+str(ee))
			self.close_connection()
			return_data["status"]="failure"
			return_data["error"]=str(ee)
			return_data["value"]=str(ee)
			return return_data


	#select events.id,email,users.org_id from events,users where events.user_id =users.id;

	

	def getAllCount(self):
		try:
			
			return_data={"ioc_count":0,"feed_count":0,"event_count":0}
			self.init_connection()	
			self.cur.execute("select count(id) from attributes where deleted=0")
			records=self.cur.fetchall()			
			if records :
				return_data["ioc_count"]=records[0][0]
			self.cur.execute("select count(id) from events")
			records=self.cur.fetchall()			
			if records :
				return_data["event_count"]=records[0][0]
			self.cur.execute("select count(id) from feeds")
			records=self.cur.fetchall()			
			if records :
				return_data["feed_count"]=records[0][0]
			
			self.cur.execute("select count(id) from users where disabled <> 1")
			records=self.cur.fetchall()			
			if records :
				return_data["user_count"]=records[0][0]


			self.cur.execute("select count(id) from organisations")
			records=self.cur.fetchall()			
			if records :
				return_data["org_count"]=records[0][0]


			self.cur.execute("select count(id) from servers")
			records=self.cur.fetchall()			
			if records :
				return_data["server_count"]=records[0][0]

			self.cur.execute("select count(id) from users")
			records=self.cur.fetchall()			
			if records :
				return_data["user_count"]=records[0][0]

			self.close_connection()
								
				
			return return_data	
				
			

		except Exception as ee:
			self.log.error("Error in pulling the Mapping data : "+str(ee))
			self.close_connection()
			return return_data

	def check_event(self,id):
		try:
			
			return_data={"ioc_count":0,"feed_count":0,"event_count":0}
			self.init_connection()	
			self.cur.execute("select count(id) from events where id = %s",(int(id),))
			records=self.cur.fetchall()			
			self.close_connection()
								
				
			return records[0][0]	
				
			

		except Exception as ee:
			self.log.error("Error in pulling event count : "+str(ee))
			self.close_connection()
			return 0

		


	def get_job_stats(self):
		try:
			
			return_data={"status":"success","value":{"completed_jobs":0,"processing_jobs":0}}
			self.init_connection()	
			self.cur.execute("select count(id) ,status,progress,substring(date_modified,1,10) from jobs where progress=100 or (progress > 0 and progress <100)  group by progress,substring(date_modified,1,10)")
			records=self.cur.fetchall()
			self.close_connection()
			for rec in records:
				if int(rec[2])==100:
					return_data["value"]["completed_jobs"]=return_data["value"]["completed_jobs"] + int(rec[0])
				elif int(rec[2]) < 100 and int(rec[2]) > 0:
					job_date=dt.strptime(str(rec[3]), "%Y-%m-%d")
					diff=dt.now()-job_date
					if (diff.days <= 1):
						return_data["value"]["processing_jobs"]=return_data["value"]["processing_jobs"] + int(rec[0])		
												
			return return_data
				
			

		except Exception as ee:
			self.log.error("Error in Pulling Job Stats : "+str(ee))
			self.close_connection()
			return_data["status"]="failure"
			return_data["error"]=str(ee)
			return_data["value"]=str(ee)
			return return_data

	def getEventUsersOrgs(self):
		try:
			
			return_data={}
			mapping_org_ioc=[]
			self.init_connection()	
			self.cur.execute("select events.id,email,users.org_id,events.attribute_count from events,users where events.user_id =users.id")
			records=self.cur.fetchall()
			self.close_connection()
			if records :
				for rec in records:
					return_data[rec[0]]={"email":rec[1],"org_id":rec[2],"ioc_count":rec[3]}	
				self.init_connection()	
				self.cur.execute("select sum(events.attribute_count),count(events.id) ,organisations.name from events,organisations where events.orgc_id=organisations.id group by organisations.id")
				records=self.cur.fetchall()
				if records:
					for rec in records:
						mapping_org_ioc.append({"org_name":rec[2],"event_count":rec[1],"ioc_count":rec[0]})
				return_data["org_ioc_event_mapping"]=mapping_org_ioc
				self.close_connection()			
				
				return return_data	
				
				#return return_data
			else:
				
				return return_data

		except Exception as ee:
			self.log.error("Error in pulling the Mapping data : "+str(ee))
			self.close_connection()
			return return_data

	def getAttributeSightings(self,event_id):
		try:
			
			return_data={}
			self.init_connection()	
			self.cur.execute("select sightings.id,attribute_id,event_id,organisations.name ,date_sighting,sightings.type from sightings,organisations where event_id=%s and organisations.id=org_id",(event_id,))
			records=self.cur.fetchall()
			att_ids=[]
			#self.close_connection()
			if records :
				for rec in records:
					return_data[rec[0]]={"att_id":rec[1],"event_id":rec[2],"org_name":rec[3],"date":rec[4],"type":rec[5]}					
					att_ids.append(rec[1])
				for id in att_ids:
					self.cur.execute("select type,count(type) from sightings  where attribute_id = %s group by type",(id,))
					recc=self.cur.fetchall()
					return_data["sighting_count"]={}
					return_data["sighting_count"][id]={}
					for r in recc:
						return_data["sighting_count"][id].update({r[0]:r[1]})
						
				self.close_connection()
				
				return return_data	
				
				#return return_data
			else:
				self.close_connection()
				
				return return_data

		except Exception as ee:
			self.log.error("Error in pulling the att sightings data : "+str(ee))
			self.close_connection()
			return return_data
	

	def getAttributeTags_(self,attribute_id,con_open=False):
		try:
			
			return_data=[]
			if con_open ==False:
				self.init_connection()	
			self.cur.execute("select attribute_id as id,tag_id as tag_id ,name,colour from attribute_tags,tags where attribute_id=%s and tag_id=tags.id",(attribute_id,))
			records=self.cur.fetchall()
			if con_open ==False:
				self.close_connection()
			if records :
				for rec in records:
					return_data.append({"id":rec[1],"name":rec[2],"colour":rec[3]})			
				
				return return_data	
				
				
			else:
				
				return return_data

		except Exception as ee:
			self.log.error("Error in pulling the Tag __ data : "+str(ee))
			if con_open == False:
				self.close_connection()
			return return_data


	def getAttributeTags(self,event_id):
		try:
			
			return_data={}
			self.init_connection()	
			self.cur.execute("select attribute_id as id,tag_id as tag_id ,name,colour from attribute_tags,tags where event_id=%s and tag_id=tags.id",(event_id,))
			records=self.cur.fetchall()
			self.close_connection()
			if records :
				for rec in records:
					return_data[rec[0]]={"tag_id":rec[1],"tag_name":rec[2],"tag_color":rec[3]}				
				
				return return_data	
				
				#return return_data
			else:
				
				return return_data

		except Exception as ee:
			self.log.error(" 1 Error in pulling the Tag data : "+str(ee))
			self.close_connection()
			return return_data

	def getShadowAttributeDetails(self,id):
		try:
			return_data={}
			
			self.init_connection()	
			self.cur.execute("select email from shadow_attributes where id =%s",(int(id),))
			record=self.cur.fetchone()
			self.close_connection()
			return_data["status"]="success"
			return_data["value"]=record[0]
			return return_data

		except Exception as ee:
			self.log.error("Error in pulling the shadow att data : "+str(ee))
			self.close_connection()
			return_data["status"]="failure"
			return_data["value"]=str(ee)
			return_data["error"]=str(ee)
			return return_data

	def getEventTags(self,event_id,proper_name=False):
		try:
			
			return_data=[]
			self.init_connection()	
			self.cur.execute("select event_id as id,tag_id as tag_id ,name,colour from event_tags,tags where event_id=%s and tag_id=tags.id",(event_id,))
			records=self.cur.fetchall()
			self.close_connection()
			if records :
				for rec in records:
					if proper_name == False:
						return_data.append({"tag_id":rec[1],"tag_name":rec[2],"tag_color":rec[3]})
					else:
						return_data.append({"Tag":{"id":rec[1],"name":rec[2],"colour":rec[3]}})				
				
				return return_data	
				
				#return return_data
			else:
				
				return return_data

		except Exception as ee:
			self.log.error("2 Error in pulling the Tag data : "+str(ee))
			self.close_connection()
			return return_data



	def getTags(self):
		try:
			
			return_data=[]
			self.init_connection()	
			self.cur.execute("select id,name,colour,org_id from tags")
			records=self.cur.fetchall()
			self.close_connection()
			if records :
				for rec in records:
					return_data.append({"id":rec[0],"name":rec[1],"color":rec[2],"org_id":rec[3]})			
				
				return return_data	
				
				#return return_data
			else:
				
				return return_data

		except Exception as ee:
			self.log.error("3 Error in pulling the Tag data : "+str(ee))
			self.close_connection()
			return return_data

	def register_user(self,user_id,username,password,email,auth_key='',role_id=3):
		try:
			return_data={}
			my_hash = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
			password=my_hash
			
			self.init_connection()	
			self.cur.execute("insert into local_users (user_id,username,password,email,auth_key,role_id) values(%s,%s,%s,%s,%s,%s)",(user_id,username,password,email,auth_key,role_id))
			self.conn.commit()
			self.close_connection()
			return_data["status"]="success"
			return_data["value"]="Inserted Successfully"
			return return_data
			
		except Exception as exc :
			#print("Exception while reg locally : " +str(exc))
			self.conn.rollback()
			self.close_connection()
			return_data["status"]="failure"
			return_data["value"]=str(exc)	
			return return_data

	def update_password(self,password,email):
		try:
			return_data={}
			ret_bal=0
			if password != None:
				my_hash = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
				password=my_hash
				mysql_cmd="update local_users set password=%s where email=%s"
				value_tuple=(password,email)
				self.init_connection()	
				self.cur.execute(mysql_cmd,value_tuple)
				ret_val=self.cur.rowcount
				self.conn.commit()
				self.close_connection()
				if ret_val :
					return_data["status"]="success"
					return_data["value"]="Updated Successfully"	
					return return_data
				else:
					return_data["status"]="failure"
					return_data["value"]="Check Username/email ,no record found."	
					return_data["error"]="Check Username/email ,no record found."
					return return_data
			else:
				return_data["status"]="failure"
				return_data["value"]="Update failed-Password None"
				return_data["error"]="Update failed-Password None"	
				return return_data
				
			
			
			
			return return_data
			
		except Exception as exc :
			#print(str(exc))
			self.conn.rollback()
			self.close_connection()
			return_data["status"]="failure"
			return_data["value"]=str(exc)	
			return return_data

	def update_user(self,user_id,username,password,email,auth_key,role_id):
		try:
			return_data={}
			if password != None:
				my_hash = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
				password=my_hash
				mysql_cmd="update local_users set username=%s,password=%s,email=%s,auth_key=%s,role_id=%s where user_id=%s"
				value_tuple=(username,password,email,auth_key,role_id,user_id)
			else:
				
				mysql_cmd="update local_users set username=%s,email=%s,auth_key=%s,role_id=%s where user_id=%s"
				value_tuple=(username,email,auth_key,role_id,user_id)
			
			self.init_connection()	
			self.cur.execute(mysql_cmd,value_tuple)
			self.conn.commit()
			self.close_connection()
			return_data["status"]="success"
			return_data["value"]="Updated Successfully"
			#print("Returning : " +str(return_data))
			return return_data
			
		except Exception as exc :
			print(str(exc))
			self.conn.rollback()
			self.close_connection()
			return_data["status"]="failure"
			return_data["value"]=str(exc)	
			return return_data

	def delete_user(self,user_id):
		try:
			return_data={}
			self.init_connection()	
			self.cur.execute("delete from users where id =%s",(int(user_id),))
			self.conn.commit()
			self.close_connection()
			return_data["status"]="success"
			return_data["value"]="Deleted Successfully"
			return return_data
			
		except Exception as exc :
			self.conn.rollback()
			self.close_connection()
			return_data["status"]="failure"
			return_data["value"]=str(exc)	
			return return_data

	def delete_local_user(self,user_id):
		try:
			return_data={}
			self.init_connection()	
			self.cur.execute("delete from local_users where user_id =%s",(int(user_id),))
			self.conn.commit()
			self.close_connection()
			return_data["status"]="success"
			return_data["value"]="Deleted Successfully"
			return return_data
			
		except Exception as exc :
			self.conn.rollback()
			self.close_connection()
			return_data["status"]="failure"
			return_data["value"]=str(exc)	
			return return_data


	def Authenticate(self,username,password):
		try:
			
			return_data={}
			#print(username)
			self.init_connection()	
			self.cur.execute("select password from local_users where username = %s or email =%s",(username,username))
			record=self.cur.fetchone()
			self.close_connection()
			if record :
				actual_hash=record[0]
				return_data["status"]="success"
			
				return_data["value"]= pbkdf2_sha256.verify(password, actual_hash)
				#print("AUTH Failed")	
				
				
			else:
				return_data["status"]="failure"
				return_data["value"]= False
				return_data["error"]="No record found"
				print("No records")
			return return_data

		except Exception as ee:
			self.log.error("Error in pulling the Authentication data : "+str(ee))
			self.close_connection()
			return_data["status"]="failure"
			return_data["value"]= False
			return_data["error"]=str(ee)
			return return_data

	

	def generate_graph(self,event_id):
		try:
			"""
			{"name":"TorrentLocker","type":"attribute","id":"605957","att_category":"Payload delivery","att_type":"text","image":"/img/indicator.png","att_ids":false,"comment":"RANSOMWARE_TRACKER_DOMAIN_TL_1"},{"name":"(4793) OSINT 2017-11-06 - 2017-11-06T1...","type":"event","id":"4793","expanded":0,"image":"/img/orgs/MISP.png","info":"OSINT 2017-11-06 - 2017-11-06T13:59:05.291088 - 2017-11-06T14:29:05.291088","org":"inThreat","analysis":"Completed","date":"2017-11-06"}
			"""
			return_data={}
			return_data={"nodes":[],"links":[]}
			record_list=[]
			result_data=[]
			etc_details={}
			node_counter=0
			self.init_connection()	
			lower_upper_bond=20
			upper_bond=60
			intermediate_upper_bond=40
			#or (e.id=%s and e.orgc_id=o.id)
			self.cur.execute("select e.id,'event',e.id,'1','image',e.info,o.name,e.analysis,e.date from events e , organisations o where e.id=%s and e.orgc_id=o.id ",(int(event_id),))
			events=self.cur.fetchall()
			for event in events:
				#print ("Pushing Event Parent\n\n")
				return_data["nodes"].append({"name":"("+str(event[0])+") "+str(event[5][0:22])+"...","type":event[1],"id":event[2],"expanded":event[3],"image":event[4],"info":event[5],"org":event[6],"analysis":event[7],"date":event[8]})
			
			self.cur.execute("select e.id,'event',e.id,'0','image',e.info,o.name,e.analysis,e.date from events e , organisations o where (e.orgc_id=o.id and e.id in (select distinct 1_event_id from correlations where event_id=%s)) ",(int(event_id),))
			events=self.cur.fetchall()
			current_limit=len(events)
			#print(current_limit)
			max_att=10
			if current_limit > upper_bond:
				max_att=2
			elif current_limit > intermediate_upper_bond:
				max_att=3
			elif current_limit > lower_upper_bond:
				max_att=4
			else:
				max_att=10
			
			for event in events[0:50]:
				
				return_data["nodes"].append({"name":"("+str(event[0])+") "+str(event[5][0:22])+"...","type":event[1],"id":event[2],"expanded":event[3],"image":event[4],"info":event[5],"org":event[6],"analysis":event[7],"date":event[8]})
				event_index=len(return_data["nodes"]) -1
				
				thrash_hold=0
				
				self.cur.execute("select c.value ,'attribute',c.attribute_id ,a.category,a.type,'image',a.to_ids,a.comment from correlations c,attributes a where c.event_id=%s and c.1_event_id =%s  and c.attribute_id=a.id",(int(event_id),int(event[0])))				
				all_data=self.cur.fetchall()
				etc_details[event_index]=[]
				etc_att=[]
				for data in all_data:
					
					if thrash_hold < max_att :
						
						#print("Now pushing attributes")
						return_data["nodes"].append({"name":data[0],"type":data[1],"id":data[2],"att_category":data[3],"att_type":data[4],"image":data[5],"att_ids":data[6],"comment":data[7]})
						att_index=len(return_data["nodes"]) -1
						return_data["links"].append({"source":0,"target":att_index})
						
						return_data["links"].append({"source":att_index,"target":event_index})
						
						
						
					else:
						etc_details[event_index].append({"name":data[0],"type":data[1],"id":data[2],"att_category":data[3],"att_type":data[4],"image":data[5],"att_ids":data[6],"comment":data[7]})
						etc_att.append({"name":data[0],"id":data[2]})

					thrash_hold=thrash_hold +1 
				if len(etc_att):
					return_data["nodes"][event_index].update({"is_etc":True,"etc_details":etc_att})

			self.close_connection()
			return_data["extra_data"]=etc_details
			#print("\n\n "+str(return_data))
			return return_data
					
						
					
					

		except Exception as ee :
			self.log.error("Error in pulling the graph data : "+str(ee))
			self.close_connection()
			return_data["status"]="failure"
			return_data["error"]=str(ee)
			return_data["value"]=str(ee)
			return return_data

	def CustomSearch(self,att_val):
		try:
			return_data={}
			return_data["Attribute"]=[]
			self.init_connection()
			self.cur.execute("select a.id,event_id,category,type,value1,to_ids,uuid,timestamp,distribution,sharing_group_id,comment,comulative_score,updated_comulative_score,i_tag_score,i_date_score,i_corelation_score,i_comment_score from attributes a left  join threat_scoring on a.id=threat_scoring.attribute_id where (value1=%s) and deleted <> 1 order by comulative_score desc limit 1",(str(att_val),))
			attributes=self.cur.fetchall()
			exact=False
			for att in attributes:
				return_data["Attribute"].append({"id":att[0],"type":att[3],"category":att[2],"to_ids":att[5],"uuid":att[6],"event_id":att[1],"distribution":att[8],"timestamp":att[7],"comment":att[10],"sharing_group_id":att[9],"deleted":False,"value":att[4],"Tag":self.getAttributeTags_(att[0],True),"ts":att[11],"uts":att[12],"i_tag_score":att[13],"i_date_score":att[14],"i_corelation_score":att[15],"i_comment_score":att[16],"exact":True })
				exact=True

			self.cur.execute("select a.id,event_id,category,type,value1,to_ids,uuid,timestamp,distribution,sharing_group_id,comment,comulative_score,updated_comulative_score,i_tag_score,i_date_score,i_corelation_score,i_comment_score from attributes a left  join threat_scoring on a.id=threat_scoring.attribute_id where (value1 <> %s and value1 like %s) and deleted <> 1 order by comulative_score desc",(str(att_val),"%"+str(att_val)+"%"))

			attributes=self.cur.fetchall()
			approx=0
			approx_v=False
			for att in attributes:
				
				if approx == 0 and exact == False:
					approx_v=True
				else:
					approx_v=False
				approx=approx +1 

				return_data["Attribute"].append({"id":att[0],"type":att[3],"category":att[2],"to_ids":att[5],"uuid":att[6],"event_id":att[1],"distribution":att[8],"timestamp":att[7],"comment":att[10],"sharing_group_id":att[9],"deleted":False,"value":att[4],"Tag":self.getAttributeTags_(att[0],True),"ts":att[11],"uts":att[12],"i_tag_score":att[13],"i_date_score":att[14],"i_corelation_score":att[15],"i_comment_score":att[16],"approx":approx_v})
			
			
			self.close_connection()
			#return_data["Attribute"] = sorted(return_data["Attribute"], key=itemgetter("ts"), reverse=True)
			return return_data
		except Exception as ee:
			self.log.error("Error in pulling the Custom search data : "+str(ee))
			self.close_connection()
			return_data["status"]="failure"
			return_data["error"]=str(ee)
			return_data["value"]=str(ee)
			return return_data

	def SearchAttributes(self,param="tags",search="",offset=0,limit=200):
		try:
			return_data={}
			return_data["Attribute"]=[]
			if param =="org":
				sql_query="select a.id,event_id,category,type,value1,to_ids,uuid,timestamp,distribution,sharing_group_id,comulative_score,updated_comulative_score,i_tag_score,i_date_score,i_corelation_score,i_comment_score from attributes a left  join threat_scoring on a.id=threat_scoring.attribute_id where event_id in (select id from events where  org_id or orgc_id in (select id from organisations where name = %s)) order by comulative_score desc limit "+str(limit)+" offset "+str(offset)
				sql_query_count="select count(id) from attributes where event_id in (select id from events where  org_id or orgc_id in (select id from organisations where name = %s))"

			elif param == "type_attribute":
				sql_query="select a.id,event_id,category,type,value1,to_ids,uuid,timestamp,distribution,sharing_group_id,comment,comulative_score,updated_comulative_score,i_tag_score,i_date_score,i_corelation_score,i_comment_score from attributes a left  join threat_scoring on a.id=threat_scoring.attribute_id  where type = %s order by comulative_score desc  limit "+str(limit)+" offset "+str(offset)
				sql_query_count="select count(id) from attributes  where type = %s"

			elif param == "category" :
				sql_query="select a.id,event_id,category,type,value1,to_ids,uuid,timestamp,distribution,sharing_group_id,comment,comulative_score,updated_comulative_score,i_tag_score,i_date_score,i_corelation_score,i_comment_score from attributes a left  join threat_scoring on a.id=threat_scoring.attribute_id  where category = %s order by comulative_score desc  limit "+str(limit)+" offset "+str(offset)
				sql_query_count="select count(id) from attributes  where category = %s"

			elif param =="tags":
				sql_query="select a.id,event_id,category,type,value1,to_ids,uuid,timestamp,distribution,sharing_group_id,comment ,comulative_score,updated_comulative_score,i_tag_score,i_date_score,i_corelation_score,i_comment_score from attributes a left  join threat_scoring on a.id=threat_scoring.attribute_id where a.id in (select distinct attribute_id from attribute_tags where tag_id = %s ) order by comulative_score desc  limit "+str(limit)+" offset "+str(offset)
				sql_query_count="select count(id) from attributes where id in (select distinct attribute_id from attribute_tags where tag_id = %s )"
				#print(sql_query)

			elif param =="withAttachments":
				
				sql_query="select a.id,event_id,category,type,value1,to_ids,uuid,timestamp,distribution,sharing_group_id,comment,comulative_score,updated_comulative_score,i_tag_score,i_date_score,i_corelation_score,i_comment_score from attributes a left  join threat_scoring on a.id=threat_scoring.attribute_id where type = %s order by comulative_score desc  limit "+str(limit)+" offset "+str(offset)
				search='attachment'
				sql_query_count="select count(id) from attributes where type = %s"
				#print(sql_query)
			
			elif param =="date_to":
				date_to = search +" 00:00:00"
				pattern = '%Y-%m-%d %H:%M:%S'
				epoch = int(time.mktime(time.strptime(date_to, pattern)))
				#print ("Epoch is : " +str(epoch))

				sql_query="select a.id,event_id,category,type,value1,to_ids,uuid,timestamp,distribution,sharing_group_id,comment ,comulative_score,updated_comulative_score,i_tag_score,i_date_score,i_corelation_score,i_comment_score from attributes a left  join threat_scoring on a.id=threat_scoring.attribute_id where timestamp <= %s order by comulative_score desc  limit "+str(limit)+" offset "+str(offset)
				search=int(epoch)
				sql_query_count="select count(id) from attributes where timestamp <= %s "
				
			elif param =="date_from":
				date_from = search +" 00:00:00"
				pattern = '%Y-%m-%d %H:%M:%S'
				epoch = int(time.mktime(time.strptime(date_from, pattern)))
				#print ("Epoch is : " +str(epoch))
				sql_query="select a.id,event_id,category,type,value1,to_ids,uuid,timestamp,distribution,sharing_group_id,comment,comulative_score,updated_comulative_score,i_tag_score,i_date_score,i_corelation_score,i_comment_score from attributes a left  join threat_scoring on a.id=threat_scoring.attribute_id where timestamp >= %s order by comulative_score desc  limit "+str(limit)+" offset "+str(offset) 
				search=int(epoch)
				sql_query_count="select count(id) from attributes where timestamp >= %s "
			elif param =="date_exact":
				#print(11)
				date_exact = search +" 00:00:00"
				pattern = '%Y-%m-%d %H:%M:%S'
				epoch = int(time.mktime(time.strptime(date_exact, pattern)))
				search_end=search.split("-")
				#print(epoch)
				#print("End search is :"+str(search_end))
				search_end=search_end[0]+"-"+search_end[1]+"-"+str(int(search_end[2])+1)
				date_end=search +" 20:00:00" #Keep 4 hour difference into picture .Exact date would be timestamp -4 (ts is as per UTC)
				#print("end date : " +date_end)
				epoch_end=int(time.mktime(time.strptime(date_end, pattern)))
				#print ("Epoch is : " +str(epoch))
				sql_query="select a.id,event_id,category,type,value1,to_ids,uuid,timestamp,distribution,sharing_group_id,comment ,comulative_score,updated_comulative_score,i_tag_score,i_date_score,i_corelation_score,i_comment_score from attributes a left  join threat_scoring on a.id=threat_scoring.attribute_id where timestamp >= %s and timestamp < "+str(epoch_end)+" order by comulative_score desc  limit "+str(limit)+" offset "+str(offset) 
				search=int(epoch)
				#print(sql_query)
				sql_query_count="select count(id) from attributes where timestamp >= %s and timestamp < "+str(epoch_end)
 			
			elif param =="published":
				sql_query="select a.id,event_id,category,type,value1,to_ids,uuid,timestamp,distribution,sharing_group_id,comment ,comulative_score,updated_comulative_score,i_tag_score,i_date_score,i_corelation_score,i_comment_score from attributes a left  join threat_scoring on a.id=threat_scoring.attribute_id where event_id in (select id from events where published = %s) order by comulative_score desc  limit "+str(limit)+" offset "+str(offset)
				sql_query_count="select count(id) from attributes where event_id in (select id from events where published = %s)"

			elif param =="to_ids":
				sql_query="select a.id,event_id,category,type,value1,to_ids,uuid,timestamp,distribution,sharing_group_id,comment ,comulative_score,updated_comulative_score,i_tag_score,i_date_score,i_corelation_score,i_comment_score from attributes a left  join threat_scoring on a.id=threat_scoring.attribute_id where to_ids = %s order by comulative_score desc  limit "+str(limit)+" offset "+str(offset)
				sql_query_count="select count(id) from attributes where to_ids = %s"

			else:
				return_data={}
				return_data["status"]="failure"
				return_data["error"]="Invalid Search String"
				return_data["value"]="Invalid Search String"
				return return_data

			#return_data["Attribute"]=[]
			self.init_connection()
			self.cur.execute(sql_query,(search,))
			attributes=self.cur.fetchall()
			for att in attributes:
				my_dict={}
				my_dict={"id":att[0],"type":att[3],"category":att[2],"to_ids":att[5],"uuid":att[6],"event_id":att[1],"distribution":str(att[8]),"timestamp":att[7],"comment":att[10],"sharing_group_id":att[9],"deleted":False,"value":att[4],"Tag":self.getAttributeTags_(att[0],True),"ts":att[11],"uts":att[12],"i_tag_score":att[13],"i_date_score":att[14],"i_corelation_score":att[15],"i_comment_score":att[16]}
				return_data["Attribute"].append(my_dict)
			
			self.cur.execute(sql_query_count,(search,))
			count=self.cur.fetchone()
			#print("count is : " +str(count))
			if len(count):
				count_val=count[0]
			else:
				count_val=0
			return_data["counter"]=count_val
			self.close_connection()
			
			return return_data
		except Exception as ee:
			self.log.error("Error in pulling the Custom search data Attributes : "+str(ee))
			self.close_connection()
			return_data={}
			return_data["status"]="failure"
			return_data["error"]=str(ee)
			return_data["value"]=str(ee)
			return return_data

	def SearchEvents(self,param="tags",search="",offset=0,limit=200):
		try:
			return_data=[]
			many_count=False
		
			if param =="org":
				sql_query="select id,orgc_id,org_id,date,threat_level_id,info,published,uuid,attribute_count,publish_timestamp,sharing_group_id,disable_correlation,user_id, distribution,analysis from events where org_id or orgc_id in (select id from organisations where name = %s) order by id desc limit "+str(limit)+" offset "+str(offset)
				sql_query_count="select count(id) from events where org_id or orgc_id in (select id from organisations where name = %s)"

			elif param == "type_attribute":
				sql_query="select id,orgc_id,org_id,date,threat_level_id,info,published,uuid,attribute_count,publish_timestamp,sharing_group_id,disable_correlation,user_id ,distribution,analysis from events where id in (select distinct event_id from attributes where type = %s) order by id desc limit "+str(limit)+" offset "+str(offset)
				sql_query_count="select count(id) from events where id in (select distinct event_id from attributes where type = %s)"

			elif param == "category" :
				sql_query="select id,orgc_id,org_id,date,threat_level_id,info,published,uuid,attribute_count,publish_timestamp,sharing_group_id,disable_correlation,user_id , distribution,analysis from events where id in (select distinct event_id from attributes where category = %s) order by id desc limit "+str(limit)+" offset "+str(offset)
				sql_query_count="select count(id) from events where id in (select distinct event_id from attributes where category = %s)"

			elif param =="tags":
				sql_query="select id,orgc_id,org_id,date,threat_level_id,info,published,uuid,attribute_count,publish_timestamp,sharing_group_id,disable_correlation,user_id, distribution,analysis  from events where id in (select distinct event_id from event_tags where tag_id = %s ) order by id desc limit "+str(limit)+" offset "+str(offset)
				sql_query_count="select count(id) from events where id in (select distinct event_id from event_tags where tag_id = %s)"
				#print(sql_query)
				

			elif param =="withAttachments":
				sql_query="select id,orgc_id,org_id,date,threat_level_id,info,published,uuid,attribute_count,publish_timestamp,sharing_group_id,disable_correlation,user_id,distribution,analysis  from events where id in (select distinct event_id from attributes where type = %s) order by id desc limit "+str(limit)+" offset "+str(offset)
				search='attachment'
				sql_query_count="select count(id) from events where id in (select distinct event_id from attributes where type = %s)"
				
				
				
			
			elif param =="date_to":
				sql_query="select id,orgc_id,org_id,date,threat_level_id,info,published,uuid,attribute_count,publish_timestamp,sharing_group_id,disable_correlation,user_id,distribution,analysis from events where date <= %s order by id desc limit "+str(limit)+" offset "+str(offset)
				sql_query_count="select count(id) from events where date <= %s"
				
			elif param =="date_from":
				sql_query="select id,orgc_id,org_id,date,threat_level_id,info,published,uuid,attribute_count,publish_timestamp,sharing_group_id,disable_correlation,user_id ,distribution,analysis from events where date >= %s order by id desc limit "+str(limit)+" offset "+str(offset)  
				sql_query_count="select count(id) from events where date >= %s"

			elif param =="date_exact":
				sql_query="select id,orgc_id,org_id,date,threat_level_id,info,published,uuid,attribute_count,publish_timestamp,sharing_group_id,disable_correlation,user_id ,distribution,analysis from events where date = %s  order by id desc limit "+str(limit)+" offset "+str(offset)  
				sql_query_count="select count(id) from events where date = %s"
 
			elif param =="published":
				sql_query="select id,orgc_id,org_id,date,threat_level_id,info,published,uuid,attribute_count,publish_timestamp,sharing_group_id,disable_correlation,user_id,distribution,analysis  from events where published = %s order by id desc limit "+str(limit)+" offset "+str(offset)
				sql_query_count="select count(id) from events where published = %s"

			elif param =="to_ids":
				sql_query="select id,orgc_id,org_id,date,threat_level_id,info,published,uuid,attribute_count,publish_timestamp,sharing_group_id,disable_correlation,user_id ,distribution,analysis from events where id in (select distinct event_id from attributes where to_ids = %s ) order by id desc limit "+str(limit)+" offset "+str(offset)
				sql_query_count="select count(id) from events where id in (select distinct event_id from attributes where to_ids = %s)"
			elif param == "all":
				sql_query="select e.id,e.orgc_id,e.org_id,e.date,e.threat_level_id,e.info,e.published,e.uuid,e.attribute_count,e.publish_timestamp,e.sharing_group_id,e.disable_correlation, u.email ,e.distribution,e.analysis from events e, users u  where e.id <> %s and e.user_id=u.id order by id desc limit "+str(limit)+" offset "+str(offset)
				sql_query_count="select count(id) from events where id <> %s"
				search=0
				#print (sql_query)

			elif param == "ioc":
				sql_query="select e.id,e.orgc_id,e.org_id,e.date,e.threat_level_id,e.info,e.published,e.uuid,e.attribute_count,e.publish_timestamp,e.sharing_group_id,e.disable_correlation, u.email ,e.distribution,e.analysis from events e, users u  where e.id = (select event_id from attributes where id = %s) and e.user_id=u.id order by id desc limit "+str(limit)+" offset "+str(offset)
				sql_query_count="select email from shadow_attributes where old_id =%s"
				many_count=True
				
				#print (sql_query)

			else:
				return_data={}
				return_data["status"]="failure"
				return_data["error"]="Invalid Search String"
				return_data["value"]="Invalid Search String"
				return return_data

			self.init_connection()
			self.cur.execute(sql_query,(search,))
			events=self.cur.fetchall()
			self.close_connection()
			org_data=self.getOrgs()
			orgs=[]
			if org_data["status"]=="success":
				orgs=org_data["value"]
			
			for ev in events:
				my_dict={}
				my_dict["Event"]={"id":ev[0],"orgc_id":ev[1],"org_id":ev[2],"date":ev[3],"threat_level_id":str(ev[4]),"info":ev[5],"published":ev[6],"uuid":ev[7],"attribute_count":ev[8],"publish_timestamp":ev[9],"sharing_group_id":ev[10],"disable_correlation":ev[11],"distribution":str(ev[13]),"analysis":str(ev[14])}
				try:
					my_dict["Event"].update({"email":ev[12]})
				except Exception as eee:
					#print("Exception : !" +str(eee))
					pass
			
				#print("Normal resume")
				if len(orgs):
					my_dict["Event"].update({"Org":org for org in orgs if org["id"]==ev[2]})
					my_dict["Event"].update({"Orgc":org for org in orgs if org["id"]==ev[1]})
				
				my_dict["Event"]["EventTag"]=[]
				try:
					tags=self.getEventTags(int(ev[0]),True)
				except Exception as ew:
					tags=[]
				
				my_dict["Event"]["EventTag"]=tags
				#print("Tags are : " +str(my_dict["Event"]["EventTag"]))
				if param != "all":
					return_data.append(my_dict)
				else:
					ev_dict=my_dict["Event"]
					return_data.append(ev_dict)
			
			self.init_connection()
			self.cur.execute(sql_query_count,(search,))
			if many_count ==False:
				count=self.cur.fetchone()
			else:
				count=self.cur.fetchall()
			self.close_connection()
			#print("count is : " +str(count))
			if len(count):
				if many_count ==False:
					count_val=count[0]
				else:
					my_list=[]
					my_list=[c[0] for c in count]
					count_val=my_list
				
			else:
				count_val=0
			
			resp_data={}
			
			resp_data["counter"]=count_val	
			resp_data["events"]=return_data
			
			return resp_data
			

		except Exception as ee:
			#print("Exception : "+str(ee))
			self.log.error("Error in pulling the Custom search data Events : "+str(ee))
			self.close_connection()
			return_data={}
			return_data["status"]="failure"
			return_data["error"]=str(ee)
			return_data["value"]=str(ee)
			return return_data

	def getServer(self,server_id):	
		try:
			return_data={}
			return_data["status"]="success"
			record_list=[]
			self.init_connection()	
			self.cur.execute("select id,name,url,org_id,push,pull,organization,remote_org_id,publish_without_email,unpublish_event,self_signed,pull_rules,push_rules,cert_file,client_cert_file ,authkey,internal from servers where id =%s",(int(server_id),))
			records=self.cur.fetchall()
			self.close_connection()
			org_data=self.getOrgs()
			orgs=[]
			if org_data["status"]=="success":
				orgs=org_data["value"]
				
			if records :
				for rec in records:
					my_dict={"id":rec[0],"name":rec[1],"url":rec[2],"org_id":rec[3],"push":rec[4],"pull":rec[5],"organization":rec[6],"remote_org_id":rec[7],"publish_without_email":rec[8],"unpublish_event":rec[9],"self_signed":rec[10],"pull_rules":rec[11],"push_rules":rec[12],"cert_file":rec[13],"cert_file_client":rec[14],"authkey":rec[15],"internal":rec[16]}
					
					if len(orgs):
						#print ("Org id : "+str(orgs[0]["id"]) +"  Id other " +str(rec[8]))
						my_dict.update({"org":org for org in orgs if org["id"]==rec[3]})
					
					record_list.append(my_dict)
					
				return_data["value"]=record_list[0]
				return return_data
			else:
				return_data["status"]="failure"
				return_data["error"]="empty"
				return_data["value"]="empty"
				return return_data

		except Exception as ee:
			self.log.error("Error in pulling the role data : "+str(ee))
			self.close_connection()
			return_data["status"]="failure"
			return_data["error"]=str(ee)
			return_data["value"]=str(ee)
			return return_data




	def getServers(self):	
		try:
			return_data={}
			return_data["status"]="success"
			record_list=[]
			self.init_connection()	
			self.cur.execute("select id,name,url,org_id,push,pull,organization,remote_org_id,publish_without_email,unpublish_event,self_signed,pull_rules,push_rules,cert_file,client_cert_file,internal   from servers")
			records=self.cur.fetchall()
			self.close_connection()
			org_data=self.getOrgs()
			orgs=[]
			if org_data["status"]=="success":
				orgs=org_data["value"]
				#print ("Got it length is : "+str(len(orgs)))
			if records :
				for rec in records:
					my_dict={"id":rec[0],"name":rec[1],"url":rec[2],"org_id":rec[3],"push":rec[4],"pull":rec[5],"organization":rec[6],"remote_org_id":rec[7],"publish_without_email":rec[8],"unpublish_event":rec[9],"self_signed":rec[10],"pull_rules":rec[11],"push_rules":rec[12],"cert_file":rec[13],"cert_file_client":rec[14],"internal":rec[15]}
					
					if len(orgs):
						#print ("Org id : "+str(orgs[0]["id"]) +"  Id other " +str(rec[8]))
						my_dict.update({"org":org for org in orgs if org["id"]==rec[3]})
					
					record_list.append(my_dict)
					
				return_data["value"]=record_list
				return return_data
			else:
				return_data["status"]="failure"
				return_data["error"]="empty"
				return_data["value"]="empty"
				return return_data

		except Exception as ee:
			self.log.error("Error in pulling the role data : "+str(ee))
			self.close_connection()
			return_data["status"]="failure"
			return_data["error"]=str(ee)
			return_data["value"]=str(ee)
			return return_data

	def getJobs(self):	
		try:
			return_data={}
			return_data["status"]="success"
			record_list=[]
			self.init_connection()	
			# where process_id in (select distinct process_id from tasks where type='threat_scoring')
			self.cur.execute("select task_id,process_id,status,process_messages,task_message,task_type,scheduled_time,frequency from threat_scoring_tasks order by task_id desc limit 5")
			records=self.cur.fetchall()
			for rec in records:
					my_dict={"id":rec[0],"worker":"Threat Scoring","job_type":"threat_scoring","job_input":"Scheduled","status":rec[2],"retries":0,"message":rec[4],"progress":100,"org_id":1,"process_id":rec[1],"date_created":rec[6],"date_modified":rec[6]}
					record_list.append(my_dict)
			
			self.cur.execute("select id,worker,job_type,job_input,status,retries,message,progress,org_id,process_id,substring(date_created,1,10),substring(date_modified,1,10) from jobs order by id desc limit 2500")
			records=self.cur.fetchall()
			self.close_connection()
			org_data=self.getOrgs()
			orgs=[]
			if org_data["status"]=="success":
				orgs=org_data["value"]
			if records :
				for rec in records:
					my_dict={"id":rec[0],"worker":rec[1],"job_type":rec[2],"job_input":rec[3],"status":rec[4],"retries":rec[5],"message":rec[6],"progress":rec[7],"org_id":rec[8],"process_id":rec[9],"date_created":rec[10],"date_modified":rec[11]}
					
					if len(orgs):
						#print ("Org id : "+str(orgs[0]["id"]) +"  Id other " +str(rec[8]))
						my_dict.update({"org":org for org in orgs if org["id"]==rec[8]})
					
					record_list.append(my_dict)
					
				return_data["value"]=record_list
				return return_data
			else:
				return_data["status"]="failure"
				return_data["error"]="empty"
				return_data["value"]="empty"
				return return_data

		except Exception as ee:
			self.log.error("Error in pulling the role data : "+str(ee))
			self.close_connection()
			return_data["status"]="failure"
			return_data["error"]=str(ee)
			return_data["value"]=str(ee)
			return return_data

	def getTypes(self):
		try:

			ret_resp={}
			curr_dir=os.path.dirname(os.path.realpath(__file__))
			with open(os.path.join(curr_dir,"att.json"),"r+") as out_file:
				ret_resp=json.loads(out_file.read())
			return ret_resp
		except Exception as  ex :
			ret_resp["status"]="failure"
			ret_resp["value"]=str(ex)
			ret_resp["error"]=str(ex)


	def group_ioc(self,cluster="week",interval=4,current_year=True,year_number=dt.now().year):
		try:
			#print(year_number)
			return_data={}
			return_data["status"]="success"
			identifier=""
			if cluster=="week" and current_year ==True:
				
				dow=dt.today().weekday()
				dow=dow+1
				days=interval * 7 + dow
				interval=days
				#print("Interval : " +str(days) )
				#Below is the query which needs to be fixed for proper weekly data
				'''sql_query="select count(id),WEEK(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d')) as 'WEEK NUMBER' ,(SELECT CASE WHEN WEEK(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d')) =0 THEN makedate(YEAR(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d')),(WEEK(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d'))) *7 +1)  ELSE makedate(YEAR(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d')),(WEEK(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d'))-1) *7 +1 ) END) as'Start Date'  ,(SELECT CASE WHEN WEEK(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d')) =53 THEN makedate(YEAR(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d')),365)  ELSE makedate(YEAR(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d')),(WEEK(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d'))) *7) END) as 'End Date' from attributes where  DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d') >= DATE(NOW()) - INTERVAL %s DAY group by WEEK(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d'))"'''
				sql_query="select count(id),WEEK(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d')) as 'WEEK NUMBER' ,makedate(YEAR(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d')),(DAY(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d'))) ) as'Start Date'  , makedate(YEAR(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d')),(DAY(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d')))) as 'End Date' from attributes where  DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d') >= DATE(NOW()) - INTERVAL %s DAY group by WEEK(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d'))"
				identifier="WEEK #"

			elif cluster=="day" and current_year ==True:
				"""print("Interval before : " +str(interval))
				dom=dt.today().day -1
				days=((interval -1) * 30) + dom
				interval=days"""
				interval=29
				#print("\n\n Interval is : "+str(interval))
				sql_query="select count(id),DAY(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d')) as 'DAY NUMBER',DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d') as 'Start Date' ,DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d') as 'End Date' from attributes where  DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d') >= DATE(NOW()) - INTERVAL %s DAY group by DAY(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d'))"
				identifier="#"

			elif cluster=="month" and current_year==True:
				identifier="MONTH #"
				sql_query="select count(id),MONTH(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d')) as 'MONTH NUMBER' ,makedate(YEAR(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d')),(MONTH(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d')))) as 'Start Date' ,concat(YEAR(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d')),'-','30','-',MONTH(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d'))) as 'End Date' from attributes where  DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d') >= DATE(NOW()) - INTERVAL %s MONTH group by MONTH(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d'))"

			elif cluster=="month" and current_year ==False:
				identifier="MONTH #"
				#print(type(year_number))
				#print(year_number)
				sql_query="select count(id),MONTH(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d')) as 'MONTH NUMBER' ,makedate((YEAR(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d'))),(MONTH(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d')))) as 'Start Date' ,concat(YEAR(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d')),'-','30','-',MONTH(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d'))) as 'End Date' from attributes where  YEAR(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d')) = %s and  DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d') >= '"+str(int(year_number)+1)+"-01-01' - INTERVAL %s MONTH group by MONTH(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d'))"
				#print(sql_query)

			elif cluster=="year":
				current_year=True
				identifier="YEAR #"
				sql_query="select count(id),YEAR(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d')) as 'YEAR NUMBER' ,YEAR(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d')) as 'Start Date' ,YEAR(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d'))  as 'End Date' from attributes where  DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d') >= DATE(NOW()) - INTERVAL %s YEAR group by YEAR(DATE_FORMAT(FROM_UNIXTIME(timestamp),'%%Y-%%m-%%d'))"
				


				

			else:
				return_data["status"]="failure"
				return_data["value"]="In valid Search String"
				return_data["error"]="In valid Search String"
				return return_data

			
			record_list=[]
			self.init_connection()
			if current_year==True:	
				self.cur.execute(sql_query,(int(interval),))
			else:
				#print("In else")
				#print(type(interval))
				self.cur.execute(sql_query,(int(year_number),int(interval)))
			records=self.cur.fetchall()
			self.close_connection()
			for rec in records:
				record_list.append({"identifier":identifier,"count":rec[0],identifier:rec[1],"start_date":rec[2],"end_date":rec[3]})
			return_data["value"]=record_list
			#if cluster =="day":
			#	print (record_list)
			return record_list
			
			

		except Exception as ee :
			self.log.error("\n\n\nError in pulling the Dashboard IOC data : "+str(ee))
			self.close_connection()
			return_data["status"]="failure"
			return_data["error"]=str(ee)
			return_data["value"]=str(ee)
			return return_data

	def update_feed_status(self,feed_id,enabled):
		try:
			ret_resp={}
			self.init_connection()	
			self.cur.execute("update feeds set enabled  = %s  where id = %s",(int(enabled),int(feed_id)))
			self.conn.commit()
			self.close_connection()
			ret_resp["status"]="success"
			ret_resp["value"]="success"
			return ret_resp

		except Exception as ee:
			self.log.error("Error in Updating : "+str(ee))
			self.conn.rollback()
			self.close_connection()
			ret_resp["status"]="success"
			ret_resp["error"]=str(ee)
			ret_resp["value"]=str(ee)
			return ret_resp

	def FeedsTreeView(self):
		try:
			"""data_graph={
			 "name": "flare",
			 "children": [
			  {
			   "name": "analytics",
			   "children": [
			    {
			     "name": "cluster",
			     "children": [
			      {"name": "AgglomerativeCluster", "size": 3938},
			      {"name": "CommunityStructure", "size": 3812},
			      {"name": "HierarchicalCluster", "size": 6714},
			      {"name": "MergeEdge", "size": 743}
			     ]
			    },
			   ]
			  }]
			   }"""
			data_graph={"name":"Feeds","children":[]}
			
			ret_resp={}
			current_job=0
			self.init_connection()	
			#select f.id,f.name,f.provider,e.id,e.info,e.attribute_count from feeds f join events e on f.event_id = e.id where f.id not in (select id from feeds where input_source = 'misp')
			self.cur.execute("select f.id,f.name,f.provider,e.id,e.info,e.attribute_count,f.source_format,f.input_source from feeds f join events e on f.event_id = e.id where f.source_format <> 'misp'")
			non_misp=self.cur.fetchall()
			i=2
			self.cur.execute("select substring(job_input,7) as j from jobs where LEFT(job_input,'5') ='Feed:' and progress >=50 and progress <> 100 and process_id='Part of scheduled feed fetch' order by id desc limit 1")
			current_job=self.cur.fetchone()
			self.cur.execute("select sum(events.attribute_count) from events where events.id not in (select f.event_id from feeds f  where f.source_format <> 'misp')")
			misp_based=0
			misp_based=self.cur.fetchone()
			self.cur.execute("select f.id,f.name,f.provider,f.source_format,f.input_source from feeds f  where f.source_format = 'misp'")
			misp_data=self.cur.fetchall()
			if misp_based:
				try:
					misp_based=int(misp_based[0])
					print(misp_based)
				except Exception as ee:
					print("Exception 1" +str(ee))
					pass

			if current_job:
				try:
					current_job=int(current_job[0])
					print(current_job)
				except Exception as ee:
					print("Exception 1" +str(ee))
					pass
			for entry in non_misp:
				current=False
				element={"name":str(entry[1][0:21])+"..","type":"parent","idd":str(entry[0])}
				parent=element.copy()
				
				if int(entry[0]) == current_job:
					current=True
					#print("True !")
				
				element["children"]=[{"name":"Event id :"+str(entry[3]),"size":str(entry[3]),"type":"child","color":"#f0ad4e"},{"name":"Format :"+str(entry[6]),"type":"child","color":"#5bc0de"},{"name":"Source : "+str(entry[7]),"type":"child","color":"#d9534f","children":[{"name":"IOC-count ("+str(entry[5])+")","size":entry[5],"type":"child","current":current,"parent":parent,"color":"#5cb85c"}]}]
				data_graph["children"].append(element)

			if misp_based:
				element={"name":"MISP","type":"parent","idd":"@","children":""}
				#print(element)
				element["children"]=[{"name":"#count ("+str(misp_based)+")","children":[],"type":"misp","no_color":True}]
				#print("Now : "+str(element))
				for entry in misp_data:
					element["children"][0]["children"].append({"name":"("+str(entry[0])+") "+str(entry[1][0:21]),"type":"child","color":"#f0ad4e"})
					element["children"][0]["children"].append({"name":"Source : "+str(entry[4]),"type":"child","color":"#d9534f"})
				#print("Reached here")
				#print(element)
				data_graph["children"].append(element)

			self.close_connection()
			ret_resp["status"]="success"
			ret_resp["value"]=data_graph
			#print(data_graph)
			return ret_resp

		except Exception as ee:
			print("eX" +str(ee))
			self.log.error("Error in Updating : "+str(ee))
			#self.conn.rollback()
			self.close_connection()
			ret_resp["status"]="failure"
			ret_resp["error"]=str(ee)
			ret_resp["value"]=str(ee)
			return ret_resp

	def getAttributeCount(self,distinct=False):
		try:
			"""
				delete from correlations where attribute_id not in (select id from attributes) 
				or 1_attribute_id not in (select id from attributes);
			"""
			return_data={}
			self.init_connection()
			if distinct ==False:	
				self.cur.execute("select count(id) from attributes where deleted=0")
			else:
				self.cur.execute("select count(distinct(value)) from threat_scoring where isnull(value)=false")

			records=self.cur.fetchall()			
			if records :
				return_data["status"]="success"
				return_data["value"]=records[0][0]
				#return_data["value"]=100
			else:
				return_data["status"]="failure"
				return_data["value"]="No data"
				return_data["error"]="No data"
			self.close_connection()
			return return_data
		except Exception as ee:
			self.log.error("1 Error in Pulling IOC count : "+str(ee))
			self.close_connection()
			ret_resp["status"]="failure"
			ret_resp["error"]=str(ee)
			ret_resp["value"]=str(ee)
			return ret_resp

	def getAttributesToScore(self,offset,limit,external_scoring=False):
		try:
			
			return_data={}
			att_list=[]
			self.init_connection()	
			self.log.debug("Obtained limit :"+str(limit)+" and Offset : "+str(offset))
			
			self.cur.execute("select T.id,timestamp,comment,corelation,count(attribute_tags.tag_id) as tag_count ,value from (select attributes.id,timestamp,comment,count(1_attribute_id) as 'corelation' ,attributes.value1 as value from attributes  left join correlations on attributes.id=correlations.1_attribute_id where attributes.deleted=0  group by attributes.id limit %s offset %s) as T left join attribute_tags on T.id=attribute_tags.attribute_id group by T.id",(int(limit),int(offset)))
			
			"""self.cur.execute("select T.id,timestamp,comment,corelation,count(attribute_tags.tag_id) as tag_count ,value from (select attributes.id,timestamp,comment,0 as 'corelation' ,attributes.value1 as value from attributes  where attributes.deleted=0  group by attributes.id limit %s offset %s) as T left join attribute_tags on T.id=attribute_tags.attribute_id group by T.id",(int(limit),int(offset)))"""
			records=self.cur.fetchall()			
			if records :
				for att_data in records:
					#self.cur.execute("select count(distinct event_id) from correlations where value = %s",(att_data[5],))
					#recc=self.cur.fetchone()
					att_list.append({"id":att_data[0],"i_date":att_data[1],"i_comment":att_data[2],"i_corelation":att_data[3],"i_tags":att_data[4],"value":att_data[5]})
					#print("Data is : " +str(att_data[5]))
					
					#if att_data[5] == '4.59.56.18':
					#	self.log.error("Obtained check it :=" +str(att_data[3]))
				return_data["status"]="success"
				return_data["value"]=att_list
				#self.log.error("The pulled up list is  : "+str((att_list)))
			else:
				return_data["status"]="failure"
				return_data["value"]="No data"
				return_data["error"]="No data"
			
			self.close_connection()
			self.log.debug("Pulled up chunk length : "+str(len(att_list)))
			return return_data
		except Exception as ee:
			self.log.error("2 Error in getAttributesToScore : "+str(ee))
			self.close_connection()
			ret_resp={}
			ret_resp["status"]="failure"
			ret_resp["error"]=str(ee)
			ret_resp["value"]=str(ee)
			return ret_resp

	def getTaskStatusCodes(self,task_id):
		try:
			
			return_data={}
			self.init_connection()	
			self.cur.execute("select process_messages from threat_scoring_tasks where task_id=%s",(task_id,))
			records=self.cur.fetchall() #returns list of list			
			if records :
				return_data["status"]="success"
				return_data["value"]=json.loads(str(records[0][0]))
			else:
				return_data["status"]="failure"
				return_data["value"]="No data"
				return_data["error"]="No data"
			self.close_connection()
			return return_data

		except Exception as ee:
			self.log.error("Error in Pulling Task status : "+str(ee))
			self.close_connection()
			ret_resp={}
			ret_resp["status"]="failure"
			ret_resp["error"]=str(ee)
			ret_resp["value"]=str(ee)
			return ret_resp

	def getTaskid(self,task_type):
		try:
			
			return_data={}
			self.init_connection()	
			self.cur.execute("select id,process_id from tasks where type=%s",(task_type,))
			records=self.cur.fetchone() #returns list of list			
			if records :
				return_data["status"]="success"
				return_data["task_id"]=records[0]
				if records[1] is not None and records[1] != "":
					
					return_data["process_id"]=records[1]
				else:
					return_data["process_id"]=0
			else:
				return_data["status"]="failure"
				return_data["value"]="No data"
				return_data["error"]="No data"
			self.close_connection()
			return return_data

		except Exception as ee:
			self.log.error("Error in Pulling Task status : "+str(ee))
			self.close_connection()
			ret_resp={}
			ret_resp["status"]="failure"
			ret_resp["error"]=str(ee)
			ret_resp["value"]=str(ee)
			return ret_resp

	def updateAttributeScore(self,id,i_date_score=0,i_tags_score=0,
				i_corelation_score=0,i_comment_score=0,total_internal_score=0,e_date_score=0,e_tags_score=0,
				e_corelation_score=0,total_external_score=0,e_th_score=0,e_passive_dns_score=0,
				e_who_is_score=0,e_country_score=0,cumulative_score=0,value=None):
		try:
			#if (int(id) == 1767226):
			#	self.log.error("\n\n\n Obtained id "+ str(id) +".The paarmaters are : Tags -" +str(i_tags_score) +" Co-rel : " +str(i_corelation_score))
				
			return_data={}
			self.init_connection()	
			insert=False
			self.cur.execute("select count(id) from threat_scoring where attribute_id=%s",(int(id),))
			record=self.cur.fetchone() #returns single list			
			if record[0] == 0 :
				insert=True
				
			if insert:
				self.cur.execute("insert into threat_scoring (attribute_id,i_tag_score,i_date_score,i_comment_score,i_corelation_score,total_internal_score,e_tag_score,e_date_score,\
e_corelation_score,e_th_score,e_passive_dns_score,e_who_is_score,e_country_score,total_external_score,comulative_score,updated_comulative_score,value) values\
(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(id,i_tags_score,i_date_score,i_comment_score,i_corelation_score,total_internal_score,
e_tags_score,e_date_score,e_corelation_score,e_th_score,e_passive_dns_score,e_who_is_score,e_country_score,total_external_score,
cumulative_score,cumulative_score,value))
			else:
				self.cur.execute("update threat_scoring set i_tag_score=%s,i_date_score=%s,i_comment_score=%s,i_corelation_score=%s,total_internal_score=%s,e_tag_score=%s,e_date_score=%s,\
e_corelation_score=%s,e_th_score=%s,e_passive_dns_score=%s,e_who_is_score=%s,e_country_score=%s,total_external_score=%s,comulative_score=%s,updated_comulative_score=%s,value=%s where attribute_id= %s",(i_tags_score,i_date_score,i_comment_score,i_corelation_score,total_internal_score,
e_tags_score,e_date_score,e_corelation_score,e_th_score,e_passive_dns_score,e_who_is_score,e_country_score,total_external_score,
cumulative_score,cumulative_score,value,id))
				"""if value != None :
					#update t2 set score=(select score from (select max(score) as score from t2 where v3='user1') as sc) where v3='user1';
					self.cur.execute("update threat_scoring set updated_comulative_score=(select score from (select max(comulative_score) as score  from threat_scoring where value=%s) as T) where value=%s",(str(value),str(value)))"""
			self.conn.commit()
			self.close_connection()
			return_data["status"]="success"
			return_data["value"]="Updated"
			return return_data

		except Exception as ee:
			self.log.error("Error in Pulling / Updating Attribute with id "+str(id) +" status : "+str(ee))
			self.conn.rollback()
			self.close_connection()
			ret_resp={}
			ret_resp["status"]="failure"
			ret_resp["error"]=str(ee)
			ret_resp["value"]=str(ee)
			return ret_resp


	def updateAttributeScoreFinal(self,offset=0,limit=0,process_id=0):
		try:
			my_id=0
			self.log.debug("Process id : "+ str(process_id) + " Start time is  "+str(datetime.datetime.now()))
			return_data={}
			self.init_connection()
			self.cur.execute("select distinct value from threat_scoring where isnull(value)=false limit %s offset %s",(limit,offset))
			values=self.cur.fetchall()
			inner_exception_count=0
			for value in values:
				my_id=value[0]	
				try:
					self.cur.execute("update threat_scoring set updated_comulative_score=(select score from (select max(comulative_score) as score  from threat_scoring where value=%s) as T) where value=%s",(str(value[0]),str(value[0])))
					self.conn.commit()
				except Exception as inner:
					inner_exception_count=inner_exception_count+1
					self.log.error("Process id : "+str(process_id) +" - Error in Inner Update Attribute with id : "+str(my_id)+"  Exc : " +str(inner))
					if inner_exception_count > 100:
						break
	
			self.close_connection()
			return_data["status"]="success"
			return_data["value"]="Updated"
			self.log.debug("Process id : "+ str(process_id) + "End time is  "+str(datetime.datetime.now()))
			return return_data

		except Exception as ee:
			self.log.error("Error in Final Update Attribute with id : "+str(my_id)+"  Exc : " +str(ee))
			self.conn.rollback()
			self.close_connection()
			ret_resp={}
			ret_resp["status"]="failure"
			ret_resp["error"]=str(ee)
			ret_resp["value"]=str(ee)
			return ret_resp

	def updateProcessMessage(self,process_id,task_id,process_status="success",process_message=""):
		try:

			"""
				Initially set teh template as followes :
				insert into json_test(id,text)values(1,'[]')
				

				When teh process finishes push the update as :
				update json_test set test=JSON_ARRAY_APPEND(test,'$','{"status":"success","id":"Process 1","message":"Process updated successfully"}');
				
				$ means the whole array
				$1 meands append a list at index 1
				$2 means apppend at index 2

			"""			
			return_data={}
			self.init_connection()	
			process_data=json.dumps({"status":process_status,"id":process_id,"message":process_message})
			#JSON_ARRAY_APPEND IS CAUSING THE ERROR	
			self.cur.execute("update threat_scoring_tasks set process_messages=JSON_ARRAY_APPEND(process_messages,'$',%s) where task_id=%s",(process_data,task_id))
			self.conn.commit()
			self.close_connection()
			return_data["status"]="success"
			return_data["value"]="Updated"
			return return_data

		except Exception as ee:
			self.log.error("Error in Pulling Updating status : "+str(ee))
			self.conn.rollback()
			self.close_connection()
			ret_resp={}
			ret_resp["status"]="failure"
			ret_resp["error"]=str(ee)
			ret_resp["value"]=str(ee)
			return ret_resp

	def createTask(self,status="init",task_message="No message",is_current=False):
		
		try:

			"""
				Initially set teh template as followes :
				insert into json_test(id,text)values(1,'[]')

			"""	
			ret_resp={}		
			return_data={}
			self.init_connection()	
			if is_current ==False:	
				self.cur.execute("insert into threat_scoring_tasks (status,task_message,process_messages) values (%s,%s,%s)",(status,task_message,'[]'))
			else:
				self.cur.execute("update misp.threat_scoring_tasks set is_current=0")
				self.cur.execute("insert into threat_scoring_tasks (status,task_message,process_messages,is_current) values (%s,%s,%s,%s)",(status,task_message,'[]',1))
				

			self.conn.commit()
			self.close_connection()
			ret_resp["status"]="success"
			
			ret_resp["value"]=self.cur.lastrowid
			return ret_resp

		except Exception as ee:
			self.log.error("Error in inserting  Task values : "+str(ee))
			self.conn.rollback()
			self.close_connection()
			ret_resp={}
			ret_resp["status"]="failure"
			ret_resp["error"]=str(ee)
			ret_resp["value"]=str(ee)
			return ret_resp

	def updateTask(self,task_id=0,status="started",message="No message",process_id=0,update_process=True):
		try:
			ret_resp={}		
			return_data={}
			self.init_connection()	
			if update_process == True:	
				self.cur.execute("update threat_scoring_tasks set status=%s,task_message=%s,process_id=%s where task_id=%s",(status,message,process_id,task_id))
			else:
				self.cur.execute("update threat_scoring_tasks set status=%s,task_message=%s,scheduled_time=%s where task_id=%s",(status,message,str(datetime.datetime.now())[0:19],task_id)) #,scheduled_time=%s

			self.conn.commit()
			self.close_connection()
			self.log.debug("Update done for Update Task ! : "+str(task_id))
			ret_resp["status"]="success"
			
			ret_resp["value"]="Updated"
			return ret_resp

		except Exception as ee:
			self.log.error("Error in Updating  Task values : "+str(ee))
			self.conn.rollback()
			self.close_connection()
			ret_resp={}
			ret_resp["status"]="failure"
			ret_resp["error"]=str(ee)
			ret_resp["value"]=str(ee)
			return ret_resp

	def updateSchedulerTask(self,id,timer="",scheduled_time="",next_execution_time="",process_id="",message="Scheduler Task started"):
		try:
			ret_resp={}		
			return_data={}
			self.init_connection()	
			message=message+" By process id : " +str(process_id)
			self.cur.execute("update tasks set timer=%s,scheduled_time=%s,process_id=%s,next_execution_time=%s,message=%s where id=%s",(timer,scheduled_time,process_id,next_execution_time,message,id))

			self.conn.commit()
			self.close_connection()
			ret_resp["status"]="success"
			
			ret_resp["value"]="Updated"
			return ret_resp

		except Exception as ee:
			self.log.error("Error in Updating  Scheduling Task values : "+str(ee))
			self.conn.rollback()
			self.close_connection()
			ret_resp={}
			ret_resp["status"]="failure"
			ret_resp["error"]=str(ee)
			ret_resp["value"]=str(ee)
			return ret_resp

	def logHit(self,link="",author="",dated="",found_at="",word="",whole_text=""):
		try:
			try:
				res= str(whole_text).encode('ascii','replace')
				whole_text=res.decode("utf-8",'replace') 
					
			except Exception as inner:
				pass
			ret_resp={}
			self.init_connection()
			self.cur.execute("insert into Hits (link,author,dated,found_at,word,whole_text) values (%s,%s,%s,%s,%s,%s)",(link,author,dated,found_at,word,whole_text))
			self.conn.commit()
			self.close_connection()
			ret_resp["status"]="success"
			ret_resp["value"]="RInsertedd"
			return ret_resp
		except Exception as ex:
			#print("Exception Caught in Updating statius as Closed : " +str(ex))
			self.conn.rollback()
			self.close_connection()
			self.HitsLog(message="Exception Caught while Inserting in Hits : " +str(ex))
			ret_resp["status"]="failure"
			ret_resp["value"]=str(ex)
			return ret_resp

	def fetchHits(self):
		try:
			ret_resp={}
			self.init_connection()
			self.cur.execute("select id,link,author,dated,found_at,word,whole_text from Hits order by id desc")
			all_records=self.cur.fetchall()
			self.close_connection()
			ret_resp["status"]="success"
			ret_resp["value"]=all_records
			return ret_resp
		except Exception as ex:
			#print("Exception Caught in Updating statius as Closed : " +str(ex))
			self.close_connection()
			ret_resp["status"]="failure"
			ret_resp["value"]=str(ex)
			return ret_resp
		

	def HitsLog(self,dated=datetime.datetime.now().date(),message=""):
		try:
			try:
				res= str(message).encode('ascii','replace')
				message=res.decode("utf-8",'replace') 
			except Exception as inner:
				#print("INNER EXCEPTION : " +str(inner))
				pass
			ret_resp={}
			self.init_connection()
			self.cur.execute("insert into HitsLogs (dated,message) values (%s,%s)",(dated,message))
			self.conn.commit()
			self.close_connection()
			ret_resp["status"]="success"
			ret_resp["value"]="Inserted"
			return ret_resp
		except Exception as ex:
			print("Exception Caught Logging: " +str(ex))
			self.conn.rollback()
			self.close_connection()
			ret_resp["status"]="failure"
			ret_resp["value"]=str(ex)
			return ret_resp
		
		

		
			

		
			



			
	
		
			



			
	
                                                                                                                                                                                                      


	

	
					
	
	
