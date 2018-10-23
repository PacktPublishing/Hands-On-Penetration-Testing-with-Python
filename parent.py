#! /usr/bin/python3.5
import child as c
def parent_method():
	print("--------------------")
	print("IN parent method -Invoking child()")
	c.child_method()
	print("--------------------\n")

parent_method()
