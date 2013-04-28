// SciTE Python Extension
// Ben Fisher, 2011

#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "Scite.h"
#include "Scintilla.h"
#include "Extender.h"
#include "SString.h"
#include "SciTEKeys.h"
#include "IFaceTable.h"

#include "PythonExtension.h"

#ifdef _MSC_VER
	#pragma warning(disable: 4100) // unreferenced formal parameter
	#pragma warning(disable: 4996) // unsafe calls (deprecated stdio)
#endif

#ifdef _WIN32
#include <windows.h>
#endif

static const char* c_szExtensionModName = "scite_extend"; //looks for the file scite_extend.py
static bool fPythonInitialized = false;
static inline bool FInitialized() { return fPythonInitialized; }
static ExtensionAPI *_host = NULL;

PythonExtension::PythonExtension() {}
PythonExtension::~PythonExtension() {}
void PythonExtension::InitializePython()
{
	if (!FInitialized())
	{
		Py_NoSiteFlag = 1; // tell python not to try to 'import site'
		Py_Initialize();
		SetupPythonNamespace();
		fPythonInitialized = true;
	}
}
PythonExtension &PythonExtension::Instance()
{
	static PythonExtension singleton;
	return singleton;
}
bool PythonExtension::Initialise(ExtensionAPI *host)
{
	_host = host;
	writeLog("log:PythonExtension::Initialise");
	
	char* szDelayLoad = _host->Property("ext.python.delayload");
	if (!(szDelayLoad && szDelayLoad[0]!='\0' && (szDelayLoad[0]!='0'||strlen(szDelayLoad)>1)))
	{
		InitializePython();
		_runCallback("OnStart", 0, NULL);
#if FALSE
		{
			// binary search requires items to be sorted, verify that they are sorted
			for (unsigned int i=0; i<PythonExtension::lengthfriendlyconstants-1; i++)
			{
				const char* name1 = PythonExtension::friendlyconstants[i].name;
				const char* name2 = PythonExtension::friendlyconstants[i+1].name;
				if (strcmp(name1, name2) != -1)
				{
					trace("\nWarning-unsorted-");
					trace(name1, name2);
				}
			}
		}
#endif
	}
	return true;
}
bool PythonExtension::OnExecute(const char *s)
{
	InitializePython();
	int nResult = PyRun_SimpleString(s);
	if (nResult == 0) { return true; }
	else { 
		PyErr_Print(); 
		return true; //used to be false, looked weird
		}
}
bool PythonExtension::Finalise()
{
	_host = NULL; /* by this point _host may be already invalid */
	return false;
}
bool PythonExtension::Clear()
{
	writeLog("log:PythonExtension::Clear");
	return false;
}
bool PythonExtension::Load(const char *fileName)
{
	FILE* f = fopen(fileName, "r");
	if (!f) { _host->Trace(">Python: could not open file.\n"); return false; }
	int nResult = PyRun_SimpleFileEx(f, fileName, 1); //Python will close file handle.
	if (nResult == 0) { return true; }
	else { PyErr_Print(); return false; }
}
bool PythonExtension::InitBuffer(int index)
{
	writeLog("log:PythonExtension::InitBuffer");
	return false;
}
bool PythonExtension::ActivateBuffer(int index)
{
	writeLog("log:PythonExtension::Activatebuffer");
	return false;
}
bool PythonExtension::RemoveBuffer(int index)
{
	writeLog("log:PythonExtension::removebuffer");
	return false;
}


void PythonExtension::writeText(const char *szText) { trace(szText, "\n"); }
bool PythonExtension::writeError(const char *szError) { trace(">Python Error:", szError); trace("\n"); return true; }
bool PythonExtension::writeError(const char *szError, const char *szError2)
{
	trace(">Python Error:", szError); trace(" ", szError2); trace("\n"); return true;
}
void PythonExtension::writeLog(const char *szText) { /* if (false) trace(szText, "\n"); */ } 


//////////////////////////////////////////// callbacks //////////////////////////////////////////////////

