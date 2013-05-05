
import re
import searchutil
from searchutil import assertEqual, assertContains, assertNotEqual, SipException

def checkStringOk(s):
    if len(s)==1:
        raise SipException("No results! We don't index single characters.")
    if not s or not re.match(r'[a-zA-Z0-9_]+$', s):
        raise SipException("No results! Input can't contain punctuation or spaces.")
def IsHeader(path):
    return path.endswith('.h') or path.endswith('.H')
def filter(sMode, s, rawresults):
    checkStringOk(s)
    obj = FilterResults_Looking()
    obj.sT = s
    
    arResults = []
    
    # tag each hit as a type
    txt = rawresults.replace('\r\n','\n')
    for line in txt.split('\n'):
        if line.count('\\')==0:
            print 'Info: ',line
        else:
            path, num, context = pullapartline(line)
            context = searchutil.killcomments(context)
            ret = obj.lookAtLine(context, path)
            arResults.append((ret, line, path))
    
    def filterButNotAllHits(ar, fn):
        arTmp = [item for item in ar if fn(item)]
        if len(arTmp)==0 and len(ar)>0: print 'Only results:'
        else: ar = arTmp
        return ar
    
    # further filtering based on mode
    if sMode=='IndexedOther':
        # keep only the None results
        arResults = filterButNotAllHits(arResults, lambda item: item[0]==None)
    elif sMode=='IndexedDefn' or sMode=='IndexedImpl':
        arResults = filterButNotAllHits(arResults, lambda item: item[0]!=None)
        if sMode=='IndexedDefn':
            mult = -1
            # kill constructor impl
            arResults = filterButNotAllHits(arResults, lambda item: item[0]!='CONSTR_IMPL')
            # defns shouldn't be in src files. the converse does not hold
            arResults = filterButNotAllHits(arResults, lambda item: item[0]!='METHOD_EITHER' or IsHeader(item[2]))
            
        elif sMode=='IndexedImpl':
            mult = 1
            # kill methods that end with ');'
            arResults = filterButNotAllHits(arResults, lambda item: 
                item[0]!='METHOD_EITHER' or not (item[1].rstrip().endswith(');') or item[1].rstrip().endswith(') ;')))
            # kill 'class foo' or 'struct foo'
            arResults = filterButNotAllHits(arResults, lambda item: not (item[0]=='CLASS_DEFN' or item[0]=='STRUCT_DEFN' or item[0]=='IFACE_DEFN'))
        
        # sort by headers first if that, else other. hopefully a stable sort.
        arResults.sort(key=lambda item: mult if IsHeader(item[2]) else 0)
        
        # other ideas:
        # if looking for an implementation and there's one without an extern, show that one?
        # ideally, if there's a paired method+impl, only show the right one...
        
    else:
        raise SipException("unknown mode")
    
    if not len(arResults):
        print 'No results found.'
    else:
        for res in arResults:
            print res[1],res[0]
    
    return arResults
    
def pullapartline(line):
    line=line.strip()
    if ':' not in line: return
    first, rest = line[0:2], line[2:]
    path, num, context = rest.split(':',2)
    path = first+path
    return path, int(num), context
    

class IFilterResults():
    sT=None
    def lookAtLine(self, sLine):
        raise exceptions.RuntimeError, 'Not implemented'

