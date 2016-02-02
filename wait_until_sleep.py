import time
from timeit import default_timer
import subprocess
import os
#print time.strftime('%X')




import ctypes, ctypes.wintypes

# http://msdn.microsoft.com/en-us/library/ms646272(VS.85).aspx
# typedef struct tagLASTINPUTINFO {
#     UINT cbSize;
#     DWORD dwTime;
# } LASTINPUTINFO, *PLASTINPUTINFO;

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [
      ('cbSize', ctypes.wintypes.UINT),
      ('dwTime', ctypes.wintypes.DWORD),
      ]

PLASTINPUTINFO = ctypes.POINTER(LASTINPUTINFO)

# http://msdn.microsoft.com/en-us/library/ms646302(VS.85).aspx
# BOOL GetLastInputInfo(PLASTINPUTINFO plii);

user32 = ctypes.windll.user32
GetLastInputInfo = user32.GetLastInputInfo
GetLastInputInfo.restype = ctypes.wintypes.BOOL
GetLastInputInfo.argtypes = [PLASTINPUTINFO]

kernel32 = ctypes.windll.kernel32
GetTickCount = kernel32.GetTickCount
Sleep = kernel32.Sleep

def wait_until_idle(idle_time=60):
    """Wait until no more user activity is detected.

    This function won't return until `idle_time` seconds have elapsed
    since the last user activity was detected.
    """

    idle_time_ms = int(idle_time*1000)
    liinfo = LASTINPUTINFO()
    liinfo.cbSize = ctypes.sizeof(liinfo)
    while True:
        GetLastInputInfo(ctypes.byref(liinfo))
        elapsed = GetTickCount() - liinfo.dwTime
        if elapsed>=idle_time_ms:
            break
        Sleep(idle_time_ms - elapsed or 1)


def wait_until_active(tol=5):
    """Wait until awakened by user activity.

    This function will block and wait until some user activity
    is detected. Because of the polling method used, it may return
    `tol` seconds (or less) after user activity actually began.
    """

    liinfo = LASTINPUTINFO()
    liinfo.cbSize = ctypes.sizeof(liinfo)
    lasttime = None
    delay = 1 # ms
    maxdelay = int(tol*1000)
    while True:
        GetLastInputInfo(ctypes.byref(liinfo))
        if lasttime is None: lasttime = liinfo.dwTime
        if lasttime != liinfo.dwTime:
            break
        delay = min(2*delay, maxdelay)
        Sleep(delay)

def test():
    print("Waiting for 3 minutes of no user input...")
    wait_until_idle(180)
    user32.MessageBeep(0)
    print("Ok. Now, putting the computer to sleep in 20 seconds!")
    time.sleep(20)
    os.system("D:/Py/sleep.bat")
    

if __name__=='__main__':
    test()