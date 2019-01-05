#! /usr/bin/python3.5
print("------ Iterate over strings ------")
my_str="Hello"
for s in my_str:
	print(s)

print("------ Iterate over Lists------")
my_list=[1,2,3,4,5,6]
for l in my_list:
	print(l)
print("------ Iterate over Lists with index and value ------")
my_list=[1,2,3,4,5,6]
for index,value in enumerate(my_list):
	print(index,value)

print("------ Iterate over Dictionary Keys  ------")
my_dict={"k1":"v1","k2":"v2","k3":"v3"}
for key in my_dict:
	print("Key : "+key+ " Value : "+ my_dict[key])

print("------ Iterate over Dictionary with items()  ------")
my_dict={"k1":"v1","k2":"v2","k3":"v3"}
for key,value in my_dict.items():
	print("Key : "+key+ " Value : "+ value)


print("------ Iterate over Tuples  ------")
my_tuple=(1,2,3,4,5)
for value in my_tuple:
	print(value)

print("------ Iterate over Set  ------")
my_set={2,2,3,3,5,5}
for value in my_set:
	print(value)



