

def printascii():
	overrides = { 0:"(Null)", 9:"(Tab)",10:"(\\n Newline)", 13:"(\\r Return)", 32:"(Space)"}
	for i in range(128):
		c = overrides.get(i, chr(i))
		print str(i).zfill(3) + ' ' + c

printascii()