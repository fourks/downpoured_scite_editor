    
# can be a color, sent from isColorPicker.exe
def sd(*args):
    if len(args)>0:
        parts = args[0].split(',')
        if len(parts)==1:
            print parts
        else:
            print 'rgb('+','.join(parts[1:4])+')'
            print parts[4]
    
def runGetStdout(listArgs, shell=False):
    import subprocess
    sp = subprocess.Popen(listArgs, shell=shell, stdout=subprocess.PIPE)
    text = sp.communicate()[0]
    return text.rstrip(), sp.returncode

def getChoiceShowDialog(sTitle, arOptions):
    from CScite import ScEditor, ScOutput, ScApp
    import os
    
    # we can't load Tkinter from here because we are running within the scite python extension.
    # so, start up the full python.exe in another process and read from stdout.
    
    pydir = ScApp.GetProperty('pyplugin.pypathw')
    assert 'pythonw.exe' in pydir
    dlgutil = os.path.join( ScApp.GetSciteDirectory(), 'plugins', 'plugin_shared', 'dlgutil.py')
    
    args = [pydir, dlgutil, sTitle]
    for opt in arOptions: args.append(opt)
    sret, status = runGetStdout(args)
    if status==0 and '|' in sret:
        a,res,b = sret.split('|')
        return int(res)
    else:
        return None
    
def getInputShowDialog(sPrompt, sTitle):
    from CScite import ScEditor, ScOutput, ScApp
    import os
    
    pydir = ScApp.GetProperty('pyplugin.pypathw')
    assert 'pythonw.exe' in pydir
    dlgutil = os.path.join( ScApp.GetSciteDirectory(), 'plugins', 'plugin_shared', 'dlgutil.py')
    
    args = [pydir, dlgutil, 'inputdialog', sPrompt, sTitle]
    sret, status = runGetStdout(args)
    if status==0 and '|' in sret:
        a,res,b = sret.split('|')
        return int(res)
    else:
        return None
    
    