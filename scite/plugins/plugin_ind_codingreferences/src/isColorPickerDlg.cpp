//---------------------------------------------------------------------------
//
// Name:        isColorPickerDlg.cpp
// Author:      bfisher
// Created:     1/8/2007 9:58:03 PM
// Description: isColorPickerDlg class implementation
//
//---------------------------------------------------------------------------


#include "isColorPickerDlg.h"
#include "common.cpp"

//Do not add custom headers
//wxDev-C++ designer will remove them
////Header Include Start
#include "btnColorDialog_XPM.xpm"
////Header Include End

//----------------------------------------------------------------------------
// isColorPickerDlg
//----------------------------------------------------------------------------
//Add Custom Events only in the appropriate block.
//Code added in other places will be removed by wxDev-C++
////Event Table Start
BEGIN_EVENT_TABLE(isColorPickerDlg,wxDialog)
	////Manual Code Start
	EVT_TEXT_ENTER(ID_RTEXT,isColorPickerDlg::rTextUpdated)
	EVT_TEXT_ENTER(ID_GTEXT,isColorPickerDlg::gTextUpdated)
	EVT_TEXT_ENTER(ID_BTEXT,isColorPickerDlg::bTextUpdated)
	EVT_TEXT_ENTER(ID_TEXTHEX,isColorPickerDlg::textHexUpdated)
	////Manual Code End
	
	EVT_CLOSE(isColorPickerDlg::OnClose)
	EVT_BUTTON(wxID_CANCEL,isColorPickerDlg::btnCancelClick)
	EVT_BUTTON(ID_BTNCOLORDIALOG,isColorPickerDlg::btnColorDialogClick)
	
	EVT_COMMAND_SCROLL(ID_BSLIDER,isColorPickerDlg::bSliderScroll)
	
	EVT_COMMAND_SCROLL(ID_GSLIDER,isColorPickerDlg::gSliderScroll)
	EVT_BUTTON(ID_BTNOK,isColorPickerDlg::btnOKClick)
	
	EVT_COMMAND_SCROLL(ID_RSLIDER,isColorPickerDlg::rSliderScroll)
END_EVENT_TABLE()
////Event Table End

isColorPickerDlg::isColorPickerDlg(wxWindow *parent, wxWindowID id, const wxString &title, const wxPoint &position, const wxSize& size, long style)
: wxDialog(parent, id, title, position, size, style)
{
	CreateGUIControls();
}

isColorPickerDlg::~isColorPickerDlg()
{
} 

void isColorPickerDlg::CreateGUIControls()
{
	//Do not add custom code here
	//wxDev-C++ designer will remove them.
	//Add the custom code before or after the blocks
	////GUI Items Creation Start

	WxPanel1 = new wxPanel(this, ID_WXPANEL1, wxPoint(0,0), wxSize(523,258), wxTAB_TRAVERSAL);

	rSlider = new wxSlider(WxPanel1, ID_RSLIDER, 0, 0, 255, wxPoint(47,61), wxSize(168,22), wxSL_HORIZONTAL | wxSL_SELRANGE , wxDefaultValidator, wxT("rSlider"));
	rSlider->SetRange(0,255);
	rSlider->SetValue(0);

	rText = new wxTextCtrl(WxPanel1, ID_RTEXT, wxT("0"), wxPoint(231,61), wxSize(59,21), wxTE_PROCESS_ENTER, wxDefaultValidator, wxT("rText"));

	previewColor = new wxPanel(WxPanel1, ID_PREVIEWCOLOR, wxPoint(344,42), wxSize(150,125));
	previewColor->SetBackgroundColour(wxColour(0,0,0));

	btnOK = new wxButton(WxPanel1, ID_BTNOK, wxT("OK"), wxPoint(345,211), wxSize(65,25), 0, wxDefaultValidator, wxT("btnOK"));

	WxStaticText1 = new wxStaticText(WxPanel1, ID_WXSTATICTEXT1, wxT("R:"), wxPoint(23,61), wxDefaultSize, 0, wxT("WxStaticText1"));

	WxStaticText2 = new wxStaticText(WxPanel1, ID_WXSTATICTEXT2, wxT("G:"), wxPoint(23,101), wxDefaultSize, 0, wxT("WxStaticText2"));

	gSlider = new wxSlider(WxPanel1, ID_GSLIDER, 0, 0, 255, wxPoint(47,101), wxSize(168,22), wxSL_HORIZONTAL | wxSL_SELRANGE , wxDefaultValidator, wxT("gSlider"));
	gSlider->SetRange(0,255);
	gSlider->SetValue(0);

	gText = new wxTextCtrl(WxPanel1, ID_GTEXT, wxT("0"), wxPoint(231,101), wxSize(59,21), wxTE_PROCESS_ENTER, wxDefaultValidator, wxT("gText"));

	WxStaticText3 = new wxStaticText(WxPanel1, ID_WXSTATICTEXT3, wxT("B:"), wxPoint(23,138), wxDefaultSize, 0, wxT("WxStaticText3"));

	bSlider = new wxSlider(WxPanel1, ID_BSLIDER, 0, 0, 255, wxPoint(47,138), wxSize(168,22), wxSL_HORIZONTAL | wxSL_SELRANGE , wxDefaultValidator, wxT("bSlider"));
	bSlider->SetRange(0,255);
	bSlider->SetValue(0);

	bText = new wxTextCtrl(WxPanel1, ID_BTEXT, wxT("0"), wxPoint(231,138), wxSize(59,21), wxTE_PROCESS_ENTER, wxDefaultValidator, wxT("bText"));

	wxBitmap btnColorDialog_BITMAP (btnColorDialog_XPM);
	btnColorDialog = new wxBitmapButton(WxPanel1, ID_BTNCOLORDIALOG, btnColorDialog_BITMAP, wxPoint(20,199), wxSize(45,39), wxBU_AUTODRAW, wxDefaultValidator, wxT("btnColorDialog"));

	debug = new wxTextCtrl(WxPanel1, ID_DEBUG, wxT("debug"), wxPoint(467,174), wxSize(121,21), 0, wxDefaultValidator, wxT("debug"));
	debug->Show(false);

	btnCancel = new wxButton(WxPanel1, wxID_CANCEL, wxT("Cancel"), wxPoint(419,211), wxSize(75,25), 0, wxDefaultValidator, wxT("btnCancel"));

	textHex = new wxTextCtrl(WxPanel1, ID_TEXTHEX, wxT("#000000"), wxPoint(202,211), wxSize(89,21), wxTE_PROCESS_ENTER, wxDefaultValidator, wxT("textHex"));

	dlgColor =  new wxColourDialog(this);

	SetTitle(wxT("isColorPicker"));
	SetIcon(wxNullIcon);
	SetSize(8,8,531,292);
	Center();
	
	////GUI Items Creation End
	btnOK->SetDefault();
	rText->SetFocus();
	rText->SelectAll();
}

