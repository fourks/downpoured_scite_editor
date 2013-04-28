
import os
import sys


sourceext=['.asm','.c','.cc','.cpp','.cxx','.cs','.h','.hh','.hxx','.hpp','.idl','.odl','.rc','.rc2','.dlg','.def','.vb','.vbs','.bas','.frm','.cls','.ctl','.java','.js','.py','.pl','.rb','.cgi','.lua','.conf','.mak','.properties','.html','.xml','.iface','.bat','.e']
def listdir(dir, bOnlySource=False):
	#don't include directories
	files = [file for file in os.listdir(dir) if not os.path.isdir(os.path.join(dir,file))]
	if bOnlySource:
		newlist = []
		for file in files:
			bFound = False
			for ext in sourceext:
				if file.lower().endswith(ext):
					bFound = True
					break
			if bFound:
				newlist.append(file)
		return newlist
	else:
		return files

def printdir(dir, bOnlySource=False):
	filelist = listdir(dir, bOnlySource)
	#~ print filelist
	for file in filelist:
		print os.path.join(dir, file) + ':1:l'
		# this syntax indicates to Scite that this is a clickable filepatah

if __name__=='__main__':
	printdir('c:\\', True)
