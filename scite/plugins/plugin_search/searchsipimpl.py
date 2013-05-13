
import re
import searchutil
from searchutil import SipException

Resulttypes = searchutil.make_enum('OTHER_HIT','CLASS_DEFN','STRUCT_DEFN',
'IFACE_DEFN', 'IFACE_DEFN', 'ENUM_DEFN', 'CSTYLE_DEFN', 'TYPEDEF_DEFN',
'MACRO_DEFN', 'CONSTR_IMPL', 'METHOD_EITHER', 'VAR_EITHER')

Searchmodes = searchutil.make_enum('ALL_EXCEPT_COMMENTS', 'SEARCH_IMPLS', 'SEARCH_DEFNS')

def filterEliminateWhereTrue(ar, fn):
    arTmp = [item for item in ar if not fn(item)]
    if len(arTmp)==0 and len(ar)>0: print 'Only results:'; return ar
    else: return arTmp

def filter(sMode, sQuery, rawresults):
    searchutil.checkSupportedString(sQuery)
    arResults = []
    
    # tag each hit as a type
    txt = rawresults.replace('\r\n','\n')
    for line in txt.split('\n'):
        if line.startswith('error:') or line.startswith('warning:'):
            print line
        elif line.count('\\')==0:
            print '(no filepath found?)', line
        else:
            path, num, context = pullapartline(line)
            context = searchutil.killcomments(context)
            ret = determineResultType(sQuery, context, path)
            if ret:
                arResults.append((ret, line, path))
    
    arResults = filterEliminateWhereTrue(arResults, lambda item: item[0]==None)
    if sMode==Searchmodes.SEARCH_DEFNS or sMode==Searchmodes.SEARCH_IMPLS:
        arResults = filterEliminateWhereTrue(arResults, lambda item: item[0]=='OTHER_HIT')
        if sMode==Searchmodes.SEARCH_DEFNS:
            mult = -1
            # kill constructor impl
            arResults = filterEliminateWhereTrue(arResults, lambda item: item[0]=='CONSTR_IMPL')
            # if it could be either, but is in a .c, don't show it.
            arResults = filterEliminateWhereTrue(arResults, lambda item: item[0]=='METHOD_EITHER' and not searchutil.isHeader(item[2]))
            
        elif sMode==Searchmodes.SEARCH_IMPLS:
            mult = 1
            # kill methods that end with ');'
            arResults = filterEliminateWhereTrue(arResults, lambda item: 
                item[0]=='METHOD_EITHER' and (item[1].rstrip().endswith(');') or item[1].rstrip().endswith(') ;')))
        
        # sort by headers first if that, else other.
        arResults.sort(key=lambda item: mult if searchutil.isHeader(item[2]) else 0)
        
        # other ideas:
        # if looking for an implementation and there's one without an extern, show that one?
        # ideally, if there's a paired method+impl, only show the right one...
        
    elif sMode==Searchmodes.ALL_EXCEPT_COMMENTS:
        pass
        
    else:
        raise SipException("unknown mode")
        
    return arResults

def displayResults(arResults):
    if not len(arResults):
        print 'No results found.'
    else:
        for res in arResults:
            print res[1],res[0]

def pullapartline(line):
    line=line.strip()
    if ':' not in line: return
    first, rest = line[0:2], line[2:]
    path, num, context = rest.split(':',2)
    path = first+path
    return path, int(num), context
    

