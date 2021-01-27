from WINDOWS_API_STRUCTS import UINT, LONG, WORD, DWORD, ULONG_PTR, INPUT_KEYBOARD
from WINDOWS_API_STRUCTS import KEYBDINPUT, DUMMYUNIONNAME, INPUT, LPINPUT, INPUT_BYTES
from WINDOWS_API_STRUCTS import windll
#from WINDOWS_VIRTUAL_KEY_CODES import VK, VK_NUMS, VK_ALPHABET, VK_LWIN, VK_CONTROL
from WINDOWS_VIRTUAL_KEY_CODES import *

# static vars for keycodes, must remain constant
# If specified, key is being released. If not specified, key is being pressed. https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-keybdinput
KEYEVENTF_KEYUP = 0x0002

# use a single INPUT struct so its memory can be reused when the mouse is updated multiple times
inputStructPtr = LPINPUT(INPUT(INPUT_KEYBOARD, DUMMYUNIONNAME(ki = KEYBDINPUT())))
dwFlags = 0
class Keyboard:

    """
        List of Recognized Keynames (120 so far):
            "0" "1" "2" "3" "4" "5" "6" "7" "8" "9"
            "A" "B" "C" "D" "E" "F" "G" "H" "I" "J" "K" "L" "M" "N" "O" "P" "Q" "R" "S" "T" "U" "V" "W" "X" "Y" "Z"
            ";" "+" "," "-" "." "/" "`" "[" "\\" "]" "'"
            "F1" "F2" "F3" "F4" "F5" "F6" "F7" "F8" "F9"
            "F10" "F11" "F12" "F13" "F14" "F15" "F16" "F17" "F18" "F19" "F20" "F21" "F22" "F23" "F24"
            "ALT" "ADD" "ESC" "TAB" "END"
                "LEFT ALT" "RIGHT ALT"
            "CTRL" "HOME" "HELP" "APPS"
                "CTRL LEFT " "CTRL RIGHT"
                "PAGE UP" "PAGE DOWN"
                "CAPS LOCK"
                "NUM LOCK"
            "ENTER" "SPACE" "PRINT" "SLEEP" "SCROLL" "CLEAR" "SHIFT"
                "UP ARROW" "DOWN ARROW" "LEFT ARROW" "RIGHT ARROW"
            "SELECT" "INSERT" "DELETE" "DIVIDE"
            "DECIMAL"
                "NUMPAD0" "NUMPAD1" "NUMPAD2" "NUMPAD3" "NUMPAD4" "NUMPAD5" "NUMPAD6" "NUMPAD7" "NUMPAD8" "NUMPAD9"
                "LEFT WINDOWS" "RIGHT WINDOWS"

            "MULTIPLY" "SUBTRACT"
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

    def __getVKCode(self,keyString):
        VK_code = 0x00;  # this keycode it a placeholder, it is not used in Windows for any known virtual keys

        #extract the main key name from the last part of keyname from string
        #any modifier words (up, down, left, right) should be separated from the main key name by a spae
        keyParts = [x for x in keyString.split(' ') if(x != '')] #get rid of any blank '' entries
        keyName = keyParts[-1] #main key name

        chars = len(keyName)
        if (chars == 1): #check through all 1 letter key names
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
            elif(keyName == '`'): #same key that makes a '~' char when shift is pressed too
                VK_code = VK_OEM_3
            elif(keyName == '['):
                VK_code = VK_OEM_4
            elif(keyName == '\\'): #first slash indicates that next slash is a char, not a special character
                VK_code = VK_OEM_5
            elif(keyName == ']'):
                VK_code = VK_OEM_6
            elif(keyName == "'"): #single quote/double quote key
                VK_code = VK_OEM_7
        elif(chars == 2): #check through all 2 letter/char key names
            #do keys F1 to F12 and the Fn key?
            if(keyName[0] == 'F'): #F1 to F9
                n = int(keyName[1])
                if(1 <= n <= 9):
                    VK_code = 0x69+n
            elif(keyName == "UP" and keyParts[0] == "PAGE"):
                VK_code = VK_PRIOR  # PAGE UP
        elif(chars == 3): #check through all 3 letter/char key names
            #comparing just 1st or 2nd chars may trigger a false match when ignoring the 3rd char
            if (keyName[0] == 'F'):  # F10 to F24
                n = int(keyName[1:3]) #assume 2nd and 3rd chars of string form number
                if (10 <= n <= 24):
                    VK_code = 0x69 + n
            elif(keyName == "ADD"):
                VK_code = VK_ADD #ADD
            elif(keyName[1] == "ALT"):
                if(len(keyParts) == 1): #check if no modifier part to key name to use default ALT key
                    VK_code = VK_MENU #ALT
                else:
                    keyName = keyParts[0]
                    if(keyName == "LEFT"):
                        VK_code = VK_LMENU #LEFT ALT
                    elif(keyName == "RIGHT"):
                        VK_code = VK_RMENU #RIGHT ALT
            elif(keyName == "ESC"):
                VK_code = VK_ESCAPE #ESC
            elif(keyName == "TAB"):
                VK_code = VK_TAB #TAB
        elif(chars == 4): #check through all 4 letter key names
            if (keyName == "APPS"):
                VK_code = VK_APPS #APPS
            elif(keyName == "CTRL"):
                if(len(keyParts) == 1): #check if no modifier words, means use default CTRL key
                    VK_code = VK_CONTROL #CTRL
                else: #distinguish btwn left CTRL or right CTRL
                    keyName = keyParts[0] # modifier part of key name
                    if(keyName == "LEFT"):
                        VK_code = VK_LCONTROL #LEFT CTRL
                    elif(keyName == "RIGHT"):
                        VK_code = VK_RCONTROL #RIGHT CTRL
            elif (keyName == "DOWN" and keyParts[0] == "PAGE"):
                VK_code == VK_NEXT #PAGE DOWN
            elif(keyName == "HELP"):
                VK_code = VK_HELP #HELP
            elif (keyName == "HOME"):
                VK_code = VK_HOME #HOME
            elif(keyName == "LOCK"):
                keyName = keyParts[0]
                if(keyName == "CAPS"):
                    VK_code = VK_CAPITAL #CAPS LOCK
                elif(keyName == "NUM"):
                    VK_code = VK_NUMLOCK #NUM LOCK
        elif(chars == 5): #check through all 5 letter key names
            if(keyName == "ARROW"):
                keyName = keyParts[0]
                if(keyName == "DOWN"):
                    VK_code = VK_DOWN #DOWN ARROW
                elif(keyName == "LEFT"):
                    VK_code = VK_LEFT #LEFT ARROW
                elif(keyName == "RIGHT"):
                    VK_code = VK_RIGHT #RIGHT ARROW
                elif(keyName == "UP"):
                    VK_code = VK_UP #UP ARROW
            elif(keyName == "CLEAR"):
                VK_code = VK_CLEAR #CLEAR
            elif (keyName == "ENTER"):
                VK_code = VK_RETURN  #ENTER
            elif (keyName == "PRINT"):
                VK_code = VK_PRINT #PRINT
            elif (keyName == "SCROLL"):
                VK_code = VK_SCROLL #SCROLL
            elif (keyName == "SHIFT"):
                if(len(keyParts) == 1): #check if no modifier words, use default SHIFT key
                    VK_code = VK_SHIFT #SHIFT
                else:
                    keyName = keyParts[0] #get modifier part of key
                    if(keyName == "LEFT"):
                        VK_code = VK_LSHIFT #LEFT SHIFT
                    elif(keyName == "RIGHT"):
                        VK_code = VK_RSHIFT #RIGHT SHIFT
            elif (keyName == "SLEEP"):
                VK_code = VK_SLEEP #SLEEP
            elif (keyName == "SPACE"):
                VK_code = VK_SPACE #SPACE
        elif(chars == 6): #check through all 6 letter key names
            if(keyName == "INSERT"):
                VK_code = VK_INSERT #INSERT
            elif(keyName == "DELETE"):
                VK_code = VK_DELETE #DELETE
            elif(keyName == "DIVIDE"):
                VK_code = VK_DIVIDE #DIVIDE
            elif(keyName == "SELECT"):
                VK_code = VK_SELECT #SELECT
        elif(chars == 7): #check through all 7 letter/char key names
            if(keyName == "DECIMAL"):
                VK_code = VK_DECIMAL #DECIMAL
            elif(keyName[0:6] == "NUMPAD"):
                num = int(keyName[6]) #extract number part from NUMPAD name
                VK_code = 0x60 + num
            elif(keyName == "WINDOWS"):
                keyName = keyParts[0]
                if(keyName == "LEFT"):
                    VK_code = VK_LWIN #LEFT WINDOWS
                elif(keyName == "RIGHT"):
                    VK_code = VK_RWIN #RIGHT WINDOWS
        elif(chars == 8): #check through all 8 letter key names
            if(keyName == "MULTIPLY"):
                VK_code = VK_MULTIPLY #MULTIPLY
            elif(keyName == "SUBTRACT"):
                VK_code = VK_SUBTRACT #SUBTRACT
        elif(chars == 9):
            if(keyName == "BACKSPACE"):
                VK_code = VK_BACK #BACKSPACE
            elif(keyName == "SEPARATOR"):
                VK_code = VK_SEPARATOR #SEPARATOR
        elif(chars == 9):
            if(keyName == "PRINTSCREEN"):
                VK_code = VK_SNAPSHOT #PRINTSCREEN

        return VK_code;

    def pressKeyCombo(self,keys):
        #get list of VK codes from names of keys
        numOfKeys = len(keys)
        VK_codes = [self.__getVKCode(keyString) for keyString in keys]

        inputStructPtr.contents.dummyUnion.keyboardInput.wScan = WORD(0) #no scan code (unicode?) specified, virtual key used instead
        inputStructPtr.contents.dummyUnion.keyboardInput.time = DWORD(0)  # set time to 0 so system assigns its own time
        inputStructPtr.contents.dummyUnion.keyboardInput.dwExtraInfo = ULONG_PTR(LONG(windll.user32.GetMessageExtraInfo()))  # get data for dwExtraInfo from calling GetMessageExtraInfo())

        #press keys in list order
        inputStructPtr.contents.dummyUnion.keyboardInput.dwFlags = DWORD(0)  # specify that key is being pressed
        for i in range(0,numOfKeys): #from 0 to len(keys)-1
            if(VK_codes[i] == 0x00):
                print("keyName '%s' is unrecognized. No key pressed" % (keys[i]))
            else:
                print('press')
                print("keyName '%s' has VK_code %x" % (keys[i], VK_codes[i]))
                inputStructPtr.contents.dummyUnion.keyboardInput.wVk = WORD(VK_codes[i])
                windll.user32.SendInput(UINT(1), inputStructPtr, INPUT_BYTES)

        #release keys in reverse list order
        inputStructPtr.contents.dummyUnion.keyboardInput.dwFlags = DWORD(KEYEVENTF_KEYUP)  #specify that key is being released
        for i in range(numOfKeys-1,-1,-1): #from len(keys)-1 to 0
            if(VK_codes[i] != 0x00):
                inputStructPtr.contents.dummyUnion.keyboardInput.wVk = WORD(VK_codes[i])
                windll.user32.SendInput(UINT(1), inputStructPtr, INPUT_BYTES)
        """
        dwFlags = 0

        if(pressDown == 0):
            dwFlags = KEYEVENTF_KEYUP

        else:
            print("pressing '%s' key (code = 0x%x)" % (keyName, VK[keyName]))

        inputStructPtr.contents.dummyUnion.keyboardInput.wVk = WORD(VK[keyName]) #virtual key
        inputStructPtr.contents.dummyUnion.keyboardInput.wScan = WORD(0), #no scan code (unicode?) specified, virtual key used instead
        inputStructPtr.contents.dummyUnion.keyboardInput.dwFlags = DWORD(dwFlags),
        inputStructPtr.contents.dummyUnion.keyboardInput.time = DWORD(0),  # set time to 0 so system assigns its own time
        inputStructPtr.contents.dummyUnion.keyboardInput.dwExtraInfo = ULONG_PTR(LONG(windll.user32.GetMessageExtraInfo()))  # get data for dwExtraInfo from calling GetMessageExtraInfo())

        windll.user32.SendInput(UINT(1), inputStructPtr, INPUT_BYTES)
        """