void isColorPickerDlg::OnClose(wxCloseEvent& /*event*/)
{
	Destroy();
}

/*
 * rSliderScroll
 */
 void isColorPickerDlg::OnScroll(wxSlider * slider, wxTextCtrl * text)
{
   
	RefreshColor();
}
void isColorPickerDlg::OnEnterComponentText(wxSlider * slider, wxTextCtrl * text)
{
	int ret = StringToInt(text->GetValue());
	if (ret>255 ) ret = 255; if (ret < 0) ret = 0;
	slider->SetValue(ret);
	RefreshColor();
}
void isColorPickerDlg::RefreshColor()
{
	unsigned char r = (unsigned char) rSlider->GetValue(),  g=(unsigned char)gSlider->GetValue(),  b=(unsigned char)bSlider->GetValue();
	wxColour colour(r,g,b);
	textHex->SetValue(HexToString(r,g,b));
	
	 rText->SetValue(IntToString(rSlider->GetValue()));
	 gText->SetValue(IntToString(gSlider->GetValue()));
	 bText->SetValue(IntToString(bSlider->GetValue()));
	
	previewColor->SetBackgroundColour(colour);
	previewColor->SetForegroundColour(colour);
	previewColor->Refresh();
}

void isColorPickerDlg::rSliderScroll(wxScrollEvent& event) { OnScroll(rSlider, rText); }
void isColorPickerDlg::gSliderScroll(wxScrollEvent& event) { OnScroll(gSlider, gText); }
void isColorPickerDlg::bSliderScroll(wxScrollEvent& event) { OnScroll(bSlider, bText); }
 
void isColorPickerDlg::rTextUpdated(wxCommandEvent& event) { OnEnterComponentText(rSlider, rText); gText->SetFocus(); gText->SelectAll(); }
void isColorPickerDlg::gTextUpdated(wxCommandEvent& event) { OnEnterComponentText(gSlider, gText); bText->SetFocus(); bText->SelectAll(); }
void isColorPickerDlg::bTextUpdated(wxCommandEvent& event) { OnEnterComponentText(bSlider, bText); btnOK->SetFocus(); }
 



void isColorPickerDlg::btnColorDialogClick(wxCommandEvent& event)
{
	wxColourData  cdata;
	cdata.SetCustomColour(0, previewColor->GetBackgroundColour());
	wxColourDialog dlg(this, &cdata);
	// dlg.Create();// this, cdata);
	
	if (dlg.ShowModal()==wxID_OK)
	{
		   wxColour a = dlg.GetColourData().GetColour();
		   
		   rSlider->SetValue((int) a.Red());
		   gSlider->SetValue((int)a.Green());
		   bSlider->SetValue((int)a.Blue());
	}
	RefreshColor();
}
void isColorPickerDlg::textHexUpdated(wxCommandEvent& event)
{
	//Parse it
	wxString str = textHex->GetValue();
	if (str.Left(1)!="#") str = "#" + str;
	int r = StringToHex( str.Mid(1,2) );
	int g = StringToHex( str.Mid(3,2) );
	int b = StringToHex( str.Mid(5,2) );
	rSlider->SetValue(r); gSlider->SetValue(g); bSlider->SetValue(b);

	RefreshColor();
}


void isColorPickerDlg::btnCancelClick(wxCommandEvent& event)
{
	Close(true);
}

#include <wx/msw/winundef.h>
#include "SciteDirector.cpp"
#include <windows.h>

void isColorPickerDlg::btnOKClick(wxCommandEvent& event)
{
	int nmsg;
	HWND results[100];
	results[0] = 0;
	EnumWindows(EnumWindowsProc,(long)results);
	nmsg = size_of_array(results);

	if (nmsg == 0) //No versions of Scite are open. 
	{
		//res = launch_scite(args[0], "output:Now that worked.");
		//if (res)
		//	retstr = istrdup("new:success");
		//else
		//	retstr = istrdup("new:failure");
	}
	else //Pick the first instance of Scite found.
	{
		wxString params;
		params = "extender:import scmsg; scmsg.sd(\"," + IntToString(rSlider->GetValue()) + "," +
		 IntToString(gSlider->GetValue()) + "," +IntToString(bSlider->GetValue()) + "," + textHex->GetValue() +
		 ",\")";
		
		SendToHandle(results[0], params.c_str());
		rSlider->SetValue(255);
	}
		
	Close(true);
}

