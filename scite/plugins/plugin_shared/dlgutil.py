

def ShowChoiceDialog(sPrompt, arOptions):
    import Tkinter
    assert len(arOptions) > 0
    retval = [None]
    def setresult(v):
        retval[0] = v
    
    #http://effbot.org/tkinterbook/tkinter-dialog-windows.htm
    class ChoiceDialog(object):
        def __init__(self, parent):
            top = self.top = Tkinter.Toplevel(parent)
            Tkinter.Label(top, text=sPrompt).pack()
            top.title('Choice')

            box = Tkinter.Frame(top)
            for i in range(len(arOptions)):
                opts = dict()
                opts['text'] = arOptions[i]
                opts['width'] = 10
                opts['underline'] = 0
                opts['command'] = lambda capt=i: self.onbtn(None, capt)
                top.bind( arOptions[i][0].lower(), lambda _,capt=i: self.onbtn(_, capt))
                if i==0: opts['default'] = Tkinter.ACTIVE
                w = Tkinter.Button(box, **opts)
                w.pack(side=Tkinter.LEFT, padx=5, pady=5)
            
            top.bind("<Return>", self.onbtn)
            top.bind("<Escape>", self.cancel)

            box.pack(pady=5)
            parent.update()

        def cancel(self, unused):
            self.top.destroy()
        def onbtn(self, unused, nWhich=0):
            setresult(nWhich)
            self.top.destroy()

    root = Tkinter.Tk()
    root.withdraw()
    d = ChoiceDialog(root)
    root.wait_window(d.top)
    return retval[0]

if __name__=='__main__':
    r = ShowChoiceDialog('Show which tool?', ['ascii table', 'color picker'] )
    print r
    