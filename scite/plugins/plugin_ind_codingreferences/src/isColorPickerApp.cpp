//---------------------------------------------------------------------------
//
// Name:        isColorPickerApp.cpp
// Author:      bfisher
// Created:     1/8/2007 9:58:03 PM
// Description: 
//
//---------------------------------------------------------------------------

#include "isColorPickerApp.h"
#include "isColorPickerDlg.h"

IMPLEMENT_APP(isColorPickerDlgApp)

bool isColorPickerDlgApp::OnInit()
{
	isColorPickerDlg* dialog = new isColorPickerDlg(NULL);
	SetTopWindow(dialog);
	dialog->Show(true);		
	return true;
}
 
int isColorPickerDlgApp::OnExit()
{
	return 0;
}
