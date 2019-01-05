#!/usr/bin/python3.5
a=22
b=44
c=55
d=None
if 22:
	print("This will be printed -> if 22:")
if "hello":
	print("This will  be printed -> if 'hello':")
if -1:
	print("This will be printed -> if -1")
if 0:
	print("This would not be printed")
if d:
	print("This will not be prined")

print("Lets Start with logical operators")

if a and b and c :
	print("Printed -> if a and b and c:")
if a and b and c and d:
	print("Not printed")
if a < b and a < c:
	print("a is smaller than b and c -> without braces")
if (a < b) and (a <c) :
	print("a is smaller than b and c -> with braces")

if a or b or c or d:
	print("This is printed > if a or b or c or d :")

if not d:
	print("Not of d will be printed as not None is True")
