import WINDOWS_API_STRUCTS

KEYEVENTF_KEYUP = 0x0002

#virtual keys: https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
VK = {}
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