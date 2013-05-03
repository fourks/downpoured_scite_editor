# SciTE Python Extension
# Ben Fisher, 2011
# records line position, so that you can navigate more easily in a large document
# (you can go 'back' and 'forward' to where you have made edits with Ctrl+minus)

from CScite import ScEditor, ScOutput, ScApp
import collections
bVerbose = False

# use 'undo stack' logic to hold positions
class UndoStack(object):
    m_stack=None
    m_stacklen=0
    m_index=0
    maxlen=64
    
    def __init__(self):
        # i'm only using this as a list where removing the first element is efficient.
        self.m_stack = collections.deque()
        
    def push(self, obj):
        if self.m_index == self.m_stacklen:
            self.m_stack.append(obj)
            self.m_stacklen += 1
            if bVerbose: print 'push top ',self.m_index,self.m_stacklen
            if self.m_stacklen > self.maxlen:
                self.m_stack.popleft() # removes first element
                self.m_stacklen -= 1
                self.m_index -= 1
        else:
            #reset it
            self.m_stack[self.m_index] = obj
            self.m_stacklen = self.m_index+1
            if bVerbose: print 'push reset ',self.m_index,self.m_stacklen
        self.m_index += 1
        
    def undo(self):
        if (self.m_index <= 1): return;
        self.m_index-=1
        obj = self.m_stack[self.m_index-1]
        if bVerbose: print 'undo ',self.m_index, self.m_stacklen
        return obj
        
    def redo(self):
        if (self.m_index >= self.m_stacklen): return;
        self.m_index+=1
        obj = self.m_stack[self.m_index-1]
        if bVerbose: print 'redo ',self.m_index, self.m_stacklen
        return obj
    
    def gettop(self):
        return None if len(self.m_stack)==0 else self.m_stack[self.m_index-1]

g_positionHistory=UndoStack()

def recordposition():
    sfile = ScApp.GetFilePath().lower()
    curline = ScEditor.LineFromPosition(ScEditor.GetCurrentPos())
    
    latestFromHistory = g_positionHistory.gettop()
    if not latestFromHistory or (latestFromHistory[0] != sfile or abs(latestFromHistory[1] - curline)>2):
        if bVerbose: print 'recording'
        g_positionHistory.push((sfile, curline))
    else:
        if bVerbose: print 'too close to record'
    
def goBack():
    if not g_positionHistory.gettop(): return
    
    obj = g_positionHistory.undo()    
    if obj:
        ScApp.OpenFile(obj[0])
        ScEditor.GotoLine(obj[1])
    
def goForward():
    if not g_positionHistory.gettop(): return
    
    obj = g_positionHistory.redo()
    if obj:
        ScApp.OpenFile(obj[0])
        ScEditor.GotoLine(obj[1])
    
    
