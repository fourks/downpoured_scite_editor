
SciTE Python Extension
Version 0.5
Ben Fisher, 2011
scitewiki@gmail.com

Overview
-------------------
You can now write plugins and scripts in Python to customize SciTE. 
You have access to the powerful standard library of Python.

Usage
-------------------
If you open the global options file, you will see a command for 'Python run script'.
When you run this command (from the Tools menu or by pressing Ctrl+Alt+k),
a sample Python script will run.

Modify this sample script by editing 'callFromCmd' in scite_extend.py.
You can call one of the many functions documented in scite_extend_doc.txt.
scite_extend.py also shows the callbacks that will be run. You can also put code here.

Release notes
-------------------
gcc makefile not updated. gtk directory not updated

Known issues:
	ScApp.Fullscreen()
	ScEditor.GetStyleAt()
	ScEditor.AssignCmdKey()
	ScApp.Tools() #not sure of effect
	ScApp.ToolWin() #not sure of effect
	
	The following are untested
	void	ScEditor.SetWordChars(, string characters)
	void	ScEditor.SetAutoCFillUps(, string characterSet)
	void	ScEditor.SetMarginLeft(, int pixelWidth)
	void	ScEditor.SetMarginRight(, int pixelWidth)
	int	ScEditor.PointXFromPosition(, position pos)
	int	ScEditor.PointYFromPosition(, position pos)
	void	ScEditor.SetWhitespaceChars(, string characters)

Certain methods can read past end of file. This is a limitation of Scintilla.

If the app exists while a MessageBox is open, an error will be shown.

