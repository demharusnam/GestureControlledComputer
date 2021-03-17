from time import sleep
from ctypes import * #no need to load windows 32 DLL files since ctypes has it as a module
#imports windll, Structure, Union, c_ulong32, POINTER, byref

#NOTE: Always pass structs or unions to functions by pointer

#data types: https://docs.microsoft.com/en-us/windows/win32/winprog/windows-data-types
UINT = c_uint32
int = c_int32
LONG = c_int32 #LONG = 32 bit signed int = c_int32 = c_int
ULONG_PTR = POINTER(c_uint32) #ULONG_PTR = unsigned LONG_PTR = unsigned long pointer = 32 bit unsigned int ptr = c_uint32 ptr = c_uint ptr
DWORD = c_uint32 #DWORD = 32 bit unsigned int = c_uint32 = c_uint
WORD = c_uint16 #WORD = 16 bit unsigned int = c_uint16

# https://docs.microsoft.com/en-us/windows/win32/winprog/windows-data-types
class MOUSEINPUT(Structure):
    _fields_ = [("dx", LONG), #LONG
                ("dy", LONG), #LONG
                ("mouseData", DWORD), #DWORD
                ("dwFlags", DWORD), #DWORD
                ("time", DWORD), #DWORD for timestamp, put as 0 so system provides its own timestamp
                ("dwExtraInfo", ULONG_PTR)] #ULONG_PTR

#flags for MOUSEINPUT dwFlags parameter
MOUSEEVENTF_ABSOLUTE = 0x8000 #specify absolute coordinates to move mouse to
MOUSEEVENTF_MOVE = 0x0001 #mouse has moved
MOUSEEVENTF_HWHEEL = 0x01000 #mouse wheel moved horizontally (+ for right, - for left)
MOUSEEVENTF_WHEEL = 0x0800 #mouse wheel moved vertically (+ for up, - for down)
MOUSEEVENTF_VIRTUALDESK = 0x4000 #move mouse to absolute desktop screen coordinates
                                # Must be used with MOUSEEVENTF_ABSOLUTE.
MOUSEEVENTF_LEFTDOWN = 0x0002 #press left mouse button
MOUSEEVENTF_LEFTUP = 0x0004 #release left mouse button
MOUSEEVENTF_RIGHTDOWN = 0x0008 #press right mouse button
MOUSEEVENTF_RIGHTUP = 0x0010 #release right mouse button

# https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-keybdinput
class KEYBDINPUT(Structure):
    _fields_ = [("wVk", WORD), #WORD
                ("wScan", WORD), #WORD
                ("dwFlags", DWORD), #DWORD
                ("time", DWORD), #DWORD
                ("dwExtraInfo", ULONG_PTR)] #ULONG_PTR

KEYEVENTF_KEYUP = 0x0002

#virtual keys: https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
VK = {}
VK["LBUTTON"] = 0x01
VK["RBUTTON"] = 0x02
VK["BACK"] = 0X08
VK["TAB"] = 0x09
VK["CLEAR"] = 0x0C
VK["RETURN"] = 0x0D
VK["SHIFT"] = 0x10
VK["CONTROL"] = 0x11
VK["MENU"] = 0x12 #alt key?
VK["PAUSE"] = 0x13
VK["CAPITAL"] = 0x14 #caps lock key?
VK["ESCAPE"] = 0x1B
VK["SPACE"] = 0x20
VK["PRIOR"] = 0x21
VK["NEXT"] = 0x22
VK["END"] = 0x23
VK["HOME"] = 0x24
VK["LEFT"] = 0x25
VK["UP"] = 0x26
VK["RIGHT"] = 0x27
VK["DOWN"] = 0x28
VK["SELECT"] = 0x29
VK["PRINT"] = 0x2A
VK["EXECUTE"] =0x2B #don't know what key this is?
VK["SNAPSHOT"] =0x2C  #printscreen key
VK["INSERT"] =0x2D
VK["DELETE"] =0x2E
VK["HELP"] =0x2F
#implement the ASCII code for all numbers and all capital letters
for i in list(range(0x30,0x39))+list(range(0x41,0x5A)):
    VK[chr(i)] = i

# https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-input
class DUMMYUNIONNAME(Union):
    _pack_ = sizeof(MOUSEINPUT)
    _fields_ = [("mi",MOUSEINPUT),
                ("ki",KEYBDINPUT)]

class INPUT(Structure):
    _fields_ = [("type", DWORD),#DWORD
                ("dummyunion",DUMMYUNIONNAME)]

INPUT_MOUSE = DWORD(0)
INPUT_KEYBOARD = DWORD(1)

LPINPUT = POINTER(INPUT)

# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendinput
# parameters of sendInput are:
# UINT cInputs = number of structs in pInput,
# LPINPUT pInputs = pointer to array of INPUT structs
# int cbSize = size (in bytes) of an INPUT struct

"""
def moveMouseTo(x,y):
    windll.user32.SendInput(c_uint(1),
                            byref(INPUT(INPUT_MOUSE, makeMI(x,y, ,))),
                            sizeof(INPUT))
"""

#https://stackoverflow.com/questions/4631292/how-detect-current-screen-resolution
#https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getsystemmetrics?redirectedfrom=MSDN
#parameters codes for getting a specific system metric
SM_CMONITORS = 80
SM_CXVIRTUALSCREEN = 78
SM_CYVIRTUALSCREEN = 79

