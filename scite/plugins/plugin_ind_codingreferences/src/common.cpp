//#define GetRValue(c) ((char)(c))
//#define GetGValue(c) ((char)(((WORD)(c))>>8))
//#define GetBValue(c) ((char)((c)>>16))
//#define RGB(r,g,b) ((long)((char)(r)|((char)(g) << 8)|((char)(b) << 16)))

//Use UPX to xompress this

static wxString IntToString(int n)
{
    wxString stringnumber = wxString::Format(wxT("%d"), n);
    return stringnumber;
}
static int StringToInt(wxString stri)
{
    long n; bool res = stri.ToLong(&n);
    if (res) return (int) n;
    else return 0;
}

static wxString HexToString(unsigned char ch1, unsigned char ch2, unsigned char ch3)
{
    wxString strr = wxString::Format(wxT("%x"),  ch1);  strr = (strr.Length()==1) ? "0"+strr : strr;
    wxString strg = wxString::Format(wxT("%x"),  ch2);  strg = (strg.Length()==1) ? "0"+strg : strg;
    wxString strb = wxString::Format(wxT("%x"),  ch3);  strb = (strb.Length()==1) ? "0"+strb : strb;
    return "#" + strr + strg + strb;
}
int StringToHex(wxString stri)
{
    long n; bool res = stri.ToLong(&n, 16);
    if (res) return (int) n;
    else return 0;
}