bool PythonExtension::OnOpen(const char *fileName)
{
	if (!FInitialized()) return false;
	return _runCallback("OnOpen", 1, fileName);
}
bool PythonExtension::OnClose(const char *fileName)
{
	if (!FInitialized()) return false;
	return _runCallback("OnClose", 1, fileName);
}
bool PythonExtension::OnSwitchFile(const char *fileName)
{
	if (!FInitialized()) return false;
	return _runCallback("OnSwitchFile", 1, fileName);
}
bool PythonExtension::OnBeforeSave(const char *fileName)
{
	if (!FInitialized()) return false;
	return _runCallback("OnBeforeSave", 1, fileName);
}
bool PythonExtension::OnSave(const char *fileName)
{
	if (!FInitialized()) return false;
	return _runCallback("OnSave", 1, fileName);
}
bool PythonExtension::OnSavePointReached()
{
	if (!FInitialized()) return false;
	return _runCallback("OnSavePointReached", 0, NULL);
}
bool PythonExtension::OnSavePointLeft()
{
	if (!FInitialized()) return false;
	return _runCallback("OnSavePointLeft", 0, NULL);
}
bool PythonExtension::OnChar(char ch)
{
	if (!FInitialized()) return false;
	CPyObjStrong pArgs = Py_BuildValue("(i)", (int) ch);
	return _runCallbackArgs("OnChar", pArgs);
}
bool PythonExtension::OnKey(int keycode, int modifiers)
{
	if (!FInitialized()) return false;
	int fShift = (SCMOD_SHIFT & modifiers) != 0 ? 1 : 0;
	int fCtrl = (SCMOD_CTRL & modifiers) != 0 ? 1 : 0;
	int fAlt = (SCMOD_ALT & modifiers) != 0 ? 1 : 0;
	CPyObjStrong pArgs = Py_BuildValue("(i,i,i,i)", (int) keycode, fShift, fCtrl, fAlt);
	return _runCallbackArgs("OnKey", pArgs);
}
bool PythonExtension::OnDoubleClick()
{
	if (!FInitialized()) return false;
	return _runCallback("OnDoubleClick", 0, NULL);
}
bool PythonExtension::OnMarginClick()
{
	if (!FInitialized()) return false;
	return _runCallback("OnMarginClick", 0, NULL);
}
bool PythonExtension::OnDwellStart(int pos, const char *word)
{
	if (!FInitialized()) return false;
	if (pos == 0 && word[0] == 0)
	{
		return _runCallback("OnDwellEnd", 0, NULL);
	}
	else
	{
		CPyObjStrong pArgs = Py_BuildValue("(i,s)", pos, word);
		return _runCallbackArgs("OnDwellStart", pArgs);
	}
}
bool PythonExtension::OnUserListSelection(int type, const char *selection)
{
	if (!FInitialized()) return false;
	CPyObjStrong pArgs = Py_BuildValue("(i,s)", type, selection);
	return _runCallbackArgs("OnUserListSelection", pArgs);
}
bool PythonExtension::_runCallback(const char* szNameOfFunction, int nArgs, const char* szArg1)
{
	if (nArgs == 0)
	{
		return _runCallbackArgs(szNameOfFunction, NULL);
	}
	else if (nArgs == 1)
	{
		CPyObjStrong pArgs = Py_BuildValue("(s)", szArg1);
		return _runCallbackArgs(szNameOfFunction, pArgs);
	}
	else
	{
		return writeError("Unexpected: calling _runCallback, only 0/1 args supported."); 
	}
}
bool PythonExtension::_runCallbackArgs(const char* szNameOfFunction, PyObject* pArgsBorrowed)
{
	CPyObjStrong pName = PyString_FromString(c_szExtensionModName);
	if (!pName) { return writeError("Unexpected error: could not form string."); }
	CPyObjStrong pModule = PyImport_Import(pName);
	if (!pModule) {
		writeError("Error importing module.");
		PyErr_Print();
		return false;
	}
	CPyObjWeak pDict = PyModule_GetDict(pModule);
	if (!pDict) { return writeError("Unexpected: could not get module dict."); }
	CPyObjWeak pFn = PyDict_GetItemString(pDict, szNameOfFunction);
	if (!pFn) { /* module does not define that callback. */ return false;	}
	if (!PyCallable_Check(pFn)) { return writeError("callback not a function", szNameOfFunction); }

	CPyObjStrong pResult = PyObject_CallObject(pFn, pArgsBorrowed);
	if (!pResult) {
		writeError("Error in callback ", szNameOfFunction);
		PyErr_Print();
		return false;
	}
	/* bubble event up by default, unless they explicitly return false. */
	if (PyBool_Check(((PyObject*)pResult)) && pResult == Py_False)
		return true; // do not bubble up event
	else
		return false; // bubble up event
}

//////////////////////////////////////////// implementation //////////////////////////////////////////////////

PyObject* pyfun_LogStdout(PyObject* self, PyObject* pArgs)
{
	char* szLogStr = NULL; /* we don't own this. */
	if (!PyArg_ParseTuple(pArgs, "s", &szLogStr)) return NULL;
	_host->Trace(szLogStr);
	Py_INCREF(Py_None);
	return Py_None;
}
PyObject* pyfun_MessageBox(PyObject* self, PyObject* pArgs)
{
	char* szLogStr = NULL; /* we don't own this. */
	if (!PyArg_ParseTuple(pArgs, "s", &szLogStr)) return NULL;
#ifdef _WIN32
	MessageBoxA(NULL, szLogStr, "SciTEPython", 0);
#endif
	Py_INCREF(Py_None);
	return Py_None;
}
PyObject* pyfun_SciteOpenFile(PyObject* self, PyObject* pArgs)
{
	char* szFilename = NULL; /* we don't own this. */
	if (!PyArg_ParseTuple(pArgs, "s", &szFilename)) return NULL;
	if (szFilename) {
		SString cmd = "open:";
		cmd += szFilename;
		cmd.substitute("\\", "\\\\");
		_host->Perform(cmd.c_str());
	}
	Py_INCREF(Py_None);
	return Py_None;
}
PyObject* pyfun_GetProperty(PyObject* self, PyObject* pArgs)
{
	char* szPropName = NULL; /* we don't own this. */
	if (!PyArg_ParseTuple(pArgs, "s", &szPropName)) return NULL;
	char *value = _host->Property(szPropName);
	if (value)
	{
		PyObject* objRet = PyString_FromString(value);
		/* leave it with a refcount of 1, don't decref */
		delete[] value;
		return objRet;
	}
	else
	{
		Py_INCREF(Py_None);
		return Py_None;	
	}
}
PyObject* pyfun_SetProperty(PyObject* self, PyObject* pArgs) 
{
	char* szPropName = NULL; char* szPropValue = NULL; /* we don't own this. */
	if (!PyArg_ParseTuple(pArgs, "ss", &szPropName, &szPropValue)) return NULL;
	_host->SetProperty(szPropName, szPropValue); // it looks like SetProperty allocates, don't need key and val on the heap.
	Py_INCREF(Py_None);
	return Py_None;
}
PyObject* pyfun_UnsetProperty(PyObject* self, PyObject* pArgs)
{
	char* szPropName = NULL; /* we don't own this. */
	if (!PyArg_ParseTuple(pArgs, "s", &szPropName)) return NULL;
	_host->UnsetProperty(szPropName);
	Py_INCREF(Py_None);
	return Py_None;
}




