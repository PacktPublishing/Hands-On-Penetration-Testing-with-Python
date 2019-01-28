#include<stdio.h>
//#include<conio.h>
#include<string.h>

void functionFunction(char* param ,int p2 ,float p3)
{
	printf("Hello function \n");
	char local[10];
	strcpy(local,param);
	printf("%s",param);
}

int main(int argc ,char** argv)
{
	functionFunction(argv[1] ,22,3.14);
}
