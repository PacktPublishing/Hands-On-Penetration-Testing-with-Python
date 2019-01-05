#! /usr/bin/python3.5
class ExceptionHandeling():
	def __init__(self):
		pass
	def div_1(self,num1,num2):
		try:
			num3=num1/num2
			print("Division result : " +str(num3))

		except Exception as ex:
			print("Exception : "+str(ex))

	def div_2(self,num1,num2):
		try:
			num3=num1/num2
			print("Division result : " +str(num3))

		except Exception as ex:
			print("Exception : "+str(ex))
		finally:
			print("Cleaning Up")
			del num1
			del num2

	def div_3(self,num1,num2):
		try:
			if num2 == 0:
				raise ValueError('Division by 0 will throw exception')
			else:
				num3=num1/num2
				print("Division result : " +str(num3))
		except Exception as exc:
			print("Exception : "+str(exc))
obj=ExceptionHandeling()
obj.div_1(10,2)
obj.div_1(10,0)
print("\n")
obj.div_2(10,2)
obj.div_2(10,0)
print("\n")
obj.div_3(10,2)
obj.div_3(10,0)	