PyObject* pyfun_pane_Append(PyObject* self, PyObject* pArgs)
{
	char* szText = NULL; /* we don't own this. */
	int nPane = -1; ExtensionAPI::Pane pane;
	if (!PyArg_ParseTuple(pArgs, "is", &nPane, &szText)) return NULL;
	if (!getPaneFromInt(nPane, &pane)) return NULL;
	_host->Insert(pane, _host->Send(pane, SCI_GETLENGTH, 0, 0), szText);
	Py_INCREF(Py_None);
	return Py_None;
}
PyObject* pyfun_pane_Insert(PyObject* self, PyObject* pArgs)
{
	char* szText = NULL; /* we don't own this. */
	int nPane = -1, nPos=-1; ExtensionAPI::Pane pane;
	if (!PyArg_ParseTuple(pArgs, "iis", &nPane, &nPos, &szText)) return NULL;
	if (nPos<0) return NULL;
	if (!getPaneFromInt(nPane, &pane)) return NULL;
	_host->Insert(pane,nPos, szText);
	Py_INCREF(Py_None);
	return Py_None;
}
PyObject* pyfun_pane_Remove(PyObject* self, PyObject* pArgs)
{
	int nPane = -1, nPosStart=-1, nPosEnd=-1; ExtensionAPI::Pane pane;
	if (!PyArg_ParseTuple(pArgs, "iii", &nPane, &nPosStart, &nPosEnd)) return NULL;
	if (nPosStart<0 || nPosEnd<0) return NULL;
	if (!getPaneFromInt(nPane, &pane)) return NULL;
	_host->Remove(pane,nPosStart,nPosEnd);
	Py_INCREF(Py_None);
	return Py_None;
}
PyObject* pyfun_pane_TextRange(PyObject* self, PyObject* pArgs)
{
	int nPane = -1, nPosStart=-1, nPosEnd=-1; ExtensionAPI::Pane pane;
	if (!PyArg_ParseTuple(pArgs, "iii", &nPane, &nPosStart, &nPosEnd)) return NULL;
	if (nPosStart<0 || nPosEnd<0) return NULL;
	if (!getPaneFromInt(nPane, &pane)) return NULL;
	char *value = _host->Range(pane, nPosStart, nPosEnd);
	if (value)
	{
		CPyObjWeak objRet = PyString_FromString(value); // weakref because we are giving ownership.
		delete[] value;
		return objRet;
	}
	else
	{
		Py_INCREF(Py_None);
		return Py_None;	
	}
}
PyObject* pyfun_pane_FindText(PyObject* self, PyObject* pArgs) //returns a tuple
{
	char* szText = NULL; /* we don't own this. */
	int nPane = -1, nFlags=0, nPosStart=0, nPosEnd=-1; ExtensionAPI::Pane pane;
	if (!PyArg_ParseTuple(pArgs, "is|iii", &nPane, &szText, &nFlags, &nPosStart, &nPosEnd)) return NULL;
	if (!getPaneFromInt(nPane, &pane)) return NULL;
	if (nPosEnd==-1) nPosEnd= _host->Send(pane, SCI_GETLENGTH, 0, 0);
	if (nPosStart<0 || nPosEnd<0) return NULL;
	
	Sci_TextToFind ft = {{0, 0}, 0, {0, 0}};
	ft.lpstrText =szText; 
	ft.chrg.cpMin = nPosStart;
	ft.chrg.cpMax = nPosEnd;
	int result = _host->Send(pane, SCI_FINDTEXT, static_cast<uptr_t>(nFlags), reinterpret_cast<sptr_t>(&ft));
	
	if (result >= 0)
	{
		// build a tuple. // weakref because we are giving ownership.
		CPyObjWeak objRet = Py_BuildValue("(i,i)", ft.chrgText.cpMin, ft.chrgText.cpMax);
		return objRet;
	}
	else
	{
		Py_INCREF(Py_None);
		return Py_None;
	}
}



