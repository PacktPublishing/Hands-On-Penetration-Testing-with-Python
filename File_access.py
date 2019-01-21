#! /usr/bin/python3.5

class File:
	def __init__(self,filepath):
		self.path=filepath

	def read(self):
		print("Opening file for reading")
		f=open(self.path,"r+")
		all_data=f.read()
		f.seek(0)
		all_lines=f.readlines()
		f.seek(0)
		b_r=f.read(20)
		f.seek(0)
		line_read=f.readline()
		if f.closed ==False:
			print("Closing file")
			f.close()
		print("All data : "+str(all_data))
		print("--------------------\n")
		print("Lines:")
		for i,line in enumerate(all_lines):
			print("#: "+str(i)+ ": "+str(line))
		print("--------------------\n")
		b_l=str(len(b_r))
		print("Buffered : ("+b_l+") -" +str(b_r))
		print("--------------------\n")
		print("Line read: "+str(line_read))
		print("--------------------\n")
	
	def write_append(self,content="",m="w+",nl=False):
		if type(content) ==type([]):
			with open(self.path,m) as outfile:
				if not nl:
				   outfile.writelines(content)
				else:
				   for line in content:
				      outfile.write(line)
				      outfile.write("\n")
		elif type(content) ==type (""):
			with open(self.path,"w+") as outfile:
				outfile.write(content)
		else:
			print("Cant write -Invalid content found")
class Driver():
	def main(self):
		my_file=File("python.txt")
		wr_list=["Learning Python is fun",".Just started it"]
		my_file.write_append(wr_list)
		ap_list=["\nI want to explore all of it","Its awesome"]
		my_file.write_append(ap_list,"a+",True)
		my_file.read()
obj=Driver()
obj.main()
	

	
		
