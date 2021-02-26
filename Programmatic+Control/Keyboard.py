from WINDOWS_API_STRUCTS import UINT, LONG, WORD, DWORD, ULONG_PTR, INPUT_KEYBOARD
from WINDOWS_API_STRUCTS import KEYBDINPUT, DUMMYUNIONNAME, INPUT, LPINPUT, INPUT_BYTES
from WINDOWS_API_STRUCTS import windll
# from WINDOWS_VIRTUAL_KEY_CODES import VK, VK_NUMS, VK_ALPHABET, VK_LWIN, VK_CONTROL
from WINDOWS_VIRTUAL_KEY_CODES import *
import time

# static vars for keycodes, must remain constant
# If specified, key is being released. If not specified, key is being pressed. https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-keybdinput
KEYEVENTF_KEYUP = 0x0002  # for releasing a key
KEYEVENTF_UNICODE = 0x0004  # specifies unicode char in wScan and wVk will be ignored

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
        VK_code = 0x00  # this keycode it a placeholder, it is not used in Windows for any known virtual keys

        #extract the main key name from the last part of keyname from string
        #any modifier words (up, down, left, right) should be separated from the main key name by a spae
        keyParts = [x for x in keyString.split(' ') if(x != '')] #get rid of any blank '' entries
        keyName = keyParts[-1] #main key name

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
                VK_code = VK_OEM_COMMA
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
            elif(keyName == "ALT"):
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
                VK_code = VK_NEXT #PAGE DOWN
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
            elif (keyName == "SCROLL"):
                VK_code = VK_SCROLL #SCROLL
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
        elif(chars == 11):
            if(keyName == "PRINTSCREEN"):
                VK_code = VK_SNAPSHOT #PRINTSCREEN

        return VK_code

    keyNames_len1 = {
        ';' : VK_OEM_1,
        '+' : VK_OEM_PLUS,
        ',' : VK_OEM_COMMA,
        '-' : VK_OEM_MINUS,
        '.' : VK_OEM_PERIOD,
        '/' : VK_OEM_2,
        '`' : VK_OEM_3,  # same key that makes a '~' char when shift is pressed too
        '[' : VK_OEM_4,
        '\\' : VK_OEM_5, # first slash indicates that next slash is a char, not a special character
        ']' : VK_OEM_6,
        "'" :VK_OEM_7  # single quote/double quote key
    }

    keyNames_len2 = {
        "UP" : {"PAGE" : VK_PRIOR}  # PAGE UP
    }

    keyNames_len3 = {
        "ADD" : VK_ADD, # ADD
        "ALT" : {
                    "default" : VK_MENU,  # ALT
                    "LEFT" : VK_LMENU,  # LEFT ALT
                    "RIGHT" : VK_RMENU,  # RIGHT ALT
                },
        "ESC" : VK_ESCAPE,  # ESC
        "TAB" : VK_TAB  # TAB
    }

    keyNames_len4 = {
        "APPS" : VK_APPS,  # APPS
        "CTRL" : {
                    "default" : VK_CONTROL,  # CTRL
                    "LEFT" : VK_LCONTROL,  # LEFT CTRL
                    "RIGHT" : VK_RCONTROL  # RIGHT CTRL
                 },
        "DOWN" : {"PAGE" : VK_NEXT},  # PAGE DOWN
        "HELP" : VK_HELP,  # HELP
        "HOME" : VK_HOME,  # HOME
        "LOCK" : {
                    "CAPS" : VK_CAPITAL,  # CAPS LOCK
                    "NUM" : VK_NUMLOCK  # NUM LOCK
                 }
    }

    keyNames_len5 = {
        "ARROW" : {
                    "DOWN" : VK_DOWN,  # DOWN ARROW
                    "LEFT" : VK_LEFT,  # LEFT ARROW
                    "RIGHT": VK_RIGHT,  # RIGHT ARROW
                    "UP" : VK_UP  # UP ARROW
                  },
        "CLEAR" : VK_CLEAR,  # CLEAR
        "ENTER" : VK_RETURN,  # ENTER
        "PRINT" : VK_PRINT,  # PRINT
        "SHIFT" : {
                    "default" : VK_SHIFT,  # SHIFT
                    "LEFT" : VK_LSHIFT,  # LEFT SHIFT
                    "RIGHT" : VK_RSHIFT  # RIGHT SHIFT
                  },
        "SLEEP" : VK_SLEEP,  # SLEEP
        "SPACE" : VK_SPACE  # SPACE
    }

    keyNames_len6 = {
        "INSERT" : VK_INSERT,  # INSERT
        "DELETE" : VK_DELETE,  # DELETE
        "DIVIDE" : VK_DIVIDE,  # DIVIDE
        "SCROLL": VK_SCROLL,  # SCROLL
        "SELECT" : VK_SELECT  # SELECT
    }

    keyNames_len7 = {
        "DECIMAL" : VK_DECIMAL, #DECIMAL
        "WINDOWS" : {
                        "LEFT" : VK_LWIN, #LEFT WINDOWS
                        "RIGHT" : VK_RWIN #RIGHT WINDOWS
                    }
    }

    keyNames_len8 = {
        "MULTIPLY" : VK_MULTIPLY, #MULTIPLY
        "SUBTRACT" : VK_SUBTRACT #SUBTRACT
    }

    keyNames_len9 = {
        "BACKSPACE" : VK_BACK,  # BACKSPACE
        "SEPARATOR" : VK_SEPARATOR  # SEPARATOR
    }

    keyNames_len11 = {
        "PRINTSCREEN" : VK_SNAPSHOT  # PRINTSCREEN
    }

    keyNames_byLength = [
        None, #put nothing in 0 index, sine no key names can have a length of 0
        keyNames_len1,
        keyNames_len2,
        keyNames_len3,
        keyNames_len4,
        keyNames_len5,
        keyNames_len6,
        keyNames_len7,
        keyNames_len8,
        keyNames_len9,
        None,
        keyNames_len11
    ]

    def __getVKCodeFast(self,keyString):
        VK_code = 0x00  # this keycode it a placeholder, it is not used in Windows for any known virtual keys

        #extract the main key name from the last part of keyname from string
        #any modifier words (up, down, left, right) should be separated from the main key name by a spae
        keyParts = [x for x in keyString.split(' ') if(x != '')] #get rid of any blank '' entries
        keyName = keyParts[-1] #main key name
        if(len(keyParts) > 1):
            prefix = keyParts[0]
        else:
            prefix = None
        keyNames_dict = None

        chars = len(keyName)
        if (chars == 1): #check through all 1 letter key name special cases
            # implement the ASCII code for all numbers and all capital letters https://docs.microsoft.com/en-us/windows/win32/learnwin32/keyboard-input
            # if keyName btwn 0(0x30) to 9(0x39) or A(0x41) to Z(0x5A), use the number of its ASCII code as the key code
            i = ord(keyName)
            if ((0x30 <= i <= 0x39) or (0x41 <= i <= 0x5A)):
                VK_code = i

        elif(chars == 2): #check through all 2 letter/char key name special cases
            #do keys F1 to F12 and the Fn key?
            if(keyName[0] == 'F'): #F1 to F9
                n = int(keyName[1])
                if(1 <= n <= 9):
                    VK_code = 0x69+n

        elif(chars == 3): #check through all 3 letter/char key name special cases
            #comparing just 1st or 2nd chars may trigger a false match when ignoring the 3rd char
            if (keyName[0] == 'F'):  # F10 to F24
                n = int(keyName[1:3]) #assume 2nd and 3rd chars of string form number
                if (10 <= n <= 24):
                    VK_code = 0x69 + n

        elif(chars == 7): #check through all 7 letter/char key name special cases
            if (keyName[0:6] == "NUMPAD"):
                num = int(keyName[6])  # extract number part from NUMPAD name
                if(0<= num <= 9):
                    VK_code = 0x60 + num

        #check if no special cases for key code occured, retrieve dict based on # of chars in keyName
        if(VK_code == 0x00 and ((1 <= chars <= 9) or (chars == 11))):
            keyNames_dict = self.keyNames_byLength[chars]
        else:
            print("Special case found for keyName "+keyName)

        #search keyName dict if any dict was selected based on # of chars in keyName
        if(keyNames_dict != None):
            VK_code = self.keyNames_dict[keyName]
            if (type(VK_code) is dict):  # checks if dict entry is another dict
                if (prefix != None): #if dict entry is another dict, but no second part of key name, use default value
                    VK_code = VK_code["default"]
                else: #otherwise search other dict with preceding part of key name
                    VK_code = VK_code[prefix]
            else:
                print("VK_code "+str(VK_code)+" has type "+str(type(VK_code)))
            print("Dict with chars of length "+str(chars)+" found")

        return VK_code

    def isKeyPressed(self, keyString):
        VK_code = self.__getVKCode(keyString)
        if(VK_code == 0x00):
            print("keyString '%s' is unrecognized" % (keyString))
        else:
            #complies with https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getkeystate
            #test if high order bit (left most bit) is a 1
            #if so, key is down aka pressed down
            return bool(windll.user32.GetKeyState(VK_code) & 0x8000)

    def updateKey(self,keyString, pressDown):
        #get VK code from names of keys
        VK_code = self.__getVKCode(keyString)

        if(VK_code == 0x00):
            print("keyString '%s' is unrecognized. No key is pressed" % (keyString))
            return #exit function here so OS does not try to interpret 0x00 as a key (it isn't a key)
        else:
            #add relevant info to struct for OS to read
            inputStructPtr.contents.dummyUnion.keyboardInput.wVk = WORD(VK_code) #Virtual Key code of desired key
            inputStructPtr.contents.dummyUnion.keyboardInput.wScan = WORD(0) #no scan code (unicode?) specified, virtual key used instead

            if(pressDown == True):
                #specify that key is being pressed
                inputStructPtr.contents.dummyUnion.keyboardInput.dwFlags = DWORD(0)
            else:
                #specifiy that key is being released
                inputStructPtr.contents.dummyUnion.keyboardInput.dwFlags = DWORD(KEYEVENTF_KEYUP)

            inputStructPtr.contents.dummyUnion.keyboardInput.time = DWORD(0)  # set time to 0 so system assigns its own time
            inputStructPtr.contents.dummyUnion.keyboardInput.dwExtraInfo = ULONG_PTR(LONG(windll.user32.GetMessageExtraInfo()))  # get data for dwExtraInfo from calling GetMessageExtraInfo())

            windll.user32.SendInput(UINT(1), inputStructPtr, INPUT_BYTES)
            print("keyString '%s' has VK_code %x, key is pressed" % (keyString, VK_code))

    def typeText(self,text):
        inputStructPtr.contents.dummyUnion.keyboardInput.wVk = WORD(0)
        inputStructPtr.contents.dummyUnion.keyboardInput.dwFlags = KEYEVENTF_UNICODE #specify that info has unicode char
        inputStructPtr.contents.dummyUnion.keyboardInput.time = DWORD(0) #set time to 0 so system assigns its own time
        inputStructPtr.contents.dummyUnion.keyboardInput.dwExtraInfo = ULONG_PTR(LONG(windll.user32.GetMessageExtraInfo())) # get data for dwExtraInfo from calling GetMessageExtraInfo())

        for char in text:
            print("typing char '%c' = %x" %(char, ord(char)))
            inputStructPtr.contents.dummyUnion.keyboardInput.wScan = WORD(ord(char))# unicode char to be typed
            windll.user32.SendInput(UINT(1), inputStructPtr, INPUT_BYTES) #ask OS to type unicode char for you
            time.sleep(0.05)

    """
    Will use On Screen Keyboard instead of Touch keyboard because:
    
        1. Not all computers have a touch screen and therefore may be missing a Touch keyboard feature.
        
        2. Also the Touch keyboard has no keyboard shortcut and can't be enabled using the windows API directly, it needs a few mouse clicks on the taskbar
            https://superuser.com/questions/1186075/shortcut-to-open-windows-10-on-screen-keyboard-not-osk-exe
            https://support.microsoft.com/en-us/windows/open-the-touch-keyboard-a1084c2e-bb51-4a95-41cd-1457f8bd7d10
            https://stackoverflow.com/questions/39618127/programmatically-open-on-screen-keyboard-in-uwp
        
        3. The Touch Keyboard will resize the PyCharm IDE window to fill the top half of the screen, but the On Screen Keyboard won't
            Turns out the Touch Keyboard does not play nice with apps that weren't designed to handle touch screen inputs
        
    Note: Both the On Screen Keyboard and the Touch Keyboard have predictive text suggestions
    
    On-Screen Keyboard Enable Settings:
    https://support.microsoft.com/en-us/windows/use-the-on-screen-keyboard-osk-to-type-ecbb5e08-5b4e-d8c8-f794-81dbf896267a
    
    Keyboard Preference parameter in Windows API Does the opposite of enabling an On Screen Keyboard:
    https://docs.microsoft.com/en-us/windows/win32/winauto/keyboard-preference-parameter
    
    IMPORTANT NOTE: Turns Out the On-Screen Keyboard does not need to be enabled, only the Touch Keyboard does
    """
    #def enableOnScreenKeyboard(visible):
    #    return

    """
    The On Screen Keyboard MUST BE ENABLED before you can toggle it with the shortcut in this function
    
    Shortcut Info:
    https://www.tenforums.com/tutorials/115495-turn-off-screen-keyboard-windows-10-a.html
    """
    def toggleOnScreenKeyboard(self):
        # Windows key (L/R) + CTRL key (any) + letter O key
        self.updateKey("CTRL", True)
        self.updateKey("RIGHT WINDOWS", True)
        self.updateKey("O", True)
        self.updateKey("O", False)
        self.updateKey("RIGHT WINDOWS", False)
        self.updateKey("CTRL", False)