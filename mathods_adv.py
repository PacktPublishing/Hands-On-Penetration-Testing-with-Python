#! /usr/bin/python3.5
def method_1(*args):
	print("------------------------")
	print("Method_1 -")
	print("Recievied : " +str(args))
	sum=0
	for arg in args:
		sum=sum+arg
	print ("Sum : " +str(sum))
	print("------------------------\n")
def method_1_rev(a=0,b=0,c=0,d=0):
	print("------------------------")
	print("Method_1_rev")
	sum= a + b + c + d
	print ("Sum : " +str(sum))
	print("------------------------\n")
def method_2(**args):
	print("------------------------")
	print("Method 2")
	print("Recievied : " +str(args))
	for k,v in args.items():
		print("Key : " +str(k) +",\
		Value : "+str(v))
	print("------------------------\n")
def method_2_rev(k1="first key",k2="second key"):
	print("------------------------")
	print("Methid_2_rev")
	print("Value for K1 : "+str(k1))
	print("Value for K2 : "+str(k2))
	print("------------------------\n")

def execute_all():
	method_1(1,2,3,4,5,6,7,8)
	method_2(k1=22,k2=33)
	my_list=[1,2,3,4]
	my_dict={"k1":"Value 1","k2":"Value 2"}
	method_1_rev(*my_list)
	method_2_rev(**my_dict)
execute_all()

