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

# https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-keybdinput
class KEYBDINPUT(Structure):
    _fields_ = [("wVk", WORD), #WORD
                ("wScan", WORD), #WORD
                ("dwFlags", DWORD), #DWORD
                ("time", DWORD), #DWORD
                ("dwExtraInfo", ULONG_PTR)] #ULONG_PTR

# https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-input
class DUMMYUNIONNAME(Union):
    _pack_ = sizeof(MOUSEINPUT)
    _fields_ = [("mouseInput",MOUSEINPUT),
                ("keyboardInput",KEYBDINPUT)]

class INPUT(Structure):
    _fields_ = [("type", DWORD),#DWORD
                ("dummyUnion",DUMMYUNIONNAME)]

INPUT_MOUSE = DWORD(0)
INPUT_KEYBOARD = DWORD(1)

LPINPUT = POINTER(INPUT)