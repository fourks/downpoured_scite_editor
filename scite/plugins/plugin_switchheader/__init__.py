# SciTE Python Extension
# Ben Fisher, 2011
# switch between a .cpp and a .h

from CScite import ScEditor, ScOutput, ScApp

def switchheader():
    import os
    cppendings = ('.cpp','.c','.cxx')
    headerendings = ('.hpp','.h','.hxx')
    curFile = ScApp.GetFilePath().lower()
    if not curFile or not len(curFile): return
        
    path, fname = os.path.split(curFile.lower())
    fname1, fname2 = os.path.splitext(fname)
    
    def search(endingsfrom, endingsto):
        for end in endingsfrom:
            if fname2 == end:
                for candidate in [os.path.join(path, fname1+newend) for newend in endingsto]:
                    if os.path.exists(candidate):
                        ScApp.OpenFile(candidate)
                        return True
                for candidate in [os.path.join(path, '..', fname1+newend) for newend in endingsto]:
                    if os.path.exists(candidate):
                        ScApp.OpenFile(candidate)
                        return True
                return False
        return False
    
    ret = search(cppendings, headerendings) or search(headerendings, cppendings)
    if not ret: print 'could not find corresponding header or source'

