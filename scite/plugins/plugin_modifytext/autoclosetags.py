# SciTE Python Extension
# Ben Fisher, 2011

# while you are typing, turn something like <a> into <a></a>
# and turn something like <br> into <br />
# future possibilities
#   auto-close parens
#   auto-close { and }

# a bug in pythonext drops last character.
useLexers = ('xm','hypertex','xml','hypertext')
xhtmlsingletons= ('br', 'img', 'hr')

def getCharAt(fnGetTextRange, n):
    return fnGetTextRange(n,n+1)

def getCurrentTag():
    from CScite import ScEditor, ScOutput, ScApp
    import math
    fnGetTextRange = ScEditor.Textrange
    pos = ScEditor.GetCurrentPos()-1
    firstpos = pos
    lastpos = max(pos - 300, 0)
    tagname = ''
    
    while pos > lastpos:
        pos = pos-1
        
        ch = getCharAt(fnGetTextRange, pos)
        if ch=='>' or ch=="\n":
            break
        elif ch=='<':
            pos = pos+1
            # Now look forward
            while pos < firstpos:
                newch = getCharAt(fnGetTextRange, pos)
                if newch==' ' or newch=='>' or newch=='/':
                    break
                tagname = tagname + newch
                pos = pos+1
            
            break
    return tagname


def autoclosetags(nChar):
    # respond only to > characters in an html or xml doc.
    if nChar!=62: return
    from CScite import ScEditor, ScOutput, ScApp
    lexername = ScEditor.GetLexerLanguage()
    if lexername not in useLexers: return
    
    currenttag = getCurrentTag()
    if not currenttag: return
        
    # found an xml/html tag!
    prevpos = ScEditor.GetCurrentPos()
    
    # turn something like <br> into <br />
    if currenttag in xhtmlsingletons:
        if getCharAt(ScEditor.Textrange, prevpos-1)!='/':
            ScEditor.Remove(prevpos-1, prevpos)
            ScEditor.ReplaceSel(' />')
            
    # turn something like <a> into <a></a>
    else:
        ScEditor.ReplaceSel('</'+currenttag+'>')
        ScEditor.GotoPos(prevpos)
    
