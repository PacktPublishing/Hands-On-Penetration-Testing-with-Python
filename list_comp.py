#!/usr/bin/python3.5
sq_list=[x**2 for x in my_list]
print(sq_list)

def square(num):
    return num ** 2

my_list=[1,2,3,4]
sq_list=[]
for num in my_list:
	sq_list.append(square(num))
print(sq_list)




