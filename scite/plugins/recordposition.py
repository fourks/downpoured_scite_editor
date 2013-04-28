# SciTE Python Extension
# Ben Fisher, 2011

from CScite import ScEditor, ScOutput, ScApp

maxlen=128
g_bufferPositions=[]
#file maps to position

def recordposition():
	sfile = ScApp.GetFilePath().lower()
	curline = ScEditor.LineFromPosition(ScEditor.GetCurrentPos())
	if len(g_bufferPositions)>0:
		latest = g_bufferPositions[-1]
		if latest == (sfile, curline):
			return
	
	
	#~ print 'saved '+str(curline) 
	
	#~ if len(bufferPositions[sfile][1]) > 0 and abs(bufferPositions[sfile][1][-1] - curline)<=2:
		#~ pass #we already recorded this line, or something close to it
	#~ else:
		#~ bufferPositions[sfile][1].append(curline)
		#~ bufferPositions[sfile][0] = len(bufferPositions[sfile][1]) - 1
	

def goBack(bGlobal=False):
	#look for one with same filename
	sfile = ScApp.GetFilePath().lower()
	if sfile not in bufferPositions: return
	bufferPositions[sfile][0] -= 1
	if bufferPositions[sfile][0]<0: bufferPositions[sfile][0]=0
	index = bufferPositions[sfile][0]
	ScEditor.GotoLine(bufferPositions[sfile][1][index])
	
def goForward(bGlobal=False):
	sfile = ScApp.GetFilePath().lower()
	if sfile not in bufferPositions: return
	bufferPositions[sfile][0] += 1
	if bufferPositions[sfile][0]>=len(bufferPositions[sfile][1]): bufferPositions[sfile][0]=len(bufferPositions[sfile][1])
	index = bufferPositions[sfile][0]
	ScEditor.GotoLine(bufferPositions[sfile][1][index])
	
	
