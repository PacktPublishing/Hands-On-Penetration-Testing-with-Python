#!/usr/bin/python3.5
def genMethod():
    a=100
    for i in range(3):
        print("A before increment : " +str(a))
        a=a+1
        yield a
        print("A after increment : " +str(a))

def driver_for():
    for a in genMethod():
        print("A is : "+str(a))
        print("--------------")
def driver():
	v=genMethod()
	next(v)
	print("----------------------")
	next(v)
	print("----------------------")
	next(v)
	print("----------------------")
#driver()'
driver_for()


def foo():
	print ("begin")
	for i in range(3):
		print ("before yield", i)
		yield i
		print ("after yield", i)

