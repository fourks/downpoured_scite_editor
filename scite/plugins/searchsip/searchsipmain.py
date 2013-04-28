
from searchutil import SipException
import os
from os.path import join
import searchutil
import shutil
import searchsipimpl

def searchSip(*args):
	ret = None
	try: ret = _searchSip(*args)
	except SipException,e: print 'Exception: '+str(e)
	return ret

def searchSipToggle(*args):
	ret = None
	try: ret = _searchSipToggle(*args) 
	except SipException,e: print 'Exception: '+str(e)
	return ret
	
def searchSipRebuild(*args):
	ret = None
	try: ret = _searchSipRebuild(*args)
	except SipException,e: print 'Exception: '+str(e)
	return ret



def getsCfgdir(sHome):
	return join(join(sHome, 'plugins'), 'searchsip_userprefs')
def getsExePath(sHome):
	pth = join(join(join(sHome, 'plugins'), 'searchsip'), 'ssip.exe')
	if not os.path.exists(pth): raise SipException('could not find ssip.exe')
	return pth

def mapPaths(sCfgdir, sPath, bVerbose=False):
	sPath = sPath.lower()
	for fname in os.listdir(sCfgdir):
		if not fname.lower().endswith('.cfg'): continue
		if fname=='ssip.cfg': continue
		fnamefull = join(sCfgdir, fname)
		f=open(fnamefull ,'r')
		match = False
		for line in f:
			line=line.strip()
			if line.startswith('srcdir'):
				spl = line.split('=',1)
				if len(spl)==2:
					wh, wpath = spl
					if len(wh.replace('srcdir',''))!=1:
						print 'invalid number', line
					wpath = wpath.lower()
					if len(wpath)>2 and sPath.startswith(wpath):
						if bVerbose: print 'match with: '+line
						match = True
						break
				else:
					print 'invalid line: ',line
		f.close()
		if match:
			return fname
	return None

def setupCfg(sCfgdir, fname):
	src = join(sCfgdir, fname)
	target = join(sCfgdir, 'ssip.cfg')
	if os.path.exists(target): os.unlink(target)
	if os.path.exists(target): raise SipException("Can't delete ssip.cfg")
	shutil.copy(src, target)
	src = join(sCfgdir, fname+'.db')
	if os.path.exists(src):
		target = join(sCfgdir, 'ssip.db')
		if os.path.exists(target): os.unlink(target)
		if os.path.exists(target): raise SipException("Can't delete ssip.cfg")
		os.rename(src, target)
		return True
	else:
		return False

def restoreCfg(sCfgdir, fname):
	# not needed, and we want to be simple because this is in a finally block
	# src = join(sCfgdir, 'ssip.cfg')
	# if os.path.exists(src): os.unlink(src)
	src = join(sCfgdir, 'ssip.db')
	if os.path.exists(src):
		target = join(sCfgdir, fname+'.db')
		os.rename(src, target)

g_nextShouldPrompt = False
def getInput(s, sHomedir, sLnzPath):
	global g_nextShouldPrompt
	s=s.strip()
	if not s or g_nextShouldPrompt:
		g_nextShouldPrompt = False
		s = searchutil.getString(sHomedir, sLnzPath)
		s=s.strip()
		if not s:
			print 'Canceled.'
			return None
	return s

