import time
import Keyboard

kb = Keyboard.Keyboard()

#get list of key names
keyStringList = []
for dict in kb.keyNames_byLength[1:10+1]:
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

"""
for string in keyStringList:
    print(string)
"""

ti = time.time()
for string in keyStringList:
    try:
        VK_code = kb._Keyboard__getVKCode(string)
        print(string+" = "+str(VK_code))
    except:
        print("Error in VKCode()")
        break
tf = time.time()
print("normal __getVKCode() over all possible valid inputs = "+str(tf-ti))


ti = time.time()
for string in keyStringList:
    try:
        VK_code = kb._Keyboard__getVKCodeFast(string)
        print(string + " = " + str(VK_code))
    except:
        print("Error in VKCodeFast()")
        break
tf = time.time()
print("__getVKCodeFast() over all possible valid inputs = "+str(tf-ti))