#virtual keys: https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes

#mouse specific buttons
VK_LBUTTON = 0x01
VK_RBUTTON = 0x02
VK_MBUTTON = 0x04
VK_XBUTTON1 = 0x05
VK_XBUTTON2 = 0x06

#keyboard buttons
VK_CANCEL_ = 0x03 # I don't know what button does "control-break processing", but it has this code
#0x07 is undefined
VK_BACK = 0X08          #BACKSPACE key
VK_TAB = 0x09           #TAB key
#0x0A and 0x0B are reserved
VK_CLEAR = 0x0C         #CLEAR key (I haven't seen this key before so I don't know where it is on a keyboard)
VK_RETURN = 0x0D        #ENTER key
VK_SHIFT = 0x10         #SHIFT key
VK_CONTROL = 0x11       #CTRL key
VK_MENU = 0x12          #ALT key
VK_PAUSE = 0x13         #PAUSE key
VK_CAPITAL = 0x14       #CAPS LOCK key
"""0x15 to 0x1A deals with IME modes (for languages other than English on a keyboard?)"""
VK_ESCAPE = 0x1B        #ESC key
"""0x1C to 0x1F deals with IME modes (for languages other than English on a keyboard?)"""
VK_SPACE = 0x20         #SPACEBAR
VK_PRIOR = 0x21         #PAGE UP key
VK_NEXT = 0x22          #PAGE DOWN key
VK_END = 0x23           #END key
VK_HOME = 0x24          #HOME key
VK_LEFT = 0x25          #LEFT ARROW key
VK_UP = 0x26            #UP ARROW key
VK_RIGHT = 0x27         #RIGHT ARROW key
VK_DOWN = 0x28          #DOWN ARROW key
VK_SELECT = 0x29        #SELECT key
VK_PRINT = 0x2A         #PRINT key
VK_EXECUTE = 0x2B       #don't know what key this is?
VK_SNAPSHOT = 0x2C      #PRINTSCREEN key
VK_INSERT = 0x2D        #INSERT key (aka INS)
VK_DELETE = 0x2E        #DELETE key (aka DEL)
VK_HELP = 0x2F          #HELP key
""" skip the ASCII codes for all numbers and all capital letters https://docs.microsoft.com/en-us/windows/win32/learnwin32/keyboard-input
    including codes for 0 (0x30) to 9 (0x39)
    0x3A to 0x40 are undefined
    including codes for A (0x41) to Z (0x5A)"""
VK_LWIN = 0x5B          #Left Windows key (Natural keyboard)
VK_RWIN = 0x5C          #Right Windows key (Natural keyboard)
VK_APPS = 0x5D          #Applications key (Natural keyboard)
#0x5E is reserved
VK_SLEEP = 0x5F         #Computer Sleep key

#NUMPAD keys
VK_NUMPAD0 = 0x60       #Numeric keypad 0 key
VK_NUMPAD1 = 0x61       #Numeric keypad 1 key
VK_NUMPAD2 = 0x62       #Numeric keypad 2 key
VK_NUMPAD3 = 0x63       #Numeric keypad 3 key
VK_NUMPAD4 = 0x64       #Numeric keypad 4 key
VK_NUMPAD5 = 0x65       #Numeric keypad 5 key
VK_NUMPAD6 = 0x66       #Numeric keypad 6 key
VK_NUMPAD7 = 0x67       #Numeric keypad 7 key
VK_NUMPAD8 = 0x68       #Numeric keypad 8 key
VK_NUMPAD9 = 0x69       #Numeric keypad 9 key
VK_MULTIPLY = 0x6A      #Multiply (*) key (not the same key as SHIFT+8)
VK_ADD = 0x6B           #Add (+) key (not the same key as the '+' key next to BACKSPACE)
VK_SEPARATOR = 0x6C     #Separator key (unknown to me?)
VK_SUBTRACT = 0x6D      #Subtract (-) key (not the same as '-' key near BACKSPACE)
VK_DECIMAL = 0x6E       #Decimal (.) key
VK_DIVIDE = 0x6F        #Divide (/) key (not the same as forward slash next to RIGHT SHIFT)

