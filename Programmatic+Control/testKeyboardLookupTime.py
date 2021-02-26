import time
import Keyboard

kb = Keyboard.Keyboard()

#get list of key names
keyStringList = []
indices = [1,2,3,4,5,6,7,8,9,11]
for dict in [kb.keyNames_byLength[i] for i in indices]:
    for (keyName, VK_code) in dict.items():
        #print("VK_code is dict? = "+str(type(VK_code) is dict)+", VK_code is: "+str(VK_code))
        if(type(VK_code) is not int):
            #print("type of VK_code is "+str(type(VK_code)))
            for prefix in VK_code.keys():
                if(prefix == "default"):
                    keyStringList.append(keyName)
                else:
                    keyStringList.append(prefix+" "+keyName)
        else:
            keyStringList.append(keyName)

#adding special case keynames
#alphanumeric (0x30-0x39),(0x41-0x5A)
for i in range(0x30,0x3A):
    keyStringList.append(chr(i))

for i in range(0x41,0x5B):
    keyStringList.append(chr(i))

#F1-F24
for i in range(1,25):
    keyStringList.append("F"+str(i))

#NUMPAD0-NUMPAD9
for i in range(0,10):
    keyStringList.append("NUMPAD"+str(i))

#inputs which shouldn't work (normal key+SHIFT)
keyStringList.append(':')
keyStringList.append('<')
keyStringList.append('>')
keyStringList.append('=')
keyStringList.append('a') #is lowercase version of key with CAPITAL name
keyStringList.append('NUMPAD@') #wrong numpad key
keyStringList.append('NUMPAD') #missing numpad key
keyStringList.append('LOCK LOCK') #wrong prefix (CAPS lOCK/NUM LOCK)
keyStringList.append('LOCK') #missing prefix (CAPS lOCK/NUM LOCK)

"""
for string in keyStringList:
    print(string)
"""

for string in keyStringList:
    print("Testing keyString "+string)
    try:
        VK_code = kb._Keyboard__getVKCode(string)
        print("old returns "+hex(VK_code))
    except:
        print("Error in __getVKCode()*********************************")
    try:
        VK_code = kb._Keyboard__getVKCodeFast(string)
        print("new returns " + hex(VK_code))
    except:
        print("Error in __getVKCodeFast()*****************************")
        pass


ti = time.time()
for i in range(0,500):
    for string in keyStringList:
        VK_code = kb._Keyboard__getVKCode(string)
tf = time.time()
print("normal __getVKCode() over all possible valid inputs = "+str(tf-ti))


ti = time.time()
for i in range(0,500):
    for string in keyStringList:
        VK_code = kb._Keyboard__getVKCodeFast(string)
tf = time.time()
print("__getVKCodeFast() over all possible valid inputs = "+str(tf-ti))