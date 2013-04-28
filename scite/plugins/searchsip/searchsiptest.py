
def test1():
	print 'test1'
	obj = FilterResults_Looking()
	def dotest(sExpect, sT, sLine):
		obj.sT=sT
		ret = obj.lookAtLine(sLine, 'foo.h')
		assertEqual(ret, sExpect)
	
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
	dotest(None, 'ReadXMLEndTag', '  SomeStatic::ReadXMLEndTag();')
	dotest(None, 'ReadXMLEndTag', '  Var::SomeStatic::ReadXMLEndTag();')
	dotest(None, 'ReadXMLEndTag', '  void aReadXMLEndTag(')
	dotest(None, 'ReadXMLEndTag', '  void ReadXMLEndTag() ReadXMLEndTagaaa(')
	dotest(None, 'ReadXMLEndTag', '  void ReadXMLEndTag() aaaReadXMLEndTag(')
	dotest(None, 'ReadXMLEndTag', 'return XMLTagHandler::ReadXMLEndTag(*tag)')
	dotest(None, 'ReadXMLEndTag', 'new XMLTagHandler::ReadXMLEndTag(*tag)')
	dotest(None, 'ReadXMLEndTag', 'This->mHandler[This->mDepth]->ReadXMLEndTag(name);')
	dotest(None, 'ReadXMLEndTag', 'obj->ReadXMLEndTag(name);')
	dotest(None, 'ReadXMLEndTag', 'return obj.ReadXMLEndTag(name);')
	dotest(None, 'ReadXMLEndTag', 'void. ReadXMLEndTag(const char *tag);')
	dotest(None, 'ReadXMLEndTag', 'ReadXMLEndTag();')
	dotest('CLASS_DEFN', 'CFoo', 'class CFoo')
	dotest('CLASS_DEFN', 'CFoo', '  class CFoo {')
	dotest('CLASS_DEFN', 'CFoo', 'class CFoo : public CBar')
	dotest(None, 'CFoo', 'class CFoo;')
	dotest(None, 'CFoo', '  class CFoo ;')
	dotest(None, 'CFoo', 'not class CFoo')
	dotest('STRUCT_DEFN', 'TFoo', 'struct TFoo')
	dotest('STRUCT_DEFN', 'TFoo', 'struct TFoo { foo')
	dotest(None, 'TFoo', 'struct TFoo { int a; }') #we don't support one-line structs
	
	dotest('ENUM_DEFN', 'ETest', 'enum ETest')
	dotest('ENUM_DEFN', 'ETest', 'enum ETest {a,b,c};')
	dotest('ENUM_DEFN', 'ETest', ' enum ETest { ')
	dotest('ENUM_DEFN', 'ETest', ' typedef   enum    ETest { ')
	dotest(None, 'ETest', ' enum ETest ;')
	dotest(None, 'ETest', ' enum ETest;')
	dotest('CSTYLE_DEFN', 'LAME_QUALTIY_PRESET', ' } LAME_QUALTIY_PRESET;')
	dotest('CSTYLE_DEFN', 'PLAME_QUALTIY_PRESET', ' } LAME_QUALTIY_PRESET, *PLAME_QUALTIY_PRESET;')
	dotest('CSTYLE_DEFN', 'LAME_QUALTIY_PRESET', '} LAME_QUALTIY_PRESET, *PLAME_QUALTIY_PRESET;')
	dotest(None, 'LAME_QUALTIY_PRESET', ' { } LAME_QUALTIY_PRESET;')
	dotest(None, 'LAME_QUALTIY_PRESET', ' } LAME_QUALTIY_PRESET();')
	dotest('TYPEDEF_DEFN', 'MType', 'typedef int MType ;')
	dotest('TYPEDEF_DEFN', 'MType', 'typedef int MType;')
	dotest('TYPEDEF_DEFN', 'MType', 'typedef int *MType;')
	dotest('TYPEDEF_DEFN', 'MType', 'typedef int* **MType ;')
	dotest('TYPEDEF_DEFN', 'MType', 'typedef crazy<a,bbb> { #%#$%$ } MType ;')
	dotest('VAR_EITHER', 'MType', 'typedeftheint MType;')
	dotest(None, 'MType', 'typedef int aMType;')
	dotest('MACRO_DEFN', 'mcro', '#define mcro')
	dotest('MACRO_DEFN', 'mcro', '#define mcro 5')
	dotest('MACRO_DEFN', 'mcro', '#define mcro mcro')
	dotest('MACRO_DEFN', 'mcro', '#define mcro(here')
	dotest(None, 'mcro', 'a #define mcro 5')
	dotest(None, 'mcro', '#define mcrono')
	dotest(None, 'mcro', '#define nomcro')
	
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
	dotest(None, 'foo', 'int afoo;')
	dotest(None, 'foo', 'int foon;')
	dotest(None, 'f', 'int foon;')
	dotest(None, 'foo', 'int foon=4;')
	dotest(None, 'foo', 'int bar = foo;')
	dotest(None, 'foo', 'int bar(foo);')
	dotest('CONSTR_IMPL', 'CFoo', 'CFoo::CFoo()')
	dotest('CONSTR_IMPL', 'CFoo', 'CFoo::CFoo ()')
	dotest('CONSTR_IMPL', 'CFoo', 'CFoo::CFoo() {')
	dotest('CONSTR_IMPL', 'CFoo', 'CFoo::CFoo() { a=5; }')
	dotest('CONSTR_IMPL', 'CFoo', 'CFoo::CFoo(int j, bool b) {')
	dotest('METHOD_EITHER', 'CFoo', 'void CFoo::CFoo() {')
	dotest(None, 'CFoo', 'CFoo::CFoob() {')
	dotest(None, 'CFoo', 'CFoob::CFoo () {')
	
	dotest('METHOD_EITHER', 'OnOK', 'static void OnOK(wxCommandEvent & event);')
	
def main():
	#ok to re-use the db, we're not testing that here.
	#~ if os.path.exists('ssip.db'): os.unlink('ssip.db')
	#~ if os.path.exists('ssip.db'): raise 'need to delete db'
	
	#~ txt, _ = searchutil._runReturnStdout( ('-s', 'BenchmarkDialog'))
	#~ print txt
	#~ txt, _ = searchutil._runReturnStdout( ('-s', 'Envelope'))
	#~ print txt
	#~ txt, _ = searchutil._runReturnStdout( ('-s', 'f'))
	#~ print txt
	tests()
	test1()

def tests():
	#~ path, num, text = pullapartline(r'C:\pydev\pyaudio_here\SimpleSourceIndexing\prior\02 index_line_number\simplesourceindexing\unittest.c:157:	//TestDbAccess();no:here')
	#~ print pullapartline(r'\\pydev\pyaudio_here\SimpleSourceIndexing\prior\02 index_line_number\simplesourceindexing\unittest.c:157:	//TestDbAccess();no:here')
	#~ ret = Go_LookForDefinition('DitherType')
	#~ assertEqual(len(ret), 1)
	#~ assertEqual(ret[0][0], 'ENUM_DEFN')
	#~ assertContains(ret[0][1], '1.2.6\src\Dither.h:40:')
	pass
	
test1()