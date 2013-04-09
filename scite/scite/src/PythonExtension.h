// SciTE Python Extension (Preview)
// Ben Fisher, 2011

#include "..\python\include\python.h"

#include "IFaceTable.h"

#include <string>
#include <vector>
#include <map>

class CPyObjStrong
{
private:
	PyObject* m_pyo;
public:
	CPyObjStrong() { m_pyo = NULL; }
	CPyObjStrong(PyObject* pyo) { m_pyo = pyo; }
	void Attach(PyObject* pyo) { m_pyo = pyo; }
	~CPyObjStrong() { if (m_pyo) Py_DECREF(m_pyo); }
	operator PyObject*() { return m_pyo; }
	
};

// unnecessary, but makes code more consistent, clear that we don't own the reference
class CPyObjWeak 
{
private:
	PyObject* m_pyo;
public:
	CPyObjWeak(PyObject* pyo) { m_pyo = pyo; }
	~CPyObjWeak() { /* do not need to decref */ }
	operator PyObject*() { return m_pyo; }
};

int FindFriendlyNamedIDMConstant(const char *name);
inline bool getPaneFromInt(int nPane, ExtensionAPI::Pane* outPane);
bool pullPythonArgument(IFaceType type, CPyObjWeak pyObjNext, intptr_t* param);
bool pushPythonArgument(IFaceType type, intptr_t param, PyObject** pyValueOut /* caller must incref this! */);
void trace(const char *szText1, const char *szText2=NULL);
void trace(const char *szText1, const char *szText2, int n);

class PythonExtension : public Extension
{

private:
	void writeLog(const char *wzError);
	bool writeError(const char *wzError);
	bool writeError(const char *wzError, const char *wzError2);
	bool _runCallback(const char* szNameOfFunction, int nArgs, const char* szArg1);
	bool _runCallbackArgs(const char* szNameOfFunction, PyObject* pArgsBorrowed);
	void InitializePython();
	void SetupPythonNamespace();

public:
	void writeText(const char *szText);

private:
	PythonExtension(); // Singleton
	PythonExtension(const PythonExtension &); // Disable copy ctor
	void operator=(const PythonExtension &); // Disable operator=

	
public:
	static const IFaceConstant * const friendlyconstants;
	static const size_t lengthfriendlyconstants;
	static PythonExtension &Instance();

	virtual ~PythonExtension();

	virtual bool Initialise(ExtensionAPI *host);
	virtual bool Finalise();
	virtual bool Clear();
	virtual bool Load(const char *fileName);

	virtual bool InitBuffer(int index);
	virtual bool ActivateBuffer(int index);
	virtual bool RemoveBuffer(int index);

	virtual bool OnExecute(const char *s);

	// file events
	virtual bool OnOpen(const char *fileName);
	virtual bool OnClose(const char *filename);
	virtual bool OnSwitchFile(const char *fileName);
	virtual bool OnBeforeSave(const char *fileName);
	virtual bool OnSave(const char *fileName);
	virtual bool OnSavePointReached();
	virtual bool OnSavePointLeft();
	// input events
	virtual bool OnChar(char ch);
	virtual bool OnKey(int keycode, int modifiers);
	virtual bool OnDoubleClick();
	virtual bool OnMarginClick();
	virtual bool OnDwellStart(int pos, const char *word);
	// misc events
	virtual bool OnUserListSelection(int type, const char *selection);
	
};

