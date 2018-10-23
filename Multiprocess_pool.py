#! /usr/bin/python3.5
from multiprocessing import Pool
import pandas as pd
import numpy as np
import multiprocessing as mp
import datetime as dt
class Pooling():
	def write_to_file(self,file_name):
		try:
			st_time=dt.datetime.now()
			process=mp.current_process()
			name=process.name
			print("Started process : " +str(name))
			with open(file_name,"w+") as out_file:
				out_file.write("Process_name,Record_id,Date_time"+"\n")
				for i in range(1000000):
					out_file.writeline(str(name)","+str(i)+","+str(dt.datetime.now())+"\n")
			print("Ended process : " +str(name))
			en_time=dt.datetime.now()
			return "Process : "+str(name)+" - Exe time in sec : " +str((en_time-st_time).seconds)
		except Exception as ex:
			print("Exception caught :"+str(ex))
			return "Process : "+str(name)+" - Exception  : " +str(ex)

	def driver(self):
		try:
			st_time=dt.datetime.now()
			p_cores=mp.cpu_count()
			pool = mp.Pool(p_cores)
			results=[]
			for i in range(8):
				results.append(pool.apply_async(self.write_to_file,"Million_"+str(i)))
			final_results=[]
			for result in results:
				final_results.append(result.get())
			pool.close()
			pool.join()
			en_time=dt.datetime.now()
			print("Results : ")
			for rec in final_results:
				print(rec)
			print("Total Execution time : " +str((en_time-st_time).seconds))
		except Exception as ex:
			print("Exception caught :"+str(ex))

obj=Pooling()
obj.driver()
