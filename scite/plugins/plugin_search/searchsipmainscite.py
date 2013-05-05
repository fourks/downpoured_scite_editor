# SciTE Python Extension
# Ben Fisher, 2011

# this file can actually use the SciTE layer. others shouldn't.
# note: unicode characters in directories not supported or tested

from CScite import ScEditor, ScOutput, ScApp

import searchsipmain

# use F4 ('next message') to go there quickly

def SciteSearchSip(sMode):
    sPath = ScApp.GetFilePath().lower()
    sCurrentWord = ScApp.GetCurrentWord()
    sHomedir = ScApp.GetSciteDirectory()
    sLnzPath = ScApp.GetProperty('pyplugin.lnzpath')
    ret = searchsipmain.searchSip(sMode, sPath, sCurrentWord, sHomedir, sLnzPath)
    print '>'
    return ret

def SciteSearchSipToggle():
    sPath = ScApp.GetFilePath().lower()
    sHomedir = ScApp.GetSciteDirectory()
    ret = searchsipmain.searchSipToggle(sPath, sHomedir)
    print '>'
    return ret
    
    
def SciteSearchSipRebuild():
    sPath = ScApp.GetFilePath().lower()
    sHomedir = ScApp.GetSciteDirectory()
    ret = searchsipmain.searchSipRebuild(sPath, sHomedir)
    print '>'
    return ret




