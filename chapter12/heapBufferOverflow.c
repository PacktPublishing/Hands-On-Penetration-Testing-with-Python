#include<stdio.h>
//#include<conio.h>
#include<string.h>
#include<stdlib.h>

int main(int argc ,char** argv)
{
	char *buffer=malloc(20);
	strcpy(buffer,argv[1]);
	free(buffer);
}
