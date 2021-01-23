#virtual keys: https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
VK = {}

# virtual keys: https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
VK_LBUTTON = 0x01
VK_RBUTTON = 0x02

VK_MOUSE = {}
VK_MOUSE["LBUTTON"] = 0x01
VK_MOUSE["RBUTTON"] = 0x02
VK_MOUSE["MBUTTON"] = 0x04
VK_MOUSE["XBUTTON1"] = 0x05
VK_MOUSE["XBUTTON2"] = 0x06

VK["CANCEL"] =0x03
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
#implement the ASCII code for all numbers and all capital letters https://docs.microsoft.com/en-us/windows/win32/learnwin32/keyboard-input
VK_NUMS = {}
for i in list(range(0x31,0x3A)):
    VK_NUMS[chr(i)] = i;

VK_ALPHABET = {}
for i in list(range(0x41,0x5B)):
    VK_ALPHABET[chr(i)] = i

VK_LWIN = 0x5B #Left Windows key (Natural keyboard)
VK_RWIN = 0x5C #Right Windows key (Natural keyboard)

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
