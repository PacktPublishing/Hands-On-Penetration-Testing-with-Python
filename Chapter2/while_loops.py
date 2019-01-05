#! /usr/bin/python3.5
i=0
print("------ While Basics ------")
while i < 5:
	print("Without Braces : Statement %s "%i)
	i=i+1
i=0
while (i < 5):
	print("With Braces : Statement %s "%i)
	i=i+1
print("------- While with Lists ------")
my_list=[1,2,"a","b",33.33,"c",4,5,['item 1','item 2']]
i=0
while(i < len(my_list)):
	if (type(my_list[i]) == type(1)):
		print ("Found Integer : %s "%my_list[i])
	elif (type(my_list[i]) == type("a")):
		print ("Found String : %s "%my_list[i])
	elif (type(my_list[i]) == type([])):
		print("------Found Inner list -Now lets iterate:---------")
		j=0
		while(j< len(my_list[i])):
			print("Inner Item : %s "%my_list[i][j])
			j =j +1
	else:
		print("Neither integer nor string : %s and Type is : %s "%(my_list[i],type(my_list[i])))
	i=i+1





