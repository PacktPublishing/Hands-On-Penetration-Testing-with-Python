import base64
import sys
def encode (password):
	return base64.b64encode(password)

def decode(text):
	return base64.b64decode(text)

#print(encode(sys.argv[1]))
#print (decode('JCh0IUBNaXNwQER1MDE='))