class FilterResults_Looking(IFilterResults):
    sT=None #the user input.
    def lookAtLine(self, sLineOrig, path):
        # enum, typedef, macro, class, struct, interface, method, inline method, global function, inline fn, global variable, member vars
        #we are -not- parsing the code. simple, common cases only!
        #todo later:enumconstant, fn ptrs, destructors
        
        s = sLineOrig.strip()
        if not s:
            return None #this can happen if the line was all comment, say.
        s = s.replace('\t', ' ')
        sT = self.sT
        bWasIndented = s[0]==' '
        
        s = s.replace('  ',' ').replace('  ',' ').replace('  ',' ').replace('  ',' ')
        if '  ' in s:
            raise SipException("That's a lot of spaces in this line")
        
        def starts(sinput): return s.startswith(sinput)
        def ends(sinput): return s.endswith(sinput)
        def contains(sinput): return sinput in s
        
        #class
        sspace = s+' '
        if sspace.startswith('class '+sT+' ') and not contains(';'):
            return 'CLASS_DEFN'
        if sspace.startswith('struct '+sT+' ') and not contains(';'):
            return 'STRUCT_DEFN'
        if sspace.startswith('interface '+sT+' ') and not contains(';'):
            return 'IFACE_DEFN'
        if starts('DECLARE_INTERFACE('+sT+' ') or starts('DECLARE_INTERFACE( '+sT+' '):
            return 'IFACE_DEFN'
        
        #enum. no forward declarations
        sT = self.sT
        if sspace.startswith('enum '+sT+' ') or sspace.startswith('typedef enum '+sT+' '):
            if not contains(';') or (contains('{') and contains('}')):
                return 'ENUM_DEFN'
        
        # c-style definitions
        if starts('} ') and ends(';') and not (contains('=') or contains('(') 
            or contains(')') or contains('.') or contains('>')):
            return 'CSTYLE_DEFN'
        
        #typedef
        if starts('typedef ') and (ends(' '+sT+';') or ends(' '+sT+' ;') or ends('*'+sT+';') or ends('*'+sT+' ;')):
            return 'TYPEDEF_DEFN'
        
        #macro
        if sspace.startswith('#define '+sT+' ') or starts('#define '+sT+'('):
            return 'MACRO_DEFN'
        
        
        if starts(sT+'::'+sT+'(') or starts(sT+'::'+sT+' '):
            #todo: namespace? would anyone ever write Ns::CFoo::CFoo() ?
            return 'CONSTR_IMPL'
        if starts('void '+sT+'::Init(') or starts('void '+sT+'::Init '):
            return 'CONSTR_IMPL'
        if starts('bool '+sT+'::FInit(') or starts('bool '+sT+'::FInit '):
            return 'CONSTR_IMPL'
        
        # how to identify a method:
        # after stripping parens and templates, it basically looks like
        # worda wordb sT
        # and nothing else.
        # (might not match old-style C fns).
        
        if sT+' (' in s: s=s.replace(sT+' (', sT+'(')
        if sT+'(' in s and not starts(sT+'('):
            stmp = s
            stmp = searchutil.killparens(stmp)
            stmp = searchutil.killtemplates(stmp)
            stmp = searchutil.killbraces(stmp) #kill an inline implementation
            stmp=stmp.strip()
            stmp = stmp.replace('  ',' ').replace('  ',' ').replace('  ',' ').replace('  ',' ')
            if '  ' in stmp:
                raise SipException("That's a lot of spaces in this line")
            #~ print 'stmp',stmp
            if '=' not in stmp and ' new ' not in (' '+stmp) and ' return ' not in (' '+stmp):
                #sregexp = r'([a-zA-Z0-9_*~&:]+ +)+[^a-zA-Z0-9_]*'+sT
                #instead, blacklist
                #remember to write \- inside a char class
                #match() must match start of string
                sregexp = r"([^./+\-!#%={}|',?]+ +)+[^a-zA-Z0-9_]*([a-zA-Z0-9_:]*::)?"+sT+' *;?$'
                if re.match(sregexp, stmp):
                    return 'METHOD_EITHER'
        
        #global var: indent is 0.
        if not bWasIndented and ends(';'):
            stmp = s.split('=')[0]
            spacestmp = ' '+stmp
            if not (' class ' in spacestmp) and not (' struct '  in spacestmp) and not \
            (' interface ' in spacestmp) and not (' enum ' in spacestmp) and not (' new ' in spacestmp) and not (' typedef ' in spacestmp):
                
                stmp = searchutil.killparens(stmp)
                stmp = searchutil.killbrackets(stmp)
                # sregexp=r'.*? *'+sT+' *;?'
                sregexp=r"([^./+\-!#%={}|',?]+ +)+[^a-zA-Z0-9_]*"+sT+' *;?$'
                if re.match(sregexp, stmp):
                    return 'VAR_EITHER'
        
        return None


