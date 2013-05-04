//---------------------------------------------------------------------------
//
// Name:        isColorPickerDlg.h
// Author:      bfisher
// Created:     1/8/2007 9:58:03 PM
// Description: isColorPickerDlg class declaration
//
//---------------------------------------------------------------------------

#ifndef __ISCOLORPICKERDLG_h__
#define __ISCOLORPICKERDLG_h__

#ifdef __BORLANDC__
	#pragma hdrstop
#endif

#ifndef WX_PRECOMP
	#include <wx/wx.h>
	#include <wx/dialog.h>
#else
	#include <wx/wxprec.h>
#endif

//Do not add custom headers
//wxDev-C++ designer will remove them
////Header Include Start
#include <wx/colordlg.h>
#include <wx/bmpbuttn.h>
#include <wx/stattext.h>
#include <wx/button.h>
#include <wx/textctrl.h>
#include <wx/slider.h>
#include <wx/panel.h>
////Header Include End

////Dialog Style Start
#undef isColorPickerDlg_STYLE
#define isColorPickerDlg_STYLE wxCAPTION | wxSYSTEM_MENU | wxDIALOG_NO_PARENT | wxDIALOG_EX_CONTEXTHELP | wxCLOSE_BOX
////Dialog Style End

class isColorPickerDlg : public wxDialog
{
	private:
		DECLARE_EVENT_TABLE();
		
	public:
         
		isColorPickerDlg(wxWindow *parent, wxWindowID id = 1, const wxString &title = wxT("isColorPicker"), const wxPoint& pos = wxDefaultPosition, const wxSize& size = wxDefaultSize, long style = isColorPickerDlg_STYLE);
		virtual ~isColorPickerDlg();
		void rSliderScroll(wxScrollEvent& event);
		void gSliderScroll(wxScrollEvent& event);
		void bSliderScroll(wxScrollEvent& event);
		void rTextUpdated(wxCommandEvent& event);
		void gTextUpdated(wxCommandEvent& event);
		void bTextUpdated(wxCommandEvent& event);
	
	private:
		//Do not add custom control declarations
		//wxDev-C++ will remove them. Add custom code after the block.
		////GUI Control Declaration Start
		wxColourDialog *dlgColor;
		wxTextCtrl *textHex;
		wxButton *btnCancel;
		wxTextCtrl *debug;
		wxBitmapButton *btnColorDialog;
		wxTextCtrl *bText;
		wxSlider *bSlider;
		wxStaticText *WxStaticText3;
		wxTextCtrl *gText;
		wxSlider *gSlider;
		wxStaticText *WxStaticText2;
		wxStaticText *WxStaticText1;
		wxButton *btnOK;
		wxPanel *previewColor;
		wxTextCtrl *rText;
		wxSlider *rSlider;
		wxPanel *WxPanel1;
		////GUI Control Declaration End
		
		
	private:
		//Note: if you receive any error with these enum IDs, then you need to
		//change your old form code that are based on the #define control IDs.
		//#defines may replace a numeric value for the enum names.
		//Try copy and pasting the below block in your old form header files.
		enum
		{
			////GUI Enum Control ID Start
			ID_TEXTHEX = 1030,
			ID_DEBUG = 1028,
			ID_BTNCOLORDIALOG = 1027,
			ID_BTEXT = 1026,
			ID_BSLIDER = 1025,
			ID_WXSTATICTEXT3 = 1024,
			ID_GTEXT = 1020,
			ID_GSLIDER = 1019,
			ID_WXSTATICTEXT2 = 1018,
			ID_WXSTATICTEXT1 = 1014,
			ID_BTNOK = 1012,
			ID_PREVIEWCOLOR = 1011,
			ID_RTEXT = 1009,
			ID_RSLIDER = 1003,
			ID_WXPANEL1 = 1001,
			////GUI Enum Control ID End
			ID_DUMMY_VALUE_ //don't remove this value unless you have other enum values
		};
	
	private:
    
		void OnClose(wxCloseEvent& event);
		void CreateGUIControls();
		
		void textHexUpdated(wxCommandEvent& event); 
        void OnScroll(wxSlider * , wxTextCtrl * );  
        void OnEnterComponentText( wxSlider *, wxTextCtrl * );
       
    public:
            void RefreshColor();
		void btnColorDialogClick(wxCommandEvent& event);
		void btnCancelClick(wxCommandEvent& event);
		void btnOKClick(wxCommandEvent& event);
    
};

#endif
