
SciTE Code Editor + Python
Ben Fisher, 2011
github.com/downpoured/downpoured_scite_editor

A lightweight code editor with easily-scriptable Python plugins.


Usage
-------------------
(If SciTE.exe is not present, unzip the contents of scite.exe.win32.zip into the scite directory).
Run SciTE.exe, and start using it to write code!

SciTE has many helpful keyboard shortcuts. Some of my favorites are:
	Ctrl Q to comment-out a line
	Ctrl D to duplicate a line
	Ctrl 1 to copy the path of the current file


Overview
-------------------
This is a fork of the excellent SciTE code editor. Mainline SciTE can be customized
with Lua scripts, but Lua is not a 'batteries included' language, and it can be less-than-
straightforward to write these customizations.

By using Python, on the other hand, one gains access to Python's standard library and 
can use much existing Python code, and I aim to simplify the process of adding plugins.

To set up the indexed code search plugin, build downpoured_scite_editor/tools/simple_source_index,
copy downpoured_scite_editor/tools/simple_source_index/release/simple_source_index.exe to 
downpoured_scite_editor/scite/plugins/plugin_search/db/ssip.exe
unzip downpoured_scite_editor/tools/simple_source_index/sqlite3.dll.zip (or download from sqlite.org) to
downpoured_scite_editor/scite/plugins/plugin_search/db/sqlite3.dll
edit downpoured_scite_editor/scite/plugins/plugin_search/projects.cfg, following the example.
You can now press F12 to run an indexed code search on the selected term.

Contact scitewiki@gmail.com with any questions.

Adding a simple plugin
-------------------
Simple plugins are a one-time action triggered by a keyboard shortcut or from the Tools menu.
Open generateproperties.py in an editor.
Ensure that g_pythonpath points to your machine's Python installation.
Add the end of generateproperties.py, add a registration line for your plugin.

If your plugin does not need to interact with the editor, use spelling as an example.
	This style of plugin is run in a separate python.exe process;
	any results from stdout are printed in the side pane.

If your plugin does need to interact with the editor, use switch_header as an example.
	This style of plugin can access the ScEditor and ScApp objects.
	You will need to edit /scite/plugins/__init__.py to import your code.
	For a full reference of what a plugin can call, see scite/plugins/scite_extend_doc.txt.

Then, run generateproperties.py and restart SciTE.


Adding an advanced plugin
-----------------
Advanced plugins can run code without being explicitly triggered. For example, the record_position
plugin runs after every key press to record the current line and file, so that you can use Ctrl+Minus
to navigate where you have been changing the file.

To add an advanced plugin, edit
scite_extend.py
For example, to run code whenever switching tabs, add a line to OnSwitchFile to call into your plugin.
Refer to OnChar to see how record_position is implemented.


