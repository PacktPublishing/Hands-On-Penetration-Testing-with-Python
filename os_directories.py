#! /usr/bin/python3.5
import os
class OsDirectories():
	def __init__(self):
		self.path_parent_0=os.getcwd
		self.file_path=os.path.realpath(__file__)
		self.pr=os.path.dirname(self.file_path)

	def Traverse(self,path,tr_all=False):
		if tr_all ==False:
			files = os.listdir(path)
			for i in files:
			    if os.path.isdir(os.path.join(path,i)):
				dir_=str(os.path.join(path,i))
			        print("Dir : " +dir_)
			        self.Traverse(os.path.join(path,i))
			    else:
			        print(os.path.join(path,i))
		else:
			for root, dirs, files in os.walk(path):
				for f in files:
					print(f)
	def create_ch_dir(self,dir_path,action="create"):
		if action =="create":
			print("\nBefore Creation :")
			self.Traverse(os.path.dirname(dir_path))
			if os.path.exists(dir_path) == False:
				os.mkdir(dir_path)
			else:
				print("Already Exists")
			print("\n\nAfter Creation")
			self.Traverse(os.path.dirname(dir_path))
		elif action =="change":
			print("\nBefore Changing :")
			print(os.getcwd())
			os.chdir(dir_path)
			print("\n\nAfter Changing")
			print(os.getcwd())
		else:
			print("Invalod action")
	def rename_delete_files(self,file_path,
			operation="delete",new_name="renamed.txt"):
		if os.path.isfile(file_path):
			if operation == "delete":
				print("\nBefore Removal :")
				self.Traverse(os.path.dirname(file_path))
				os.remove(file_path)
				print("\n\nAfter Removal")
				self.Traverse(os.path.dirname(file_path))
			elif operation == "rename":
				print("\nBefore Rename :")
				self.Traverse(os.path.dirname(file_path))
				parent_dir=os.path.dirname(file_path)
				new_path=os.path.join(parent_dir,new_name)
				os.rename(file_path,new_path)
				print("\n\nAfter Rename :")
				self.Traverse(os.path.dirname(file_path))
			else:
				print("Invalod action")	
		else:
			print("File does not exist cant Delete or rename")

o=OsDirectories()
o.create_ch_dir(os.path.join(o.pr,"Test_folder"))
o.create_ch_dir(os.path.join(o.pr,"Test_folder"),"change")
o.rename_delete_files(os.path.join
	(o.pr,"remove_folder","remove_file1"),"delete")
o.rename_delete_files(os.path.join
	(o.pr,"remove_folder","remove_file2"),"rename","updated")
		
		
		