""" F keys (0x70 to 0x87)
    Note: VK_FN = 0x69 + N
VK_F1 = 0x70            #F1 key
VK_F2 = 0x71            #F2 key
VK_F3 = 0x72            #F3 key
VK_F4 = 0x73            #F4 key
VK_F5 = 0x74            #F5 key
VK_F6 = 0x75            #F6 key
VK_F7 = 0x76            #F7 key
VK_F8 = 0x77            #F8 key
VK_F9 = 0x78            #F9 key
VK_F10 = 0x79           #F10 key
VK_F11 = 0x7A           #F11 key
VK_F12 = 0x7B           #F12 key
VK_F13 = 0x7C           #F13 key
VK_F14 = 0x7D           #F14 key
VK_F15 = 0x7E           #F15 key
VK_F16 = 0x7F           #F16 key
VK_F17 = 0x80           #F17 key"""

#0x88 to 0x8F are unassigned
VK_NUMLOCK = 0x90       #NUM LOCK key
VK_SCROLL = 0x91        #SCROLL LOCK key
#0x92 to 0x96 are OEM specific
#0x97 to 0x9F are unassigned
VK_LSHIFT = 0xA0        #Left SHIFT key
VK_RSHIFT = 0XA1        #Right SHIFT key
VK_LCONTROL = 0xA2      #Left CONTROL key
VK_RCONTROL = 0xA3      #Right CONTROL key
VK_LMENU = 0xA4         #Left ALT key (aka Left MENU keu)
VK_RMENU = 0xA5         #Right ALT key (aka Right MENU key)
"""0xA6 to 0xAC are keys for Browser specific functions:
    back, forward, refresh, stop, search, favorites, home, mute
   They may be implemented later if needed"""
"""0xAD to 0xAF are keys for Volume specific functions:
    mute, down, up
   They may be implemented later if needed"""
"""0xB0 to 0xB3 are keys for Media specific functions:
    next track, prev track, stop, play/pause, 
   They may be implemented later if needed"""
"""0xB4 to 0xB7 are keys for launching specific applications:
    mail, media select, app1, app2
   They may be implemented later if needed"""
#0xB8 and 0xB9 are reserved
VK_OEM_1 = 0xBA         #For any country/region, the ';:' key
VK_OEM_PLUS = 0xBB      #For any country/region, the '+' key
VK_OEM_COMMA = 0xBC     #For any country/region, the ',' key
VK_OEM_MINUS = 0xBD     #For any country/region, the '-' key
VK_OEM_PERIOD = 0xBE    #For any country/region, the '.' key
VK_OEM_2 = 0xBF         #For the US standard keyboard, the '/?' key
VK_OEM_3 = 0xC0         #For the US standard keyboard, the '~' key
#0xC1-0xD7 are reserved
#0xD8-0xDA are unassigned
VK_OEM_4 = 0xDB         #For the US standard keyboard, the '[{' key
VK_OEM_5 = 0xDC         #For the US standard keyboard, the '\|' key
VK_OEM_6 = 0xDD         #For the US standard keyboard, the '}]' key
VK_OEM_7 = 0xDE         #For the US standard keyboard, the single quote/double quote key
VK_OEM_8 = 0xDF         #Used for miscellaneous characters; it can vary by keyboard
#0xE0 is reserved
#0xE1 is OEM specific
#0xE2 is either the angle bracket key or the backslash key on the RT 102-key keyboard
#0xE3 and 0xE4 are OEM specific
"""0xE5 is the IME PROCESS key"""
#0xE6 is OEM specific
VK_PACKET = 0xE7        #Used to pass Unicode characters as if they were keystrokes. The VK_PACKET key is the low word of a 32-bit Virtual Key value used for non-keyboard input methods.
#0xE8 is unassigned
#0xE9 to 0xF5 is OEM specific
"""
"""