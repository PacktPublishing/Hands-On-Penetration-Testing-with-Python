#!/usr/bin/python3.5
def compute_area(shape,**args):
	if shape.lower() == "circle":
		radius=args.get("radius",0)
		area=2.17 * (radius **2)
		print("Area circle : " +str(area))
	elif shape.lower() in ["rect","rectangle"]:
		length=args.get("length",0)
		width=args.get("width",0)
		area=length*width
		print("Area Rect : " +str(area))
	elif shape.lower() == "triangle":
		base=args.get("base",0)
		altitude=args.get("altitude",0)
		area=(base*altitude)/2
		print("Area :Triangle  " +str(area))
	elif shape.lower() == "square":
		side=args.get("side",0)
		area= side **2
		print("Area Square : " +str(area))
	else:
		print("Shape not supported")

	