def _searchSip(sMode, sPath, sCurrentWord, sHomedir, sLnzPath):
	bIsIndex = 'NotIndex' not in sMode
	sCfgdir = getsCfgdir(sHomedir)
	fname = mapPaths(sCfgdir, sPath)
	if not fname:
		print 'File not mapped.'
		return
		
	s = getInput(sCurrentWord,sHomedir, sLnzPath)
	if not s:
		return
	
	wasdb = setupCfg(sCfgdir, fname)
	try:
		if bIsIndex and not wasdb: print 'Building index for '+fname+'...'
		os.chdir(sCfgdir) # ssip.exe will see that config file
		
		if not bIsIndex:
			if sMode=='NotIndexedWhole':
				stdout = searchutil.runReturnStdout(getsExePath(sHomedir), ['-noindex', s])
			elif sMode=='NotIndexedNotWhole':
				stdout = searchutil.runReturnStdout(getsExePath(sHomedir), ['-noindexnowhole', s])
			else:
				raise SipException('unknown mode')
		else:
			searchsipimpl.checkStringOk(s) #will raise exception if string isn't ok
			rawresults = searchutil.runReturnStdout(getsExePath(sHomedir), ['-s', s])
			if sMode=='IndexedAll':
				stdout = rawresults
			else:
				searchsipimpl.filter(sMode, s, rawresults)
				stdout = None
				
				
		if stdout!=None:
			if not stdout.strip(): print '0 results.'
			print stdout
	finally:
		restoreCfg(sCfgdir, fname)
	

def _searchSipToggle(sPath, sHomedir):
	# display some stuff too.
	global g_nextShouldPrompt
	sCfgdir = getsCfgdir(sHomedir)
	fname = mapPaths(sCfgdir, sPath, True)
	if not fname:
		print 'File not mapped.'
		return
	print 'File mapped to project: '+fname
	print 'The next search will prompt for string.'
	g_nextShouldPrompt = True
	
def _searchSipRebuild(sPath, sHomedir):
	sCfgdir = getsCfgdir(sHomedir)
	fname = mapPaths(sCfgdir, sPath)
	if not fname:
		print 'File not mapped.'
		return
	target = join(sCfgdir, fname+'.db')
	if os.path.exists(target): os.unlink(target)
	wasdb = setupCfg(sCfgdir, fname)
	try:
		if wasdb: raise SipException('db file should have been absent')
		os.chdir(sCfgdir)
		# ssip.exe will see that config file
		print 'Re-building index for '+fname+' ...'
		stdout = searchutil.runReturnStdout(getsExePath(sHomedir), ['-start'])
		print stdout
	finally:
		restoreCfg(sCfgdir, fname)

def Go_Standard(Classobj, s, searchmode):
	try:
		ret = Go_Standard_impl(Classobj, s, searchmode)
	except SipException,e:
		print 'Exception: '+str(e)
	return ret


if __name__=='__main__':
	sPath=r'c:\pydev\pyaudio_here\simplesourceindexing\intelliguess\bcaudio\bcaudio.h'
	sHomedir=r'C:\Users\bfisher\Documents\Fisher Applications\Coding\scite_mine\wscite'
	sLnzPath=r'C:\Users\bfisher\Documents\Fisher Applications\Utilities\lnzscript\lnzscript.exe'
	
	#~ _searchSipRebuild(sPath,sHomedir)
	#~ _searchSipToggle(sPath,sHomedir)
	
	#~ sMode='IndexedAll'
	#~ sCurrentWord='effect_modulate'
	#~ _searchSip(sMode, sPath, sCurrentWord, sHomedir, sLnzPath)
	#~ print
	
	#~ sCurrentWord='data_right==NULL) '
	#~ sMode='NotIndexedNotWhole'
	#~ _searchSip(sMode, sPath, sCurrentWord, sHomedir, sLnzPath)
	#~ print
	#~ sCurrentWord='ftl_fail_'
	#~ sMode='NotIndexedNotWhole'
	#~ _searchSip(sMode, sPath, sCurrentWord, sHomedir, sLnzPath)
	#~ print
	
	#~ sCurrentWord='6'
	#~ sMode='NotIndexedWhole'
	#~ _searchSip(sMode, sPath, sCurrentWord, sHomedir, sLnzPath)
	#~ print
	
	sMode='IndexedImpl'
	sCurrentWord='caudiodata_allocate'
	_searchSip(sMode, sPath, sCurrentWord, sHomedir, sLnzPath)
	#~ print
