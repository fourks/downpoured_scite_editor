//---------------------------------------------------------------------------
//
// Name:        isColorPickerApp.h
// Author:      bfisher
// Created:     1/8/2007 9:58:03 PM
// Description: 
//
//---------------------------------------------------------------------------

#ifndef __ISCOLORPICKERDLGApp_h__
#define __ISCOLORPICKERDLGApp_h__

#ifdef __BORLANDC__
	#pragma hdrstop
#endif

#ifndef WX_PRECOMP
	#include <wx/wx.h>
#else
	#include <wx/wxprec.h>
#endif

class isColorPickerDlgApp : public wxApp
{
	public:
		bool OnInit();
		int OnExit();
};

#endif
