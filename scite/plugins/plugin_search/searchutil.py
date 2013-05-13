import exceptions
import subprocess
import re, os

class SipException(exceptions.RuntimeError): pass

def checkSupportedString(s):
    if len(s)==1:
        raise SipException("No results! We don't index single characters.")
    if not s or not re.match(r'[a-zA-Z0-9_]+$', s):
        raise SipException("No results! Input can't contain punctuation or spaces.")

def assertEqual(v, vExpected):
    if v != vExpected:
        print 'Fail: Expected '+str(vExpected) + ' but got '+str(v)
        raise exceptions.RuntimeError, 'stop'
def assertNotEqual(v, vExpected):
    if v == vExpected:
        print 'Fail: Expected '+str(v) + ' to not equal '+str(vExpected)
        raise exceptions.RuntimeError, 'stop'
def assertContains(s, subs):
    if subs not in s:
        print 'Fail: "'+str(subs) + '" not found in "'+str(s)+'"'
        raise exceptions.RuntimeError, 'stop'
        
def _runReturn(sExe, listArgs):
    listArgs = list(listArgs) #copy the list, so we don't modify arg.
    listArgs.insert(0, sExe)
    sp = subprocess.Popen(listArgs, shell=False, stdout=subprocess.PIPE)
    text = sp.communicate()[0]
    return text.rstrip(), sp.returncode
def runReturnStdout(sExe, listArgs):
    txt, retcode = _runReturn(sExe, listArgs)
    if int(retcode)!=0:
        print txt
        raise SipException("Retcode indicates failure")
    return txt
def getString(shome, lnzpath):
    listArgs = [lnzpath, os.path.join(os.path.join(shome, 'plugins'), 'getdialog.jsz') ]
    sp = subprocess.Popen(listArgs, shell=False, stdout=subprocess.PIPE)
    text = sp.communicate()[0]
    return text.strip()

def isHeader(path):
    return path.endswith('.h') or path.endswith('.H')

def make_enum(*sequential, **named):
    enums = dict(zip(sequential, sequential), **named)
    return type('PyEnum', (), enums)

def killcomments(s):
    s = re.sub(r'/\*(.+?)\*/', '', s)
    s = re.sub(r'/\*.*', '', s) #unbalanced /* should still be removed
    s = re.sub(r'//.*', '', s, 1)
    #kill string literals
    s=s.replace('\\"', '\\\\')
    s = re.sub(r'"(.+?)"', '""', s)
    # unbalanced " are possible, as newline can be escaped, but problably not likely
    return s

def killbalanced(s, l, r):
    # can't use greedy regexp "foo<x> and foo<y> end" -> "foo end"
    # can't use nongreedy regexp "foo<x, y<z>>end' -> 
    out = []
    level = 0
    for c in s:
        if c==l: level +=1
        if level==0:
            out.append(c)
        if c==r: level -=1
    return ''.join(out)
def killtemplates(s): return killbalanced(s, '<', '>')
def killparens(s): return killbalanced(s, '(', ')')
def killbraces(s): return killbalanced(s, '{', '}')
def killbrackets(s): return killbalanced(s, '[', ']')
    
def getprojsection(ininame, sInputPath):
    sInputPath = sInputPath.lower()
    if not os.path.exists(ininame): return None
    projname = None
    thissection = []
    matchFound = False
    curname = None
    f=open(ininame, 'r')
    for line in f:
        if line.startswith('['):
            if matchFound: break
            assert line.strip().endswith(']')
            curname = line.strip().replace('[','').replace(']','')
            thissection = []
        else:
            thissection.append(line)
            if line.startswith('srcdir'):
                assert '=' in line
                thedir = line.split('=',1)[1].strip().lower()
                if len(thedir)>3 and sInputPath.startswith(thedir):
                    matchFound = True
    if matchFound:
        return curname, '[main]\n'+''.join(thissection)
    else:
        return None


if __name__=='__main__':
    assertEqual(killcomments('fhg'), 'fhg')
    assertEqual(killcomments('fh//no moreg'), 'fh')
    assertEqual(killcomments('balanced/*here*/y/*but not here'), 'balancedy')
    assertEqual(killcomments(r'fh/*no*/ but "string" ok /*nooot*/ moreg "st\"colr"'), 
        'fh but "" ok  moreg ""')
    assertEqual(killtemplates("foo<x> and foo<y> end"), 'foo and foo end')
    assertEqual(killtemplates("foo<x, y<z>>end h<h>"), 'fooend h')
    
    assert getprojsection('projects.cfg', r'c:\test')==None
    assert getprojsection('projects.cfg', r'cpp')==None
    print getprojsection('projects.cfg', r'C:\pydev\dev\downpoured_scite_editor\scite\src\scite')
    print getprojsection('projects.cfg', r'C:\pydev\dev\downpoured_scite_editor\scite\Src\Scite')
    print getprojsection('projects.cfg', r'C:\pydev\dev\downpoured_scite_editor\scite\Src\Scite\foo\bar')
    print getprojsection('projects.cfg', r'C:\pydev\dev\downpoured_scite_editor\tools\simple_source_index\nocpy_older\01 Read_c_stuff\read_c_and_stuff\foo')
    print getprojsection('projects.cfg', r'C:\fastdev\fastpixel\fastsecond\unittests\test\6')
    
