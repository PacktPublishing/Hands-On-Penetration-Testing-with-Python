#!/usr/bin/python3.5
a=22;b=44;c=55;d=None
if a and b and c and d:
	print("Not printed")
else:
	print('Remember and operator -> All must evaluate to True !')
if a == b:
	print("A and B are equal")
else:
	print("A and B are not equal ! But we saw how to use == :)")
print("\nLets use some Bit wise operators with condition statements :\n")
a=2;b=2;c=0
bit_wise=a & b & c
if bit_wise:
	print("Bit wise and returned non zero %s"%bit_wise)
else:
	print("Bit wise and returned zero : %s"%bit_wise)
bit_wise=a&b
if bit_wise:
	print("Now Bit wise and returned non zero : %s"%bit_wise)
else:
	print("Again Bit wise and returned zero : %s"%bit_wise)

bit_wise_or = a | c
if bit_wise_or:
	print("BIt wise OR - Should return 2 -> %s"%bit_wise_or)
else:
	print("Thats strange !! -> %s"%bit_wise_or)

left_shift= a << b
if left_shift:
	print("Remember Left shift has multiplication impact. -> %s"%left_shift)
else:
	print("Thats strange !! -> %s"%left_shift)

right_shift= a >> b
if right_shift:
	print("Thats strange !! -> %s"%right_shift)
else:
	print("Remember Right shift has division impact.  -> %s"%right_shift)
neg_minus_1= ~ a
if neg_minus_1 :
	print("~ operator has (-n-1) impact - (-n-1) for %s -> %s "%(a,neg_minus_1))
else:
	print("~ operator has (-n-1) impact - Produced 0  -> %s"%neg_minus_1)
	