# must normalize x and y if using absolute coordinates
# https://stackoverflow.com/questions/49026921/sendinput-always-moves-mouse-pointer-to-left-top-corner
def normalizePos(dxPos, dyPos):
    print("number of monitors is ",windll.user32.GetSystemMetrics(SM_CMONITORS))
    screenWidth = windll.user32.GetSystemMetrics(SM_CXVIRTUALSCREEN)
    screenHeight = windll.user32.GetSystemMetrics(SM_CYVIRTUALSCREEN)
    print("screen width = %d px, screen height = %d px" % (screenWidth, screenHeight))
    #screen coords go from 0 to 65535 in both directions
    return (round(dxPos*65535/screenWidth), round(dyPos*65535/screenHeight))

def changeMouseState(dxPos, dyPos, absPos, dxScroll, dyScroll, pressLeft, pressRight):
    dwFlags = 0

    if (absPos):
        dwFlags = dwFlags | MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_VIRTUALDESK | MOUSEEVENTF_MOVE
        print("mouse will move to pos (%s, %s)" % (dxPos, dyPos))
        (dxPos,dyPos) = normalizePos(dxPos,dyPos)

    elif((dxPos != 0) or (dyPos != 0)): #if the x or y positions of the mouse changed
        dwFlags = dwFlags | MOUSEEVENTF_MOVE
        print("mouse will change pos by (%s, %s)" % (dxPos,dyPos))

    if(dyScroll != 0):
        dwFlags = dwFlags | MOUSEEVENTF_WHEEL
        print("scrolling vertically by %s" % (dyScroll))

    if(pressLeft):
        if ((windll.user32.GetKeyState(VK["LBUTTON"]) & 0x100) == 0):
            dwFlags = dwFlags | MOUSEEVENTF_LEFTDOWN
            print("pressing left button")
        else:
            print("left button already pressed")
    else:
        if((windll.user32.GetKeyState(VK["LBUTTON"]) & 0x100) != 0):
            dwFlags = dwFlags | MOUSEEVENTF_LEFTUP
            print("releasing left button")
        else:
            print("left button already released")

    if (pressRight):
        if ((windll.user32.GetKeyState(VK["RBUTTON"]) & 0x100) == 0):
            dwFlags = dwFlags | MOUSEEVENTF_RIGHTDOWN
            print("pressing right button")
        else:
            print("right button already pressed")
    else:
        if ((windll.user32.GetKeyState(VK["RBUTTON"]) & 0x100) != 0):
            dwFlags = dwFlags | MOUSEEVENTF_RIGHTUP
            print("releasing right button")
        else:
            print("right button already released")

    mi = MOUSEINPUT(LONG(dxPos),
                    LONG(dyPos),
                    DWORD(dyScroll),
                    DWORD(dwFlags),
                    DWORD(0),# set time to 0 so system assigns its own time
                    ULONG_PTR(LONG(windll.user32.GetMessageExtraInfo())))# get data for dwExtraInfo from calling GetMessageExtraInfo()

    windll.user32.SendInput(UINT(1),
                            LPINPUT(INPUT(INPUT_MOUSE, DUMMYUNIONNAME(mi))),
                            int(sizeof(INPUT)))

    if(dxScroll != 0):
        changeKeyState("shift", True)
        #repeat the input change with dxScroll replacing dyScroll
        mi.mouseData = dxScroll
        windll.user32.SendInput(c_uint(1),
                                LPINPUT(INPUT(INPUT_MOUSE, DUMMYUNIONNAME(mi))),
                                sizeof(INPUT))
        changeKeyState("shift", False)

    print()

weirdVKeyNames = {' ':"SPACE", "ALT":"MENU", "CTRL":"CONTROL", "ENTER":"RETURN"}
def changeKeyState(keyName, pressDown):
    keyName = keyName.upper()

    if(keyName in weirdVKeyNames):
        keyName = weirdVKeyNames[keyName]

    dwFlags = 0
    if(pressDown == 0):
        dwFlags = KEYEVENTF_KEYUP
        print("releasing '%s' key (code = 0x%x)" % (keyName, VK[keyName]))
    else:
        print("pressing '%s' key (code = 0x%x)" % (keyName, VK[keyName]))

    ki = KEYBDINPUT(WORD(VK[keyName]), #virtual key
                    WORD(0), #no scan code (unicode?) specified, virtual key used instead
                    DWORD(dwFlags),
                    DWORD(0),  # set time to 0 so system assigns its own time
                    ULONG_PTR(LONG(windll.user32.GetMessageExtraInfo())))  # get data for dwExtraInfo from calling GetMessageExtraInfo())

    du = DUMMYUNIONNAME()
    du.ki = ki
    windll.user32.SendInput(UINT(1),
                            LPINPUT(INPUT(INPUT_KEYBOARD, du)),
                            int(sizeof(INPUT)))


if __name__ == "__main__":
    x = -100
    y = -50
    changeMouseState(x, y, False, 0, 0, False, False)
    sleep(1)
    changeMouseState(0, 0, True, 0, 0, False, False)
    sleep(1)
    changeMouseState(1280, 720, True, 0, 0, False, False)
    sleep(1)
    x = 100
    y = 50
    changeMouseState(x, y, True, 0, 0, False, False)
    sleep(1)
    changeMouseState(x, y, False, 0, 0, False, False)
    sleep(1)
    changeMouseState(1155, 20, True, 0, 0, True, False)
    sleep(1)
    #changeMouse(640, 360, True, 0, 0, False, False) #drags mouse w right click
    changeMouseState(1155, 20, True, 0, 0, True, False)
    sleep(1)
    changeMouseState(1155, 20, True, 0, 0, True, False)
    sleep(1)
    changeMouseState(1155, 20, True, 0, 0, False, False)
    sleep(1)
    changeMouseState(470, 700, True, 0, 0, True, False)
    changeMouseState(600, 700, True, 0, 0, False, False)
    sleep(1)
    # no delay needed between consecutive clicks to register a left click!
    changeMouseState(470, 700, True, 0, 0, True, False)
    changeMouseState(470, 700, True, 0, 0, False, False)