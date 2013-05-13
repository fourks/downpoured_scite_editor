# SciTE Python Extension
# Ben Fisher, 2011

sExplain = '''

This plugin can be used to quickly
add numbers or patterns.
If you want to generate
var a0 = "0";
var a1 = "1";
var a2 = "2";
var a3 = "3";

first type
var a@ = "@";
var a@ = "@";
var a@ = "@";
var a@ = "@";
, select these lines, and press
Ctrl+Shift+2.

If you want to generate
bool bRed = darkRed || lightRed;
bool bGreen = darkGreen || lightGreen;
bool bBlue = darkBlue || lightBlue;

first type
bool b@Red@ = dark@@ || light@@;
bool b@Green@ = dark@@ || light@@;
bool b@Blue@ = dark@@ || light@@;
, select these lines, and press
Ctrl+Shift+2.'''

def atReplaceImpl(ssel):
    sOut = None
    if not ssel:
        print 'No selection'
        print sExplain
        return
    if '@@@'  in ssel:
        print '@@@ is invalid.'
        print sExplain
        return
    if not '@'  in ssel:
        print 'No @ seen.'
        print sExplain
        return
    
    crlf = '\r\n' if '\r' in ssel else '\n'
    bIsNumeric = not '@@' in ssel
    if bIsNumeric:
        nNumber=-1
        sIn = ssel.split(crlf)
        for i in range(len(sIn)):
            if '@' in sIn[i]: nNumber+= 1
            sIn[i] = sIn[i].replace('@', str(nNumber))
        sOut = crlf.join(sIn)
    else:
        #~ assert '\r' not in ssel
        sIn = ssel.replace('\\'+crlf,'\\\\_\\\\')
        sIn = sIn.split(crlf)
        marker = '$!$__mrk$$'
        assert marker not in ssel
        for i in range(len(sIn)):
            if '@' not in sIn[i]: continue
            sTmp = sIn[i]
            sTmp = sTmp.replace('@@',marker)
            astmp = sTmp.split('@')
            if len(astmp)!=3:
                print 'Invalid number of single @. '+sExplain
                return
            thepiece = astmp[1]
            astmp[0] = astmp[0].replace(marker, thepiece)
            astmp[2] = astmp[2].replace(marker, thepiece)
            sIn[i] = astmp[0] + thepiece + astmp[2]
        sOut = crlf.join(sIn)
        sOut = sOut.replace('\\\\_\\\\', crlf)

    return sOut
    
def atReplace():
    from CScite import ScEditor, ScOutput, ScApp
    
    ssel = ScEditor.GetSelText()
    sOut = atReplaceImpl(ssel)
    if sOut:
        ScEditor.BeginUndoAction()
        ScEditor.Clear()
        ScEditor.InsertText(sOut, ScEditor.GetCurrentPos())
        ScEditor.SetAnchor(ScEditor.GetCurrentPos() + len(sOut))
        #don't use Write. we want it to be selected
        ScEditor.EndUndoAction()


if __name__=='__main__':
    stest1 = 'var a@ = "@";\nvar a@ = "@";\nvar a@ = "@";\nvar a@ = "@";\n'
    stest1ret = atReplaceImpl(stest1)
    assert stest1ret == 'var a0 = "0";\nvar a1 = "1";\nvar a2 = "2";\nvar a3 = "3";\n'
    
    stest2 = 'bool b@Red@ = dark@@ || light@@;\nbool b@Green@ = dark@@ || light@@;\nbool b@Blue@ = dark@@ || light@@;'
    stest2ret = atReplaceImpl(stest2)
    assert stest2ret == 'bool bRed = darkRed || lightRed;\nbool bGreen = darkGreen || lightGreen;\nbool bBlue = darkBlue || lightBlue;'
    
    # use backslash to hide a newline
    stest3 = r'''
dark@red@ = @@*0.3;\
newcolors.add(dark@@);
dark@green@ = @@*0.3;\
newcolors.add(dark@@);'''
    stest3ret = atReplaceImpl(stest3)
    assert stest3ret=='\ndarkred = red*0.3;\nnewcolors.add(darkred);\ndarkgreen = green*0.3;\nnewcolors.add(darkgreen);'
    
    print 'tests pass.'