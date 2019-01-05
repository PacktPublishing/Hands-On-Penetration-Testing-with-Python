#!/usr/bin/python3.5
l1=[1,2,3,4]
l2=[5,6]
sq_even=[x**2 for x in l1 if x%2 ==0]
l_sum=[x+y for x in l1 for y in l2]
sq_values=[{x:x**2} for x in l1]
print("Even squares : " +str(sq_even))
print("Sum nested Loop : " +str(l_sum))
print("Squares Dict : " +str(sq_values))

