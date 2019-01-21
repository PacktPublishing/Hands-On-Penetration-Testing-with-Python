import json
import os
from keys import misp_url, misp_key
import logging
from DB_Layer.Misp_access import MispDB
import multiprocessing
from multiprocessing import Process
import math
import datetime
import time

class ThreatScore():
		
		def __init__(self):
			logger = logging.getLogger('Custom_log')
			logger.setLevel(logging.DEBUG)
			fh = logging.FileHandler('TS.log')
			fh.setLevel(logging.DEBUG)
			ch = logging.StreamHandler()
			ch.setLevel(logging.ERROR)
			formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
			fh.setFormatter(formatter)
			ch.setFormatter(formatter)
			# add the handlers to the logger
			logger.addHandler(fh)
			logger.addHandler(ch)
			self.log = logger
		
		def UpdateThreatScore(self,mode="parllel",task_id=0):		
			try:					
				ret_resp={}			
				cpu_count_to_use=1
				cpu_count=multiprocessing.cpu_count()
				if cpu_count > 1:
					cpu_count_to_use=math.ceil(cpu_count/1)
				self.log.debug("CPU cores to use : " +str(cpu_count_to_use))
				att_stat=MispDB().getAttributeCount()
				att_count=0
				feed_count=0
				if att_stat["status"]=="success":
					att_count=int(att_stat["value"])
					en_st=MispDB().getEnabledFeeds()
					if en_st["status"]=="success":
						feed_count=int(en_st["value"]["enabled"])				
				if att_count:
					while (1):
						if (int(att_count) % cpu_count_to_use) == 0:
							break
						else:
							att_count=att_count+1
					chunk_size=att_count/cpu_count_to_use
					chunk_index=0
					limit_offset=[]
					while(chunk_index <= att_count):
						limit_offset.append({"offset":int(chunk_index),"limit":int(chunk_size)})
						chunk_index=int(chunk_index+chunk_size) 

					process_list=[]
					MispDB().updateTask(task_id=task_id,status="processing",message="Processes to be Spawned",update_process=False)
					self.log.debug("Processes to be Spawned : " +str(cpu_count_to_use))
					for i in range(0,len(limit_offset)):
						pr=Process(target=self.StartProcessing,args=(limit_offset[i]["offset"],limit_offset[i]["limit"],str(i),task_id,False,feed_count))
						process_list.append(pr)
						pr.start()
					for process in process_list:
						process.join()
					status_codes=MispDB().getTaskStatusCodes(task_id)
					ret_resp["status"]="success"
					ret_resp["value"]="Threat Scoring Finished Successfully"
					if status_codes["status"]=="success":
						self.log.debug("Obtained Process messaged : " +str(status_codes))
						return_now=False
						for code in status_codes["value"]:
							if isinstance(code,str):
								code=json.loads(code)
							if code["status"]=="failure":
								ret_resp["status"]="failure"
								ret_resp["value"]="Threat Scoring Finished with error for Process id :"+code["id"]+" . Message : " +code["message"]
								return_now=True
								break						
						return ret_resp		
					else:
						
						ret_resp["status"]="failure"
						ret_resp["value"]="Process succeded but the final update failed as no value was returned in att_count" + status_codes["value"]
					
				else:
					ret_resp["status"]="failure"
					ret_resp["value"]="Threat Scoring Execution failed - No value in attribute count"
					return ret_resp				
				return ret_resp								
			except Exception as ex:
				print("Exception : " +str(ex))
				ret_resp["status"]="failure"
				ret_resp["value"]="1 Threat Scoring Execution failed - " +str(ex)
				self.log.error("Ended at time : " +str(datetime.datetime.now()))
				return ret_resp

	

		def ExternalScoring(self,att,weightage_settings,att_date_score,
					att_tags_score,att_corelation_score,att_comment_score,internal_score,feed_count=0):
			try:
				e_att_date_score=self.DateScore(att["e_date"],weightage_settings["Date"])
				e_att_tags_score=self.TagScore(att["e_tags"],weightage_settings["Tags"])
				e_att_corelation_score=self.CorelationScore(att["e_corelation"],weightage_settings["Corelation"],feed_count)
				e_att_comment_score=self.CommentScore(att["e_comment"],weightage_settings["Comment"])
				external_score=e_att_date_score + e_att_tags_score + e_att_corelation_score + e_att_comment_score #in % age
				external_score=external_score/10 #S
				comulative_score=(internal_score + external_score)/2
				resp=MispDB().updateAttributeScore(id=att["id"],i_date_score=att_date_score,
						i_tags_score=att_tags_score,i_corelation_score=att_corelation_score,
						i_comment_score=att_comment_score,total_internal_score=internal_score,
						e_date_score=e_att_date_score,e_tags_score=e_att_tags_score,
						e_corelation_score=e_att_corelation_score,e_comment_score=e_att_comment_score,
						total_external_score=external_score,cumulative_score=comulative_score,value=att["value"])
				return resp
			except Exception as ex:
				ret_resp={}
				ret_resp["status"]="failure"
				ret_resp["value"]=str(ex)
				return ret_resp

		def Scoring(self,att_list,weightage_settings,external_scoring=False,feed_count=0):
			try:
				ret_resp={}
				failure=False
				att_id_failed=[]
				for att in att_list:
						att_date_score=self.DateScore(att["i_date"],weightage_settings["Date"])
						att_tags_score=self.TagScore(att["i_tags"],weightage_settings["Tags"])
						att_corelation_score=self.CorelationScore(att["i_corelation"],weightage_settings["Corelation"],feed_count=feed_count)
						att_comment_score=self.CommentScore(att["i_comment"],weightage_settings["Comment"])
						internal_score=att_date_score + att_tags_score + att_corelation_score + att_comment_score 
					
						internal_score=internal_score/10 #Scale down to number
						internal_score=internal_score
						if external_scoring ==False:
							resp=MispDB().updateAttributeScore(id=att["id"],i_date_score=att_date_score,
								i_tags_score=att_tags_score,i_corelation_score=att_corelation_score,
								i_comment_score=att_comment_score,total_internal_score=internal_score,
								cumulative_score=internal_score,value=att["value"])	
						else:
							resp=self.ExternalScoring(att,weightage_settings,att_date_score,
						att_tags_score,att_corelation_score,att_comment_score,internal_score,feed_count=feed_count)
						if resp["status"]=="failure":
							failure=True
							att_id_failed.append(att["id"])							
				if failure==True:
						ret_resp["status"]="success"
						ret_resp["value"]="Cant update for  attributes : "+ str(att_id_failed)
				else:			
						ret_resp["status"]="success"
						ret_resp["value"]="Process Executed Successfully"					
				return ret_resp
			except Exception as ex:
				self.log.debug("Exception : "+str(ex))
				ret_resp={}
				ret_resp["status"]="failure"
				ret_resp["value"]=str(ex)
				return ret_resp

	

		def StartProcessing(self,offset,limit,process_id,task_id,external_scoring=False,feed_count=0):
			try:
				root=os.path.dirname(os.path.realpath(__file__))
				weightage_settings={}
				with open(os.path.join(root,"weightage.json")) as in_file:
					weightage_settings=json.loads(in_file.read())			
				att_list_status=MispDB().getAttributesToScore(offset,limit)
				failure=False
				att_id_failed=0
				if att_list_status["status"]=="success":
					att_list=att_list_status["value"]
					if external_scoring==False:
						self.log.debug("Started : Limit : "+str(limit) + " Offset : " +str(offset))
						resp=self.Scoring(att_list,weightage_settings,external_scoring=False,feed_count=feed_count)
					else:
						resp=self.Scoring(att_list,weightage_settings,external_scoring=True,feed_count=feed_count)
	
					if resp["status"]=="success":
						MispDB().updateProcessMessage(process_id,task_id,"success","Process succeded for chunk : "+str(offset)+" -- "+str(limit))
						self.log.debug("Process succeded for chunk : "+str(offset)+" -- "+str(limit))
						
					else:						
							MispDB().updateProcessMessage(process_id,task_id,"failure","0 Process failed to Update details for chunk : "+str(offset)+" -- "+str(limit) +" - 0 Failure Message : " +str(resp["value"]))
							self.log.debug("Process Failed for chunk : "+str(offset)+" -- "+str(limit))	
								
				else:
						att_stat=MispDB().getAttributeCount()
						att_count=0
						if att_stat["status"]=="success":
							att_count=int(att_stat["value"])
						if offset < att_count:
								MispDB().updateProcessMessage(process_id,task_id,"failure","1 Process failed to pull up chunk : "+str(offset)+" --"+str(limit)+" - 1 Failure Message : " +str(att_list_status["value"]))
						else:
							MispDB().updateProcessMessage(process_id,task_id,"success","Process found empty chunk : "+str(offset)+" -- "+str(limit))					
			except Exception as ex:
				MispDB().updateProcessMessage(process_id,task_id,"failure","2 Process failed for chunk : "+str(offset)+" --"+str(limit)+" - 2 Failure Message : " +str(ex))	
				
		


		def ComputeScore(self,weighted_parameter,weightage_settings,p_type="NAN"):
			try:
				weightage=int(weightage_settings["weightage"])
				partitions=weightage_settings["partitions"]
				assig_wt=0
				for partition in partitions:
					if partition["type"]=="range":
						ll=int(partition["ll"])
						ul=int(partition["ul"])
						weight=int(partition["weight"])
						if weighted_parameter >= ll and weighted_parameter <= ul:
							assig_wt=weight
							break
			
					elif partition["type"]=="fixed":
						size=int(partition["size"])
						weight=int(partition["weight"])
						if weighted_parameter ==size:
							assig_wt=weight
							break	
				score=weightage * (assig_wt /100)
				return score
				
			except Exception as ex:
				self.log.error("Exception while computing score for parameter type : "+str(p_type)+" - "+str(ex))
				return 0
				
		def DateScore(self,date,weightage_settings):
			try:
				ioc_time=time.strftime('%Y-%m-%d', time.localtime(float(date)+14400))
				time_format = '%Y-%m-%d'
				time_delta=datetime.datetime.now() - datetime.datetime.strptime(ioc_time, time_format) 
				days=time_delta.days
				if days < 0:
					days=1   #It means its very recent
				score=self.ComputeScore(int(days),weightage_settings,'Date')
				return score
			except Exception as ex:
				self.log.error("Exception in computing Date Score : "+str(ex))
				return 0
		def TagScore(self,tags,weightage_settings):
			try:
				score=self.ComputeScore(int(tags),weightage_settings,'Tags')
				return score
			except Exception as ex:
				self.log.error("Exception in computing Tag Score : "+str(ex))
				return 0
		def CorelationScore(self,corelations,weightage_settings,feed_count):
			try:
				weightage=int(weightage_settings["weightage"])
				partitions=weightage_settings["partitions"]
				c_p=(int(corelations)/int(feed_count))*100
				assig_wt=0
				for partition in partitions:
						ll=int(partition["ll"])
						ul=int(partition["ul"])
						weight=int(partition["weight"])
						if c_p >= ll and c_p <= ul:
							assig_wt=weight
							break
				score=weightage * (assig_wt /100)
				return score
			except Exception as ex:
				self.log.error("Exception in computing Correlation Score : "+str(ex))
				return 0
		def CommentScore(self,comments,weightage_settings):
			try:
				if comments != "" and comments != None and comments != " " :
					score=self.ComputeScore(1,weightage_settings,'Comments')
				else:
					score=self.ComputeScore(0,weightage_settings,'Comments')
				return score
			except Exception as ex:
				self.log.error("Exception in computing Comment Score : "+str(ex))
				return 0


ob=ThreatScore()
ob.UpdateThreatScore()

