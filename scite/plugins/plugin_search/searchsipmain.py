# SciTE Python Extension
# Ben Fisher, 2011

import os, sys
import searchsipimpl
import searchutil
from searchutil import SipException
import scmsg
from CScite import ScEditor, ScOutput, ScApp

# ssip -s word                Search for a word        
# ssip -start                Re-build index from scratch        
# ssip -noindex word                Search for a word without using index        
# ssip -noindexnowhole word                Search for a word without using index        

def searchIndexedMain(sModeIn):
    if sModeIn=='impl': sMode = searchsipimpl.Searchmodes.SEARCH_IMPLS
    elif sModeIn=='defn': sMode = searchsipimpl.Searchmodes.SEARCH_DEFNS
    elif sModeIn=='all': sMode = searchsipimpl.Searchmodes.ALL_EXCEPT_COMMENTS
    else: assert False
    sPath = ScApp.GetFilePath()
    inidir = os.path.join(ScApp.GetSciteDirectory(), 'plugins', 'plugin_search')
    ininame = os.path.join(inidir, 'projects.cfg')
    ret = searchutil.getprojsection(ininame, sPath)
    if not ret:
        if not os.path.exists(ininame): f=open(ininame,'w'); f.write(' '); f.close()
        n = scmsg.getChoiceShowDialog('This file is not part of a project. Add it to a new project?', ['Yes', 'No'] )
        if n!=0: return
        pos1 = 0
        if n==0:
            folder, leaf = os.path.split(sPath)
            f=open(ininame,'a');
            pos1 = f.tell()
            print 'pos = ',pos1
            f.write('\n\n[project_new_%d]\nsrcdir1=%s\n\n'%(sum(map(ord, sPath)), folder))
            f.close()
        ScApp.OpenFile(ininame)
        if pos1: ScEditor.Select(pos1, pos1+20)
        return
    
    sProjname, sTxtCfg = ret
    sQuery = getQuery()
    searchutil.checkSupportedString(sQuery)
    sipname = os.path.join(inidir, 'db', 'ssip.exe')
    fcfg=open(os.path.join(inidir, 'db', 'ssip.cfg'), 'w')
    fcfg.write(sTxtCfg)
    assert 'dbpath=' not in sTxtCfg
    assert len(sProjname)>0 and '\n' not in sProjname
    fcfg.write('\ndbpath=%s\n'%os.path.join(inidir, 'db', sProjname+'.db'))
    fcfg.close()
    
    os.chdir(os.path.join(inidir, 'db')) # ssip.exe will see that config file
    rawtext = searchutil.runReturnStdout(sipname, ['-s', sQuery])
    results = searchsipimpl.filter(sMode, sQuery, rawtext)
    # todo: if there is only one result, consider opening it automatically
    searchsipimpl.displayResults(results)
    
def searchUnindexedMain(sRelativeDir):
    print 'searching source-code filetypes in %s.'%sRelativeDir
    sQuery = getQuery()
    sPath = ScApp.GetFilePath()
    searchutil.checkSupportedString(sQuery)
    inidir = os.path.join(ScApp.GetSciteDirectory(), 'plugins', 'plugin_search')
    sTxtCfg = createCfgTemporary(sPath, sRelativeDir)
    fcfg=open(os.path.join(inidir, 'db', 'ssip.cfg'), 'w')
    sipname = os.path.join(inidir, 'db', 'ssip.exe')
    fcfg.write(sTxtCfg)
    fcfg.close()
    assert 'dbpath=' not in sTxtCfg
    
    os.chdir(os.path.join(inidir, 'db')) # ssip.exe will see that config file
    rawtext = searchutil.runReturnStdout(sipname, ['-noindex', sQuery])
    print rawtext

def createCfgTemporary(sPath, sRelativeDir):
    folder, leaf = os.path.split(sPath)
    if sRelativeDir:
        folder = os.path.join(folder, sRelativeDir)
        folder = os.path.normpath(folder) #turn a/b/c/.. into a/b
    s = '\n[main]\nsrcdir1=%s\n'%folder
    return s

def getQuery():
    sCurrentWord = ScApp.GetCurrentWord().strip()
    if not sCurrentWord:
        sCurrentWord = getInputShowDialog('Enter a search term:', 'Indexed Search')
        if not sCurrentWord:
            raise SipException('No search term.')
    return sCurrentWord
