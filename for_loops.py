#! /usr/bin/python3.5
print("------ For Loop with range default start------")
for i in range(5):
	print("Statement %s ,step 1 "%i)

print("------ For Loop with Range specifying start and end  ------")
for i in range(5,10):
	print("Statement %s ,step 1 "%i)

print("------ For Loop with Range specifying start , end and step  ------")
step=2
for i in range(1,10,step):
	print("Statement %s ,step : %s "%(i,step))




