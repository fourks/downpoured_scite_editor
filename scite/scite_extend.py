# SciTE Python Extension
# Ben Fisher, 2011

from CScite import ScEditor, ScOutput, ScApp

echoEvents = False

def OnStart():
    import os, sys
    if not os.path.exists(os.path.join(ScApp.GetSciteDirectory(), 'properties', 'pyplugin_generated.properties')): 
        print 'SciTE: please 1) open generateproperties.py in an editor and specify the path to python'
        print '2) run generateproperties.py to enable keyboard shortcuts.'
    if echoEvents: print 'See OnStart'
    sys.path.append(os.path.join(ScApp.GetSciteDirectory(), 'plugins', 'plugin_shared'))

def OnOpen(sFilename):
    if echoEvents: print 'See OnOpen'

def OnClose(sFilename):
    if echoEvents: print 'See OnClose'

def OnMarginClick():
    if echoEvents: 
        ScEditor.Write('hi') # example of how to call a method on the ScEditor object
        print 'hi'
        print 'See OnMarginClick'

def OnSwitchFile(sFilename):
    if echoEvents: print 'See OnSwitchFile'
    
def OnBeforeSave(sFilename):
    if echoEvents: print 'See OnBeforeSave'
    
def OnSave(sFilename):
    if echoEvents: print 'See OnSave'
    
def OnSavePointReached():
    if echoEvents: print 'See OnSavePointReached'
    
def OnSavePointLeft():
    if echoEvents: print 'See OnSavePointLeft'

def OnChar(nChar):
    # returning False here has no effect
    import plugins
    plugins.plugin_recordposition.recordposition()
    plugins.plugin_modifytext.autoclosetags(nChar)
    if echoEvents: print 'See OnChar'

def OnDoubleClick():
    if echoEvents: print 'See OnDoubleClick'
    
def OnDwellStart(nPos, sWord):
    if echoEvents: print 'See OnDwellStart'

def OnDwellEnd():
    if echoEvents: print 'See OnDwellEnd'

def OnUserListSelection(nType, sSelection):
    if echoEvents: print 'See OnUserListSelection', nType, sSelection

# disabled out so that perf is not affected.
def OnKey_inactive_example(keycode, fShift, fCtrl, fAlt):
    if echoEvents: 
        import exceptions
        try:
            import scite_extend_tests
        except exceptions.ImportError, e:
            if str(e) == 'No module named scite_extend_tests':
                return None
            else:
                raise
        return scite_extend_tests.RunTestSet(keycode, fShift, fCtrl, fAlt)


