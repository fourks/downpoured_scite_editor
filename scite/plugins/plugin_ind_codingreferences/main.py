
def printascii():
    overrides = { 0:"(Null)", 9:"(Tab)",10:"(\\n Newline)", 13:"(\\r Return)", 32:"(Space)"}
    for i in range(128):
        c = overrides.get(i, chr(i))
        print str(i).zfill(3) + ' ' + c

def showcolorpicker(shomedir):
    path=os.path.join(shomedir, 'plugins', 'plugin_ind_codingreferences', 'isColorPicker.exe')
    import subprocess
    subprocess.call([path])

def main(shomedir):
    import dlgutil
    n = dlgutil.ShowChoiceDialog('Show which tool?', ['ascii table', 'color picker'] )
    if n==0:
        printascii()
    elif n==1:
        showcolorpicker(shomedir)
    
    
if __name__=='__main__':
    import os, sys
    shomedir = sys.argv[1]
    # add to import path, to import dlgutil
    sys.path.append(os.path.join(shomedir, 'plugins', 'plugin_shared'))
    main(shomedir)
    
    
