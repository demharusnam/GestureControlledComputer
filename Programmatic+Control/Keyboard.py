from WINDOWS_API_STRUCTS import UINT, LONG, WORD, DWORD, ULONG_PTR, INPUT_KEYBOARD
from WINDOWS_API_STRUCTS import KEYBDINPUT, DUMMYUNIONNAME, INPUT, LPINPUT, INPUT_BYTES
from WINDOWS_API_STRUCTS import windll
#from WINDOWS_VIRTUAL_KEY_CODES import VK, VK_NUMS, VK_ALPHABET, VK_LWIN, VK_CONTROL
from WINDOWS_VIRTUAL_KEY_CODES import *

# static vars for keycodes, must remain constant
# If specified, key is being released. If not specified, key is being pressed. https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-keybdinput
KEYEVENTF_KEYUP = 0x0002

weirdVKeyNames = {' ':"SPACE", "ALT":"MENU", "CTRL":"CONTROL", "ENTER":"RETURN", "WINDOWS":"LWIN"}

# use a single INPUT struct so its memory can be reused when the mouse is updated multiple times
inputStructPtr = LPINPUT(INPUT(INPUT_KEYBOARD, DUMMYUNIONNAME(KEYBDINPUT())))
dwFlags = 0

class Keyboard:
    def __getVKCode(keyName):
        VK_code = 0x00;  # this keycode it a placeholder, it is not used in Windows for any known virtual keys

        chars = len(keyName)
        if (chars == 1):
            # if keyName btwn 0(0x30) to 9(0x39) or A(0x41) to Z(0x5A), use the number of its ASCII code as the key code
            if ((0x30 <= ord(VK_code) <= 0x39) or (0x41 <= ord(VK_code) <= 0x5A)):
                VK_code = ord(keyName)
            elif(keyName == ';'):
                VK_code = VK_OEM_1
            elif(keyName == '+'):
                VK_code = VK_OEM_PLUS
            elif(keyName == ','):
                VK_code == VK_OEM_COMMA
            elif(keyName == '-'):
                VK_code = VK_OEM_MINUS
            elif(keyName == '.'):
                VK_code = VK_OEM_PERIOD
            elif(keyName == '/'):
                VK_code = VK_OEM_2
            elif(keyName == '`'): #same key that makes a '~' char when shift is pressed
                VK_code = VK_OEM_3
            elif(keyName == '['):
                VK_code = VK_OEM_4
            elif(keyName == '\\'): #first slash indicates that next slash is a char, not a special character
                VK_code = VK_OEM_5
            elif(keyName == ']'):
                VK_code = VK_OEM_6
            elif(keyName == "'"): #single quote/double quote key
                VK_code = VK_OEM_7
            else:
                # look in big list?
                print("Key '", keyName, "' is unrecognized")
                return 0;
        elif(chars == 2):

        elif(chars == 3):
            if(keyName == "ALT"):
                VK_code = VK["MENU"] #ALT
            elif(keyName == "ESC"):
                VK_code = VK["ESCAPE"] #ESC
            elif(keyName == "TAB"):
                VK_code = VK["TAB"] #TAB
        # elif(chars == 4):
        else:
            if (keyName in weirdVKeyNames):
                VK_code = VK[weirdVKeyNames[keyName]]
        #if keyName

        print("VKeyCode of '%s' is %x" % (keyName, VK_code))
        return VK_code;

    def changeKeyState(keyName, pressDown):
        dwFlags = 0

        if()
        if(pressDown == 0):
            dwFlags = KEYEVENTF_KEYUP

        else:
            print("pressing '%s' key (code = 0x%x)" % (keyName, VK[keyName]))

        inputStructPtr.contents.dummyUnion.keyboardInput.wVk = WORD(VK[keyName]) #virtual key
        inputStructPtr.contents.dummyUnion.keyboardInput.wScan = WORD(0), #no scan code (unicode?) specified, virtual key used instead
        inputStructPtr.contents.dummyUnion.keyboardInput.dwFlags = DWORD(dwFlags),
        inputStructPtr.contents.dummyUnion.keyboardInput.time = DWORD(0),  # set time to 0 so system assigns its own time
        inputStructPtr.contents.dummyUnion.keyboardInput.dwExtraInfo = ULONG_PTR(LONG(windll.user32.GetMessageExtraInfo())))  # get data for dwExtraInfo from calling GetMessageExtraInfo())

        windll.user32.SendInput(UINT(1), inputStructPtr, INPUT_BYTES)