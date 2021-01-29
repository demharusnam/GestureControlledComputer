import ctypes
#no need to load windows 32 DLL files since ctypes has it as a module

#NOTE: Always pass structs or unions to API functions by pointer

#data types: https://docs.microsoft.com/en-us/windows/win32/winprog/windows-data-types
UINT = ctypes.c_uint32
int = ctypes.c_int32
LONG = ctypes.c_int32 #LONG = 32 bit signed int = c_int32 = c_int
ULONG_PTR = ctypes.POINTER(ctypes.c_uint32) #ULONG_PTR = unsigned LONG_PTR = unsigned long pointer = 32 bit unsigned int ptr = c_uint32 ptr = c_uint ptr
DWORD = ctypes.c_uint32 #DWORD = 32 bit unsigned int = c_uint32 = c_uint
WORD = ctypes.c_uint16 #WORD = 16 bit unsigned int = c_uint16

# https://docs.microsoft.com/en-us/windows/win32/winprog/windows-data-types
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", LONG), #LONG
                ("dy", LONG), #LONG
                ("mouseData", DWORD), #DWORD
                ("dwFlags", DWORD), #DWORD
                ("time", DWORD), #DWORD for timestamp, put as 0 so system provides its own timestamp
                ("dwExtraInfo", ULONG_PTR)] #ULONG_PTR

# https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-keybdinput
class KEYBDINPUT(ctypes.Structure):
    _fields_ = [("wVk", WORD), #WORD
                ("wScan", WORD), #WORD
                ("dwFlags", DWORD), #DWORD
                ("time", DWORD), #DWORD
                ("dwExtraInfo", ULONG_PTR)] #ULONG_PTR

# https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-input
class DUMMYUNIONNAME(ctypes.Union):
    _pack_ = ctypes.sizeof(MOUSEINPUT)
    _fields_ = [("mouseInput",MOUSEINPUT),
                ("keyboardInput",KEYBDINPUT)]

class INPUT(ctypes.Structure):
    _fields_ = [("type", DWORD),#DWORD
                ("dummyUnion",DUMMYUNIONNAME)]

INPUT_MOUSE = DWORD(0)
INPUT_KEYBOARD = DWORD(1)

LPINPUT = ctypes.POINTER(INPUT)

INPUT_STRUCT_BYTES = int(ctypes.sizeof(INPUT))

#define pointer to array of INPUT structs
ARRAY_SIZE = 50
INPUT_ARRAY = INPUT * ARRAY_SIZE
PTR_INPUT_ARRAY = ctypes.POINTER(INPUT_ARRAY)