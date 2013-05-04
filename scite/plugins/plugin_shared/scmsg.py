    
# can be a color, sent from isColorPicker.exe
def sd(*args):
    if len(args)>0:
        parts = args[0].split(',')
        if len(parts)==1:
            print parts
        else:
            print 'rgb('+','.join(parts[1:4])+')'
            print parts[4]
    