PyObject* pyfun_pane_SendScintillaFn(PyObject* self, PyObject* pArgs)
{
	char* szCmd = NULL; /* we don't own this. */
	int nPane=-1; ExtensionAPI::Pane pane; 
	PyObject* pSciArgs; //borrowed reference, so ok.
	if (!PyArg_ParseTuple(pArgs, "isO", &nPane, &szCmd, &pSciArgs)) return NULL;
	if (!getPaneFromInt(nPane, &pane)) return NULL;
	if (!PyTuple_Check(pSciArgs)) { PyErr_SetString(PyExc_RuntimeError,"Third arg must be a tuple."); return NULL;}
	
	int nFnIndex = IFaceTable::FindFunction(szCmd);
	if (nFnIndex == -1) { PyErr_SetString(PyExc_RuntimeError,"Could not find fn."); return NULL; }
	
	intptr_t wParam = 0; //args to be passed to Scite
	intptr_t lParam = 0; //args to be passed to Scite
	IFaceFunction func = IFaceTable::functions[nFnIndex];
	bool isStringResult = func.returnType == iface_int && func.paramType[1] == iface_stringresult;
	size_t nArgCount = PyTuple_GET_SIZE((PyObject*) pSciArgs);
	size_t nArgsExpected = isStringResult ? ((func.paramType[0] != iface_void) ? 1 : 0) :
		((func.paramType[1] != iface_void) ? 2 : ((func.paramType[0] != iface_void) ? 1 : 0));
	if (strcmp(szCmd, "GetCurLine")==0)
	{	nArgsExpected = 0; func.paramType[0] = iface_void; func.paramType[1] = iface_void; }
	
	if (nArgCount != nArgsExpected) { PyErr_SetString(PyExc_RuntimeError,"Wrong # of args"); return false; }
	
	if (func.paramType[0] != iface_void)
	{
		bool fResult = pullPythonArgument( func.paramType[0], PyTuple_GetItem(pSciArgs, 0), &wParam);
		if (!fResult)  {	return NULL; }
	}
	if (func.paramType[1] != iface_void && !isStringResult)
	{
		bool fResult = pullPythonArgument( func.paramType[1], PyTuple_GetItem(pSciArgs, 1), &lParam);
		if (!fResult)  {	return NULL; }
	}
	else if (isStringResult) { // allocate space for the result
		size_t spaceNeeded = _host->Send(pane, func.value, wParam, NULL);
		if (strcmp(szCmd, "GetCurLine")==0) // the first param of getCurLine is useless
			wParam = spaceNeeded + 1; //not sure if correct
		//trace("", "allocating", spaceNeeded);
		lParam = (intptr_t) new char[spaceNeeded+1];
		for (unsigned i=0; i<spaceNeeded+1; i++) ((char*)lParam)[i] = 0;
	}
	
	intptr_t result = _host->Send(pane, func.value, wParam, lParam);
	PyObject* pyObjReturn = NULL;
	if (!isStringResult)
	{
		bool fRet = pushPythonArgument(func.returnType, result, &pyObjReturn); // if returns void, it simply returns NONE, so we're good
		if (!fRet)  { return NULL; }
	}
	else
	{
		if (!lParam)  { /* Unexpected: returning null instead of string */ Py_INCREF(Py_None); return Py_None; }
		//because there might not be a final null, pyObjReturn = PyString_FromString((char *) lParam); doesn't work
		//trace("got", "", (size_t) result);
		if (result == 0)
			pyObjReturn = PyString_FromString("");
		else
			pyObjReturn = PyString_FromStringAndSize((char *) lParam, (size_t) result-1);
		delete[] (char*) lParam;
	}
	Py_INCREF(pyObjReturn); //important to incref
	return pyObjReturn;
}
PyObject* pyfun_pane_SendScintillaGet(PyObject* self, PyObject* pArgs)
{
	char* szProp = NULL; /* we don't own this. */
	int nPane=-1; ExtensionAPI::Pane pane; PyObject* pyObjParam=NULL;
	if (!PyArg_ParseTuple(pArgs, "is|O", &nPane, &szProp, &pyObjParam)) return NULL;
	if (!getPaneFromInt(nPane, &pane)) return NULL;
	
	int nFnIndex = IFaceTable::FindProperty(szProp);
	if (nFnIndex == -1) { PyErr_SetString(PyExc_RuntimeError,"Could not find prop."); return NULL; }
	IFaceProperty prop =  IFaceTable::properties[nFnIndex];
	if (prop.getter == 0) { PyErr_SetString(PyExc_RuntimeError,"prop can't be get."); return NULL; }
	intptr_t wParam = 0; //args to be passed to Scite
	intptr_t lParam = 0; //args to be passed to Scite
	
	if (strcmp(szProp, "Property")==0 || strcmp(szProp, "PropertyInt")==0) { PyErr_SetString(PyExc_RuntimeError,"Not supported."); return NULL; }
	
	if (prop.paramType != iface_void)
	{
		if (pyObjParam==NULL || pyObjParam == Py_None) { PyErr_SetString(PyExc_RuntimeError,"prop needs param."); return NULL; }
		bool fResult = pullPythonArgument( prop.paramType, pyObjParam, &wParam);
		if (!fResult)  { return NULL; }
	}
	else if (!(pyObjParam==NULL || pyObjParam == Py_None)) {PyErr_SetString(PyExc_RuntimeError,"property does not take params."); return NULL; }
	intptr_t result = _host->Send(pane, prop.getter, wParam, lParam);
	
	PyObject* pyObjReturn = NULL;
	bool fRet = pushPythonArgument(prop.valueType, result, &pyObjReturn); // if returns void, it simply returns NONE, so we're good
	if (!fRet)  { return NULL; }
	Py_INCREF(pyObjReturn); //important to incref
	return pyObjReturn;
}
PyObject* pyfun_pane_SendScintillaSet(PyObject* self, PyObject* pArgs)
{
	char* szProp = NULL; /* we don't own this. */
	int nPane=-1; ExtensionAPI::Pane pane; PyObject* pyObjArg1=NULL; PyObject* pyObjArg2=NULL;
	if (!PyArg_ParseTuple(pArgs, "isO|O", &nPane, &szProp, &pyObjArg1, &pyObjArg2)) return NULL;
	if (!getPaneFromInt(nPane, &pane)) return NULL;
		
	int nFnIndex = IFaceTable::FindProperty(szProp);
	if (nFnIndex == -1) { PyErr_SetString(PyExc_RuntimeError,"Could not find prop."); return NULL; }
	IFaceProperty prop =  IFaceTable::properties[nFnIndex];
	if (prop.setter == 0) { PyErr_SetString(PyExc_RuntimeError,"prop can't be set."); return NULL; }
	intptr_t wParam = 0; //args to be passed to Scite
	intptr_t lParam = 0; //args to be passed to Scite
	
	if (prop.paramType == iface_void)
	{
		if (!(pyObjArg2==NULL || pyObjArg2 == Py_None)) {PyErr_SetString(PyExc_RuntimeError,"property does not take params."); return NULL; }
		bool fResult = pullPythonArgument( prop.valueType, pyObjArg1, &wParam);
		if (!fResult)  { return NULL; }
	}
	else
	{
		// a bit different than expected, but in the docs it says "set void StyleSetBold=2053(int style, bool bold)
		if (pyObjArg2==NULL || pyObjArg2 == Py_None) { PyErr_SetString(PyExc_RuntimeError,"prop needs param."); return NULL; }
		bool fResult = pullPythonArgument( prop.paramType, pyObjArg1, &wParam);
		if (!fResult)  { return NULL; }
		fResult = pullPythonArgument( prop.valueType, pyObjArg2, &lParam);
		if (!fResult)  { return NULL; }
	}
	
	intptr_t result = _host->Send(pane, prop.setter, wParam, lParam);
	result;
	Py_INCREF(Py_None);
	return Py_None;
}
PyObject* pyfun_app_GetConstant(PyObject* self, PyObject* pArgs)
{
	char* szProp = NULL; /* we don't own this. */
	if (!PyArg_ParseTuple(pArgs, "s",  &szProp)) return NULL;
	
	int nFnIndex = IFaceTable::FindConstant(szProp);
	if (nFnIndex == -1) { PyErr_SetString(PyExc_RuntimeError,"Could not find constant."); return NULL; }
	IFaceConstant faceConstant =  IFaceTable::constants[nFnIndex];
	PyObject* pyValueOut = PyInt_FromLong(faceConstant.value);
	Py_INCREF(pyValueOut);
	return pyValueOut;
}
PyObject* pyfun_app_SciteCommand(PyObject* self, PyObject* pArgs)
{
	char* szProp = NULL; /* we don't own this. */
	if (!PyArg_ParseTuple(pArgs, "s",  &szProp)) return NULL;
	
	int nFnIndex = FindFriendlyNamedIDMConstant(szProp);
	if (nFnIndex == -1) { PyErr_SetString(PyExc_RuntimeError,"Could not find command."); return NULL; }
	IFaceConstant faceConstant =  PythonExtension::friendlyconstants[nFnIndex];
	_host->DoMenuCommand(faceConstant.value);
	Py_INCREF(Py_None);
	return Py_None;
}
PyObject* pyfun_app_UpdateStatusBar(PyObject* self, PyObject* pArgs)
{
	PyObject * pyObjBoolUpdate = NULL;
	if (!PyArg_ParseTuple(pArgs, "|O",  &pyObjBoolUpdate)) return NULL;
	bool bUpdateSlowData = false;
	if (pyObjBoolUpdate == Py_True) bUpdateSlowData = true;
	_host->UpdateStatusBar(bUpdateSlowData);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyMethodDef methods_LogStdout[] = {
	{"LogStdout", pyfun_LogStdout, METH_VARARGS, "Logs stdout"},
	{"app_Trace", pyfun_LogStdout, METH_VARARGS, "(for compat with scite-lua scripts)"},
	{"app_MsgBox", pyfun_MessageBox, METH_VARARGS, ""},
	{"app_OpenFile", pyfun_SciteOpenFile, METH_VARARGS, ""},
	{"app_GetProperty", pyfun_GetProperty, METH_VARARGS, "Get SciTE Property"},
	{"app_SetProperty", pyfun_SetProperty, METH_VARARGS, "Set SciTE Property"},
	{"app_UnsetProperty", pyfun_UnsetProperty, METH_VARARGS, "Unset SciTE Property"},
	{"app_UpdateStatusBar", pyfun_app_UpdateStatusBar, METH_VARARGS, ""},
	{"app_SciteCommand", pyfun_app_SciteCommand, METH_VARARGS, ""},
	{"app_GetConstant", pyfun_app_GetConstant, METH_VARARGS, ""},
	
	{"pane_Append", pyfun_pane_Append, METH_VARARGS, ""},
	{"pane_Insert", pyfun_pane_Insert, METH_VARARGS, ""},
	{"pane_Remove", pyfun_pane_Remove, METH_VARARGS, ""},
	{"pane_Textrange", pyfun_pane_TextRange, METH_VARARGS, ""},
	{"pane_FindText", pyfun_pane_FindText, METH_VARARGS, ""},
	{"pane_ScintillaFn", pyfun_pane_SendScintillaFn, METH_VARARGS, ""},
	{"pane_ScintillaGet", pyfun_pane_SendScintillaGet, METH_VARARGS, ""},
	{"pane_ScintillaSet", pyfun_pane_SendScintillaSet, METH_VARARGS, ""},
	// the match object, if it's needed at all, can be written in Python.
	
	{NULL, NULL, 0, NULL}
};

void PythonExtension::SetupPythonNamespace()
{
	CPyObjWeak pInitMod = Py_InitModule("CScite", methods_LogStdout);
	
	// WARNING: PyRun_SimpleString does not handle errors well, check return value and not ErrorsOccurred(), it might leave python in a weird state.
	int ret = PyRun_SimpleString(
	"import CScite\n"
	"import sys\n"
	"class StdoutCatcher:\n"
	"    def write(self, str):\n"
	"        CScite.LogStdout(str)\n"
	"sys.stdout = StdoutCatcher()\n"
	"sys.stderr = StdoutCatcher()\n"
	);
	if (ret!=0)
	{
		writeError("Unexpected: error capturing stdout from Python. make sure python26.zip is present?");
		PyErr_Print(); //of course, if printing isn't set up, will not help, but at least will clear python's error bit
		return;
	}
	
	// now run setup script to add wrapper classes.
	// use Python's import. don't have to worry about current directory problems
	// using PyRun_AnyFile(fp, "pythonsetup.py"); ran into those issues
	// pythonsetup.py modifies the CScite module object, so others importing CScite will see the changes.
	CPyObjStrong pName = PyString_FromString("pythonsetup");
	if (!pName) { writeError("Unexpected error: could not form string pythonsetup."); }
	CPyObjStrong pModule = PyImport_Import(pName);
	if (!pModule) 
	{
		writeError("Error importing pythonsetup module.");
		PyErr_Print();
	}
}

//////////////////////////////////////////// helper fns //////////////////////////////////////////////////

bool pullPythonArgument(IFaceType type, CPyObjWeak pyObjNext, intptr_t* param)
{
	if (!pyObjNext) {  PyErr_SetString(PyExc_RuntimeError,"Unexpected: could not get next item."); return false; }

	switch(type) {
		case iface_void:
			break;
		case iface_int:
		case iface_length:
		case iface_position:
		case iface_colour:
		case iface_keymod:  // keymods: no urgent need to make this in c++, because AssignCmdKey / ClearCmdKey are only ones using this... see py's makeKeyMod
			if (!PyInt_Check((PyObject*) pyObjNext)) { PyErr_SetString(PyExc_RuntimeError,"Int expected."); return false; }
			*param = (intptr_t) PyInt_AsLong(pyObjNext);
			break;
		case iface_bool:
			if (!PyBool_Check((PyObject*) pyObjNext)) { PyErr_SetString(PyExc_RuntimeError,"Bool expected."); return false; }
			*param = (pyObjNext == Py_True) ? 1 : 0;
			break;
		case iface_string:
		case iface_cells:
			if (!PyString_Check((PyObject*) pyObjNext)) { PyErr_SetString(PyExc_RuntimeError,"String expected."); return false; }
			*param = (intptr_t) PyString_AsString(pyObjNext);
			break;
		case iface_textrange:
			PyErr_SetString(PyExc_RuntimeError,"raw textrange unsupported, but you can use CScite.Editor.Textrange(s,e)");  return false;
			break;
		default: {  PyErr_SetString(PyExc_RuntimeError,"Unexpected: receiving unknown scintilla type."); return false; }
	}
	return true;
}
bool pushPythonArgument(IFaceType type, intptr_t param, PyObject** pyValueOut /* caller must incref this! */)
{
	switch(type) {
		case iface_void:
			*pyValueOut = Py_None;
			break;
		case iface_int:
		case iface_length:
		case iface_position:
		case iface_colour:
			*pyValueOut = PyInt_FromLong((long) param);
			break;
		case iface_bool:
			*pyValueOut = param ? Py_True : Py_False;
			break;
		default: {  PyErr_SetString(PyExc_RuntimeError,"Unexpected: returning unknown scintilla type."); return false; }
	}
	return true;
}
inline bool getPaneFromInt(int nPane, ExtensionAPI::Pane* outPane)
{
	if (nPane==0) *outPane = ExtensionAPI::paneEditor;
	else if (nPane==1) *outPane = ExtensionAPI::paneOutput;
	else { PyErr_SetString(PyExc_RuntimeError,"Invalid pane, must be 0 or 1."); return false; }
	return true;
}
int FindFriendlyNamedIDMConstant(const char *name) {
	// pattern copied from IFaceTable.cxx
	int lo = 0;
	int hi = PythonExtension::lengthfriendlyconstants - 1;
	do {
		int idx = (lo+hi)/2;
		int cmp = strcmp(name, PythonExtension::friendlyconstants[idx].name);
		if (cmp > 0) {
			lo = idx + 1;
		} else if (cmp < 0) {
			hi = idx - 1;
		} else {
			return idx;
		}
	} while (lo <= hi);
	return -1;
}

void trace(const char *szText1, const char *szText2/* =NULL */)
{
	if (!_host) return;
	if (szText1) _host->Trace(szText1);
	if (szText2) _host->Trace(szText2); 
}
void trace(const char *szText1, const char *szText2, int n)
{
	trace(szText1, szText2);
	char buf[256] = {0};
	int count = snprintf(buf, sizeof(buf), "%d", n);
	if (count > sizeof(buf) || count<0) return;
	_host->Trace(buf);
}


static IFaceConstant rgFriendlyNamedIDMConstants[] = {
{"Abbrev",IDM_ABBREV},
{"About",IDM_ABOUT},
{"Activate",IDM_ACTIVATE},
{"BlockComment",IDM_BLOCK_COMMENT},
{"BookmarkClearall",IDM_BOOKMARK_CLEARALL},
{"BookmarkNext",IDM_BOOKMARK_NEXT},
{"BookmarkNextSelect",IDM_BOOKMARK_NEXT_SELECT},
{"BookmarkPrev",IDM_BOOKMARK_PREV},
{"BookmarkPrevSelect",IDM_BOOKMARK_PREV_SELECT},
{"BookmarkToggle",IDM_BOOKMARK_TOGGLE},
{"BoxComment",IDM_BOX_COMMENT},
{"Buffer",IDM_BUFFER},
{"Buffersep",IDM_BUFFERSEP},
{"Build",IDM_BUILD},
{"Clear",IDM_CLEAR},
{"ClearOutput",IDM_CLEAROUTPUT},
{"Close",IDM_CLOSE},
{"Closeall",IDM_CLOSEALL},
{"Compile",IDM_COMPILE},
{"Complete",IDM_COMPLETE},
{"CompleteWord",IDM_COMPLETEWORD},
{"Copy",IDM_COPY},
{"CopyAsrtf",IDM_COPYASRTF},
{"CopyPath",IDM_COPYPATH},
{"Cut",IDM_CUT},
{"DirectionDown",IDM_DIRECTIONDOWN},
{"DirectionUp",IDM_DIRECTIONUP},
{"Duplicate",IDM_DUPLICATE},
{"Encoding_default",IDM_ENCODING_DEFAULT},
{"Encoding_ucookie",IDM_ENCODING_UCOOKIE},
{"Encoding_ucs2be",IDM_ENCODING_UCS2BE},
{"Encoding_ucs2le",IDM_ENCODING_UCS2LE},
{"Encoding_utf8",IDM_ENCODING_UTF8},
{"EnterSelection",IDM_ENTERSELECTION},
{"Eol_convert",IDM_EOL_CONVERT},
{"Eol_cr",IDM_EOL_CR},
{"Eol_crlf",IDM_EOL_CRLF},
{"Eol_lf",IDM_EOL_LF},
{"Expand",IDM_EXPAND},
{"ExpandEnsurechildrenvisible",IDM_EXPAND_ENSURECHILDRENVISIBLE},
{"Filer",IDM_FILER},
{"Find",IDM_FIND},
{"FindInFilesDialog",IDM_FINDINFILES},
{"FindInFilesStart",IDM_FINDINFILESSTART},
{"FindNext",IDM_FINDNEXT},
{"FindNextBack",IDM_FINDNEXTBACK},
{"FindNextBackSel",IDM_FINDNEXTBACKSEL},
{"FindNextSel",IDM_FINDNEXTSEL},
{"FinishedExecute",IDM_FINISHEDEXECUTE},
{"FoldMargin",IDM_FOLDMARGIN},
{"Fullscreen",IDM_FULLSCREEN},
{"Go",IDM_GO},
{"Goto",IDM_GOTO},
{"Help",IDM_HELP},
{"HelpScite",IDM_HELP_SCITE},
{"Import",IDM_IMPORT},
{"IncSearch",IDM_INCSEARCH},
{"InsAbbrev",IDM_INS_ABBREV},
{"Join",IDM_JOIN},
{"Language",IDM_LANGUAGE},
{"LineNumberMargin",IDM_LINENUMBERMARGIN},
{"LoadSession",IDM_LOADSESSION},
{"LwrCase",IDM_LWRCASE},
{"MacroList",IDM_MACROLIST},
{"MacroPlay",IDM_MACROPLAY},
{"MacroRecord",IDM_MACRORECORD},
{"MacroSep",IDM_MACRO_SEP},
{"MacroStoprecord",IDM_MACROSTOPRECORD},
{"MatchBrace",IDM_MATCHBRACE},
{"MatchCase",IDM_MATCHCASE},
{"MonoFont",IDM_MONOFONT},
{"MoveTableft",IDM_MOVETABLEFT},
{"MoveTabright",IDM_MOVETABRIGHT},
{"MruFile",IDM_MRUFILE},
{"MruSep",IDM_MRU_SEP},
{"New",IDM_NEW},
{"NextFile",IDM_NEXTFILE},
{"NextFilestack",IDM_NEXTFILESTACK},
{"NextMatchppc",IDM_NEXTMATCHPPC},
{"NextMsg",IDM_NEXTMSG},
{"OnTop",IDM_ONTOP},
{"Open",IDM_OPEN},
{"OpenAbbrevproperties",IDM_OPENABBREVPROPERTIES},
{"OpenDirectoryproperties",IDM_OPENDIRECTORYPROPERTIES},
{"OpenFileshere",IDM_OPENFILESHERE},
{"OpenGlobalproperties",IDM_OPENGLOBALPROPERTIES},
{"OpenLocalproperties",IDM_OPENLOCALPROPERTIES},
{"OpenLuaexternalfile",IDM_OPENLUAEXTERNALFILE},
{"OpenSelected",IDM_OPENSELECTED},
{"OpenUserproperties",IDM_OPENUSERPROPERTIES},
{"Paste",IDM_PASTE},
{"PasteAnddown",IDM_PASTEANDDOWN},
{"PrevFile",IDM_PREVFILE},
{"PrevFlestack",IDM_PREVFILESTACK},
{"PrevMatchppc",IDM_PREVMATCHPPC},
{"PrevMsg",IDM_PREVMSG},
{"Print",IDM_PRINT},
{"PrintSetup",IDM_PRINTSETUP},
{"Quit",IDM_QUIT},
{"Readonly",IDM_READONLY},
{"Redo",IDM_REDO},
{"Regexp",IDM_REGEXP},
{"Replace",IDM_REPLACE},
{"Revert",IDM_REVERT},
{"RunWin",IDM_RUNWIN},
{"Save",IDM_SAVE},
{"SaveAcopy",IDM_SAVEACOPY},
{"SaveAll",IDM_SAVEALL},
{"SaveAs",IDM_SAVEAS},
{"SaveAshtml",IDM_SAVEASHTML},
{"SaveAspdf",IDM_SAVEASPDF},
{"SaveAsrtf",IDM_SAVEASRTF},
{"SaveAstex",IDM_SAVEASTEX},
{"SaveAsxml",IDM_SAVEASXML},
{"SaveSession",IDM_SAVESESSION},
{"SelMargin",IDM_SELMARGIN},  //apparently caps first.
{"SelectAll",IDM_SELECTALL},
{"SelectToBrace",IDM_SELECTTOBRACE},
{"SelectToNextmatchppc",IDM_SELECTTONEXTMATCHPPC},
{"SelectToPrevmatchppc",IDM_SELECTTOPREVMATCHPPC},
{"ShowCalltip",IDM_SHOWCALLTIP},
{"Split",IDM_SPLIT},
{"SplitVertical",IDM_SPLITVERTICAL},
{"SrcWin",IDM_SRCWIN},
{"StatusWin",IDM_STATUSWIN},
{"StopExecute",IDM_STOPEXECUTE},
{"StreamComment",IDM_STREAM_COMMENT},
{"SwitchPane",IDM_SWITCHPANE},
{"TabSize",IDM_TABSIZE},
{"TabWin",IDM_TABWIN},
{"ToggleFoldAll",IDM_TOGGLE_FOLDALL},
{"ToggleFoldRecursive",IDM_TOGGLE_FOLDRECURSIVE},
{"ToggleOutput",IDM_TOGGLEOUTPUT},
{"ToggleParameters",IDM_TOGGLEPARAMETERS},
{"ToolWin",IDM_TOOLWIN}, //apparently caps first.
{"Tools",IDM_TOOLS},
{"Undo",IDM_UNDO},
{"Unslash",IDM_UNSLASH},
{"UprCase",IDM_UPRCASE},
{"ViewEol",IDM_VIEWEOL},
{"ViewGuides",IDM_VIEWGUIDES},
{"ViewSpace",IDM_VIEWSPACE},
{"ViewStatusbar",IDM_VIEWSTATUSBAR},
{"ViewTabbar",IDM_VIEWTABBAR},
{"ViewToolbar",IDM_VIEWTOOLBAR},
{"WholeWord",IDM_WHOLEWORD},
{"Wrap",IDM_WRAP},
{"WrapAround",IDM_WRAPAROUND},
{"WrapOutput",IDM_WRAPOUTPUT},
};
const IFaceConstant * const PythonExtension::friendlyconstants = rgFriendlyNamedIDMConstants;
const size_t PythonExtension::lengthfriendlyconstants = _countof(rgFriendlyNamedIDMConstants);

