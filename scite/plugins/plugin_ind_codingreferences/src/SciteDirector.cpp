

static void SendToHandle(HWND hwnd, const char *Message)
{
  COPYDATASTRUCT cds;
  int size = strlen(Message);
  cds.dwData = 0;
  cds.lpData = (void *)Message;
  cds.cbData = size;
  SendMessage(hwnd, WM_COPYDATA,(WPARAM)NULL,(LPARAM)&cds);
}

static int size_of_array(HWND* results)
{
  int idx = 0;
  // find our place in the output array
  for (idx = 0; results[idx] != NULL; idx++) ;
  return idx;
}

//Searches through all of the open windows that respond to the director interface.
BOOL CALLBACK EnumWindowsProc(HWND  hwnd, LPARAM  lParam)
{
  HWND* results = (HWND*)lParam;
  int idx = size_of_array(results);
  char buff[256];
  GetClassName(hwnd,buff,sizeof(buff));
  if (strcmp(buff,"DirectorExtension") == 0) {
	//printf("found %x\n",hwnd);
	results[idx] = hwnd;
	results[idx+1] = NULL;
  }
  return TRUE;
}

static BOOL launch_scite(const char *path,const char *command)
{
   char buff[1024];

   sprintf(buff,"%s -%s",path,command);
   return  (WinExec(buff,SW_SHOW) > 31);
}
