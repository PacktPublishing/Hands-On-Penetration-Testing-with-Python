#! /usr/bin/python3.5
from multiprocessing import Pool
import multiprocessing as mp
import datetime as dt
class Pooling():
	def read_from_file(self,file_name):
		try:
			fn=list(file_name.keys())[0]
			line_no=0
			for line in open(fn,"r") :
				if line_no == 0:
					line_no=line_no + 1
					continue
				records=line.split(",")
				try:
					r_id=int(records[1])
					if (r_id % 1700) == 0 :
						file_name[fn].append(line)
				except Exception as ex:
					print("Exception : " +str(ex))
			return file_name
		except Exception as ex:
			print("Exception caught :"+str(ex))
			file_name[fn].append(str(ex))
			return file_name
	def driver_read(self):
		try:
			st_time=dt.datetime.now()
			p_cores=mp.cpu_count()
			pool = mp.Pool(p_cores)
			results=[]
			v="Million"
			files=[{v+"_0":[]},{v+"_1":[]},{v+"_2":[]},{v+"_3":[]}]
			aggrigated_result=pool.map(self.read_from_file,files)
			for f in aggrigated_result:
				with open ("Modulo_1700_agg","a+") as out_file:
					key=""
					for k,v in f.items():
						key=k
						print("--------------------------------------")
						print("Top 2 items for key "+str(k)+" :\n")
						for val in v[0:2]:
							print(val)
						print("-------------------------------------\n")
					out_file.writelines(f[key])
			print("Written Aggrigated Results")	
			pool.close()
			pool.join()
			en_time=dt.datetime.now()
			print("Total Execution time : " +str((en_time-st_time).seconds))
		except Exception as ex:
			print("Exception caught :"+str(ex))

	def write_to_file(self,file_name):
		try:
			st_time=dt.datetime.now()
			process=mp.current_process()
			name=process.name
			print("Started process : " +str(name))
			with open(file_name,"w+") as out_file:
				out_file.write("Process_name,Record_id,Date_time"+"\n")
				for i in range(1000000):
					tm=dt.datetime.now()
					w=str(name)+","+str(i)+","+str(tm)+"\n"
					out_file.write()
			print("Ended process : " +str(name))
			en_time=dt.datetime.now()
			tm=(en_time-st_time).seconds
			return "Process : "+str(name)+" - Exe time in sec : " +str(tm)
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
				args=("Million_"+str(i),)
				results.append(pool.apply_async(self.write_to_file,args))
			final_results=[]
			for result in results:
				final_results.append(result.get())
			pool.close()
			pool.join()
			en_time=dt.datetime.now()
			print("Results : " )
			for rec in final_results:
				print(rec)
			print("Total Execution time : " +str((en_time-st_time).seconds))
		except Exception as ex:
			print("Exception caught :"+str(ex))
obj=Pooling()
obj.driver_read()
