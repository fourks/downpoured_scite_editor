
def lookforprops(extension, filename):
	extension = '*'+extension #should look like *.bat
	f = open(filename,'r')
	found=False
	for line in f:
		if line.startswith('file.patterns.'):
			line = line.strip()
			line = line.replace('file.patterns','').split('=')[1].split(';')
			print line
			if extension in line:
				print 'yay',line
				found=True
				break
		elif line.startswith('filter.'):
			#optimization. unlikely to find file.patterns afterwards.
			break
	
	f.close()
	return found
	
lookforprops('.sml', r'C:\Users\bfisher\Documents\Fisher Applications\Coding\scite\caml.properties')
