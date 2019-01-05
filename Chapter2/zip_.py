#!/usr/bin/python3.5
l1=[1,2,3,4]
l2=[5,6,7,8]
zipped=list(zip(l1,l2))
print("Zipped is : " +str(zipped))
sum_=[x+y for x,y in zipped]
print("Sum : "+str(sum_))
sum_1=list(map(lambda x :x[0]+x[1] ,zip(l1,l2)))
print("Sum one shot (M1) : "+str(sum_1))
sum_2=[x + y for x,y in zip(l1,l2)]
print("Sum 1 shot (M2) : "+str(sum_2))


