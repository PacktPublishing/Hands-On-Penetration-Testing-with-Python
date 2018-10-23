#! /usr/bin/python3.5
def print_msg1():
	print("Basic Message Printed")
def print_msg2(message):
	print(message)
def print_msg3(message,do_return):
	print(message)
	if do_return == True:
		return True
def print_msg4(m,op1="Hello world",op2=False):
	print("-----------------------------------")
	print("Mandatory aurgument : "+str(m))
	print("Optional aurgument 1 : " +str(op1))
	print("Optional aurgument 2 : " +str(op2))
	print("-----------------------------------")
def print_msg5(arg1,arg2,arg3):
	return arg1*2,arg2*2,arg3*2
if __name__ == "__main__":
	print_msg1()
	print_msg2("This is a custom message")
	print("-----------------------------------")
	rt=print_msg3("This is message with return type",True)
	print("Return value is : " +str(rt)+"\n\n")
	print("-----------------------------------")
	print("-----------------------------------")
	n_rt=print_msg3("This is message without return type",False)
	print("Return value is : " +str(n_rt)+"\n\n")
	print("-----------------------------------")
	n_rt=print_msg3(do_return=False,message="Criss cross parameters !")
	print("-----------------------------------")
	print_msg4("Test Mandatory")
	print_msg4(1,2)
	print_msg4(2,3,2)
	print_msg4(1,op2="Test")
	print_msg4(1,op2=33,op1=44)
	r=print_msg5(1,2,3)
	print("type : " +str(type(r))+"Values : " +str(r[0]),str(r[1]),str(r[2]))
	
