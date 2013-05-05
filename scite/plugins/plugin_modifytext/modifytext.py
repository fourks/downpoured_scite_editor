# SciTE Python Extension
# Ben Fisher, 2011

from CScite import ScEditor, ScOutput, ScApp

def combineLines(ssel):
    arlines = ssel.replace('\r\n', '\n').replace('\r','\n').split('\n')
    arlines = [s.strip() for s in arlines]
    return '; '.join(arlines)

def putArgsOnDifferentLines(ssel):
    if not ( ssel.count('(') == 1 and ssel.count(')') == 1):
        print 'No parens found. Expected something in the form (int a, int b, int c)'
        return None
    sbefore = ssel[0:ssel.index('(')+1]
    sinside = ssel[ssel.index('(')+1:ssel.index(')')]
    safter = ssel[ssel.index(')'):]
    sinside = sinside.replace(', ', ',\r\n\t')
    srep = sbefore + '\r\n\t' + sinside + safter
    return srep
    
def sortLines(ssel, bReverse):
    lineend = '\r\n' if '\r\n' in ssel else '\n'
    arlines = ssel.replace('\r\n', '\n').replace('\r','\n').split('\n')
    arlines.sort()
    if bReverse: arlines.reverse()
    return lineend.join(arlines)

def getLineCount():
    print ScEditor.GetLineCount()

def main():
    import scmsg
    ssel = ScEditor.GetSelText()
    if not ssel: print 'no text selected.'; return
    sret = None
    
    n = scmsg.getChoiceShowDialog('Modify text:', 
        ['sort', 'reverse sort','combine lines','args on lines'] )
    if n==0:
        sret = sortLines(ssel, False)
    elif n==1:
        sret = sortLines(ssel, True)
    elif n==2:
        sret = combineLines(ssel)
    elif n==3:
        sret = putArgsOnDifferentLines(ssel)
    
    if sret:
        ScEditor.BeginUndoAction()
        ScEditor.Clear()
        ScEditor.InsertText(sret, ScEditor.GetCurrentPos())
        ScEditor.SetAnchor(ScEditor.GetCurrentPos() + len(sret))
        #don't use Write. we want it all selected
        ScEditor.EndUndoAction()



