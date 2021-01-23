from WINDOWS_API_STRUCTS import UINT, LONG, WORD, DWORD, ULONG_PTR, INPUT_KEYBOARD
from WINDOWS_API_STRUCTS import KEYBDINPUT, DUMMYUNIONNAME, INPUT, LPINPUT, INPUT_BYTES
from WINDOWS_API_STRUCTS import windll
#from WINDOWS_VIRTUAL_KEY_CODES import VK, VK_NUMS, VK_ALPHABET, VK_LWIN, VK_CONTROL
from WINDOWS_VIRTUAL_KEY_CODES import *

# static vars for keycodes, must remain constant
# If specified, key is being released. If not specified, key is being pressed. https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-keybdinput
KEYEVENTF_KEYUP = 0x0002

# use a single INPUT struct so its memory can be reused when the mouse is updated multiple times
inputStructPtr = LPINPUT(INPUT(INPUT_KEYBOARD, DUMMYUNIONNAME(KEYBDINPUT())))
dwFlags = 0
class Keyboard:

    """
        List of Recognized Keynames (120 so far):
            "0" "1" "2" "3" "4" "5" "6" "7" "8" "9"
            "A" "B" "C" "D" "E" "F" "G" "H" "I" "J" "K" "L" "M" "N" "O" "P" "Q" "R" "S" "T" "U" "V" "W" "X" "Y" "Z"
            ";" "+" "," "-" "." "/" "`" "[" "\\" "]" "'"
            "F1" "F2" "F3" "F4" "F5" "F6" "F7" "F8" "F9" "F10" "F11" "F12" "F13" "F14" "F15" "F16" "F17" "F18" "F19" "F20" "F21" "F22" "F23" "F24"
            "ALT" "ADD" "ESC" "TAB" "END"
                "LEFT ALT" "RIGHT ALT"
            "CTRL" "HOME" "HELP" "APPS"
                "LEFT CTRL" "RIGHT CTRL"
                "PAGE UP" "PAGE DOWN"
            "ENTER" "SPACE" "PRINT" "SLEEP" "SCROLL" "CLEAR"
                "UP ARROW" "DOWN ARROW" "LEFT ARROW" "RIGHT ARROW"
            "SELECT" "INSERT" "DELETE" "DIVIDE"
            "NUMPAD0" "NUMPAD1" "NUMPAD2" "NUMPAD3" "NUMPAD4" "NUMPAD5" "NUMPAD6" "NUMPAD7" "NUMPAD8" "NUMPAD9"
                "LEFT WINDOWS" "RIGHT WINDOWS"
            "DECIMAL" "NUMLOCK"
            "MULTIPLY" "SUBTRACT" "CAPSLOCK"
            "BACKSPACE" "SEPARATOR"
            "PRINTSCREEN"

        Discarded Code for Keynames List
        keyNames = []
        #all numbers
        for i in list(range(0,9+1)):
            keyNames.append(str(i))
        #all uppercase letters
        for i in list(range(0x41,0x5A+1)):
            keyNames.append(chr(i))
        #all punctuation
        for p in ";+,-./`[\\]'":
            keyNames.append(p)
        #all F1-F24 keys
        for i in list(range(1,24+1)):
            keyNames.append('F'+chr(i))
        #3 letter key names
        for name in ["ADD","ALT","ESC","TAB"]:
            keyNames.append(name)
    """

    def __getVKCode(keyName):
        VK_code = 0x00;  # this keycode it a placeholder, it is not used in Windows for any known virtual keys

        chars = len(keyName)
        if (chars == 1):
            # implement the ASCII code for all numbers and all capital letters https://docs.microsoft.com/en-us/windows/win32/learnwin32/keyboard-input
            # if keyName btwn 0(0x30) to 9(0x39) or A(0x41) to Z(0x5A), use the number of its ASCII code as the key code
            i = ord(keyName)
            if ((0x30 <= i <= 0x39) or (0x41 <= i <= 0x5A)):
                VK_code = i
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
        elif(chars == 2):
            #do keys F1 to F12 and the Fn key?
            if(keyName[0] == 'F'): #F1 to F24
                n = int(keyName[1])
                if(1 <= n <= 24):
                    VK_code = 0x69+n
        elif(chars == 3):
            #comparing just 1st or 2nd chars may trigger a false match when ignoring the 3rd char
            if(keyName == "ADD"):
                VK_code = VK_ADD #ADD
            elif(keyName[1] == "ALT"):
                VK_code = VK_MENU #ALT
            elif(keyName[0] == "ESC"):
                VK_code = VK_ESCAPE #ESC
            elif(keyName[0] == "TAB"):
                VK_code = VK_TAB #TAB
        elif(chars == 4):
            if(keyName == "CTRL"):
                VK_code = VK_CONTROL

        if(VK_code == 0x00):
            print("keyName '%s' is unrecognized" % (keyName))
        else:
            print("keyName '%s' has VK_code %x" % (keyName, VK_code))

        return VK_code;

    def changeKeyState(keyName, pressDown):
        dwFlags = 0

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