def determineResultType(sQuery, sResultLineOrig, path):
    # enum, typedef, macro, class, struct, interface, method, inline method, global function, inline fn, global variable, member vars
    # we are -not- parsing the code. simple, common cases only!
    # todo later:enumconstant, fn ptrs, destructors
    if not sResultLineOrig: return None
    bWasIndented = sResultLineOrig[0]==' ' or sResultLineOrig[0]=='\t'
    s = sResultLineOrig.strip()
    if not s:
        return None #this can happen if the line was all comment, say.
    s = s.replace('\t', ' ')
    s = re.sub(' +', ' ', s)
    
    def starts(sinput): return s.startswith(sinput)
    def ends(sinput): return s.endswith(sinput)
    def contains(sinput): return sinput in s
    def containsre(sinput): return re.search(sinput, s)!=None
    
    #class
    sspace = s+' '
    if sspace.startswith('class '+sQuery+' ') and not contains(';'):
        return Resulttypes.CLASS_DEFN
    if sspace.startswith('struct '+sQuery+' ') and not contains(';'):
        return Resulttypes.STRUCT_DEFN
    if sspace.startswith('interface '+sQuery+' ') and not contains(';'):
        return Resulttypes.IFACE_DEFN
    if starts('DECLARE_INTERFACE('+sQuery+' ') or starts('DECLARE_INTERFACE( '+sQuery+' '):
        return Resulttypes.IFACE_DEFN
    
    #enum. no forward declarations
    if sspace.startswith('enum '+sQuery+' ') or sspace.startswith('typedef enum '+sQuery+' '):
        if not contains(';') or (contains('{') and contains('}')):
            return Resulttypes.ENUM_DEFN
    
    # c-style definitions like typedef struct {a, b...} StructT;
    if starts('} ') and ends(';') and not (contains('=') or contains('(') 
        or contains(')') or contains('.') or contains('>')):
        return Resulttypes.CSTYLE_DEFN
    
    # typedef
    if starts('typedef ') and containsre('\\b'+sQuery+' *;'):
        return Resulttypes.TYPEDEF_DEFN
    
    #macro
    if sspace.startswith('#define '+sQuery+' ') or starts('#define '+sQuery+'('):
        return Resulttypes.MACRO_DEFN
    
    if containsre('\\b'+sQuery+'::'+sQuery+' *\(') and not contains(';'):
        return Resulttypes.CONSTR_IMPL
    if starts('void '+sQuery+'::Init(') or starts('void '+sQuery+'::Init '):
        return Resulttypes.CONSTR_IMPL
    if starts('bool '+sQuery+'::FInit(') or starts('bool '+sQuery+'::FInit '):
        return Resulttypes.CONSTR_IMPL
    
    # how to identify a method:
    # after stripping parens and templates, it basically looks like
    # worda wordb sQuery
    # and nothing else.
    # (might not match old-style C fns).
    
    if sQuery+' (' in s: s=s.replace(sQuery+' (', sQuery+'(')
    if sQuery+'(' in s and not starts(sQuery+'('):
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
            #sregexp = r'([a-zA-Z0-9_*~&:]+ +)+[^a-zA-Z0-9_]*'+sQuery
            #instead, blacklist
            #remember to write \- inside a char class
            #match() must match start of string
            sregexp = r"([^./+\-!#%={}|',?]+ +)+[^a-zA-Z0-9_]*([a-zA-Z0-9_:]*::)?"+sQuery+' *;?$'
            if re.match(sregexp, stmp):
                if '[' not in s and '->' not in s and '.' not in s:
                    return Resulttypes.METHOD_EITHER
    
    #global var: indent is 0.
    if not bWasIndented and ends(';'):
        stmp = s.split('=')[0]
        spacestmp = ' '+stmp
        if not (' class ' in spacestmp) and not (' struct '  in spacestmp) and not \
        (' interface ' in spacestmp) and not (' enum ' in spacestmp) and not (' new ' in spacestmp) and not (' typedef ' in spacestmp):
            
            stmp = searchutil.killparens(stmp)
            stmp = searchutil.killbrackets(stmp)
            # sregexp=r'.*? *'+sQuery+' *;?'
            sregexp=r"([^./+\-!#%={}|',?]+ +)+[^a-zA-Z0-9_]*"+sQuery+' *;?$'
            if re.match(sregexp, stmp):
                return Resulttypes.VAR_EITHER
    
    return Resulttypes.OTHER_HIT

