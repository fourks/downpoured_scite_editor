
def switchCppHeader():
	import os
	cppendings = ('.cpp','.c','.cxx')
	curFile = ScApp.GetFilePath().lower()
	if not curFile: return
	if curFile.endswith('.h'):
		dir, name = os.path.split(curFile)
		name1, name2 = os.path.splitext(name)
		try: doesExistIndex = map(lambda s: os.path.exists(curFile.replace('.h',s)), cppendings).index(True)
		except ValueError: print 'Could not find cpp.'; return
		else: nextFile = curFile.replace('.h',cppendings[doesExistIndex])
	else:
		try: doesExistIndex = map(lambda s: curFile.endswith(s), cppendings ).index(True)
		except ValueError: print 'Not a cpp header'; return
		nextFile = curFile.replace(cppendings[doesExistIndex],'.h')
		if not os.path.exists(nextFile): print 'Could not find .h.'; return
	ScApp.OpenFile(nextFile)