if __name__=='__main__':
    assert re.sub(' +', ' ', 'a  b  c  d       f') == 'a b c d f'
    
    def test1():
        print 'test1'
        def dotest(sExpect, sQuery, sLine):
            ret = determineResultType(sQuery, sLine, 'foo.h')
            searchutil.assertEqual(ret, sExpect)
        
        # we don't count parameters, so something like
        # Foo Bar(a);
        # looks like either a variable Foo or a function declaration for Bar
        
        dotest('METHOD_EITHER', 'ReadXMLEndTag', '  void ReadXMLEndTag(const char *tag);')
        dotest('METHOD_EITHER', 'ReadXMLEndTag', '  void ReadXMLEndTag(const char *tag) {')
        dotest('METHOD_EITHER', 'ReadXMLEndTag', 'void ReadXMLEndTag(const char *tag) { foo=bar; return 7;}')
        dotest('METHOD_EITHER', 'ReadXMLEndTag', '  void ReadXMLEndTag(')
        dotest('METHOD_EITHER', 'ReadXMLEndTag', '  void* ReadXMLEndTag(')
        dotest('METHOD_EITHER', 'ReadXMLEndTag', '  void *ReadXMLEndTag(')
        dotest('METHOD_EITHER', 'ReadXMLEndTag', '  int& ReadXMLEndTag(')
        dotest('METHOD_EITHER', 'ReadXMLEndTag', '  void ReadXMLEndTag(int a=5')
        dotest('METHOD_EITHER', 'ReadXMLEndTag', '  foo<a.5, h<c>> ReadXMLEndTag(')
        dotest('METHOD_EITHER', 'ReadXMLEndTag', '  void<a, 45=17> ReadXMLEndTag(')
        dotest('METHOD_EITHER', 'ReadXMLEndTag', '  int Cool::ReadXMLEndTag(')
        dotest('METHOD_EITHER', 'ReadXMLEndTag', '  int O::Var::Cool::ReadXMLEndTag(')
        dotest('METHOD_EITHER', 'ReadXMLEndTag', '  int *O::Var::Cool::ReadXMLEndTag(')
        dotest('METHOD_EITHER', 'ReadXMLEndTag', '  int[] Cool::ReadXMLEndTag(')
        dotest('METHOD_EITHER', 'ReadXMLEndTag', '  SOME_MACRO(foo, bar) int Cool::ReadXMLEndTag(')
        dotest('METHOD_EITHER', 'ReadXMLEndTag', '  OTHERMACRO(foo) Cool::ReadXMLEndTag(')
        dotest('METHOD_EITHER', 'ReadXMLEndTag', '  int Cool::ReadXMLEndTag(')
        dotest('METHOD_EITHER', 'ReadXMLEndTag', 'void XMLTagHandler::ReadXMLEndTag(const char *tag)')
        dotest('OTHER_HIT', 'ReadXMLEndTag', '  SomeStatic::ReadXMLEndTag();')
        dotest('OTHER_HIT', 'ReadXMLEndTag', '  Var::SomeStatic::ReadXMLEndTag();')
        dotest('OTHER_HIT', 'ReadXMLEndTag', '  void aReadXMLEndTag(')
        dotest('OTHER_HIT', 'ReadXMLEndTag', '  void ReadXMLEndTag() ReadXMLEndTagaaa(')
        dotest('OTHER_HIT', 'ReadXMLEndTag', '  void ReadXMLEndTag() aaaReadXMLEndTag(')
        dotest('OTHER_HIT', 'ReadXMLEndTag', 'return XMLTagHandler::ReadXMLEndTag(*tag)')
        dotest('OTHER_HIT', 'ReadXMLEndTag', 'new XMLTagHandler::ReadXMLEndTag(*tag)')
        dotest('OTHER_HIT', 'ReadXMLEndTag', 'This->mHandler[This->mDepth]->ReadXMLEndTag(name);')
        dotest('OTHER_HIT', 'ReadXMLEndTag', 'obj->ReadXMLEndTag(name);')
        dotest('OTHER_HIT', 'ReadXMLEndTag', 'return obj.ReadXMLEndTag(name);')
        dotest('OTHER_HIT', 'ReadXMLEndTag', 'void. ReadXMLEndTag(const char *tag);')
        dotest('OTHER_HIT', 'ReadXMLEndTag', 'ReadXMLEndTag();')
        dotest('CLASS_DEFN', 'CFoo', 'class CFoo')
        dotest('CLASS_DEFN', 'CFoo', '  class CFoo {')
        dotest('CLASS_DEFN', 'CFoo', 'class CFoo : public CBar')
        dotest('OTHER_HIT', 'CFoo', 'class CFoo;')
        dotest('OTHER_HIT', 'CFoo', '  class CFoo ;')
        dotest('OTHER_HIT', 'CFoo', 'not class CFoo')
        dotest('STRUCT_DEFN', 'TFoo', 'struct TFoo')
        dotest('STRUCT_DEFN', 'TFoo', 'struct TFoo { foo')
        dotest('OTHER_HIT', 'TFoo', 'struct TFoo { int a; }') #we don't support one-line structs
        
        dotest('ENUM_DEFN', 'ETest', 'enum ETest')
        dotest('ENUM_DEFN', 'ETest', 'enum ETest {a,b,c};')
        dotest('ENUM_DEFN', 'ETest', ' enum ETest { ')
        dotest('ENUM_DEFN', 'ETest', ' typedef   enum    ETest { ')
        dotest('OTHER_HIT', 'ETest', ' enum ETest ;')
        dotest('OTHER_HIT', 'ETest', ' enum ETest;')
        dotest('CSTYLE_DEFN', 'LAME_QUALTIY_PRESET', ' } LAME_QUALTIY_PRESET;')
        dotest('CSTYLE_DEFN', 'PLAME_QUALTIY_PRESET', ' } LAME_QUALTIY_PRESET, *PLAME_QUALTIY_PRESET;')
        dotest('CSTYLE_DEFN', 'LAME_QUALTIY_PRESET', '} LAME_QUALTIY_PRESET, *PLAME_QUALTIY_PRESET;')
        dotest('OTHER_HIT', 'LAME_QUALTIY_PRESET', ' { } LAME_QUALTIY_PRESET;')
        dotest('OTHER_HIT', 'LAME_QUALTIY_PRESET', ' } LAME_QUALTIY_PRESET();')
        dotest('TYPEDEF_DEFN', 'MType', 'typedef int MType ;')
        dotest('TYPEDEF_DEFN', 'MType', 'typedef int MType;')
        dotest('TYPEDEF_DEFN', 'MType', 'typedef int *MType;')
        dotest('TYPEDEF_DEFN', 'MType', 'typedef int* **MType ;')
        dotest('TYPEDEF_DEFN', 'MType', 'typedef crazy<a,bbb> { #%#$%$ } MType ;')
        dotest('VAR_EITHER', 'MType', 'typedeftheint MType;')
        dotest('OTHER_HIT', 'MType', 'typedef int aMType;')
        dotest('MACRO_DEFN', 'mcro', '#define mcro')
        dotest('MACRO_DEFN', 'mcro', '#define mcro 5')
        dotest('MACRO_DEFN', 'mcro', '#define mcro mcro')
        dotest('MACRO_DEFN', 'mcro', '#define mcro(here')
        dotest('OTHER_HIT', 'mcro', 'a #define mcro 5')
        dotest('OTHER_HIT', 'mcro', '#define mcrono')
        dotest('OTHER_HIT', 'mcro', '#define nomcro')
        
        dotest('VAR_EITHER', 'foo', 'extern int foo;')
        dotest('VAR_EITHER', 'foo', 'int foo;')
        dotest('VAR_EITHER', 'foo', 'const int foo=4;')
        dotest('VAR_EITHER', 'foo', 'const int foo = 4;')
        dotest('VAR_EITHER', 'foo', 'int foo = {4};')
        dotest('VAR_EITHER', 'foo', 'int foo = bar;')
        dotest('VAR_EITHER', 'foo', 'int* foo = bar;')
        dotest('VAR_EITHER', 'foo', 'int *foo;')
        dotest('VAR_EITHER', 'foo', 'int *foo=bar;')
        dotest('VAR_EITHER', 'foo', 'int **foo;')
        dotest('VAR_EITHER', 'foo', 'int &foo = bar;')
        dotest('VAR_EITHER', 'foo', 'CNotastruct foo;')
        dotest('VAR_EITHER', 'foo', 'int foo[];')
        dotest('VAR_EITHER', 'foo', 'int foo[256];')
        dotest('VAR_EITHER', 'foo', 'int foo[bufsize];')
        dotest('VAR_EITHER', 'foo', 'int foo[] = {0};')
        dotest('VAR_EITHER', 'm_nMember', 'int m_nMember;')
        dotest('VAR_EITHER', 'm_nMember', 'int<hg<ok> > m_nMember;')
        dotest('METHOD_EITHER', 'foo', 'int foo(bar);') #ok; looks kind of like a method
        dotest('OTHER_HIT', 'foo', 'int afoo;')
        dotest('OTHER_HIT', 'foo', 'int foon;')
        dotest('OTHER_HIT', 'f', 'int foon;')
        dotest('OTHER_HIT', 'foo', 'int foon=4;')
        dotest('OTHER_HIT', 'foo', 'int bar = foo;')
        dotest('OTHER_HIT', 'foo', 'int bar(foo);')
        dotest('CONSTR_IMPL', 'CFoo', 'CFoo::CFoo()')
        dotest('CONSTR_IMPL', 'CFoo', 'CFoo::CFoo ()')
        dotest('CONSTR_IMPL', 'CFoo', 'CFoo::CFoo() {')
        dotest('CONSTR_IMPL', 'CFoo', 'CFoo::CFoo() { a=5; }')
        dotest('CONSTR_IMPL', 'CFoo', 'CFoo::CFoo(int j, bool b) {')
        dotest('METHOD_EITHER', 'CFoo', 'void CFoo1::CFoo() {')
        dotest('OTHER_HIT', 'CFoo', 'CFoo::CFoob() {')
        dotest('OTHER_HIT', 'CFoo', 'CFoob::CFoo () {')        
        dotest('METHOD_EITHER', 'OnOK', 'static void OnOK(wxCommandEvent & event);')
        
        
    test1()

