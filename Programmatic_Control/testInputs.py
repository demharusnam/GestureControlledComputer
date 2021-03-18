from Mouse import Mouse
from Keyboard import Keyboard
from MouseKeyboardInput import changeKeyState
import time

m = Mouse()
kb = Keyboard()
#open google chrome
kb.updateKey("LEFT WINDOWS", pressDown = True)
kb.updateKey("LEFT WINDOWS", pressDown = False)
time.sleep(1) #wait for Windows menu to appear
kb.typeText("google")
time.sleep(1) #apparently hitting enter without waiting does not register right?
kb.updateKey("ENTER", True)
kb.updateKey("ENTER", False)
time.sleep(4)
#search for "apples" in the search bar
kb.typeText("apple")
time.sleep(1)
kb.updateKey("ENTER", True)
kb.updateKey("ENTER", False)
time.sleep(3)
#zoom in
kb.updateKey("LEFT CTRL", True)
kb.updateKey("+", True)
kb.updateKey("+", False)
kb.updateKey("+", True)
kb.updateKey("+", False)
kb.updateKey("LEFT CTRL", False)
time.sleep(2)
#move mouse away from edges of window
m.update(x = 500, y = 500)
#scroll in a square
    #moving scrollbar down or left uses negative scroll numbers
m.update(dyScroll = -500)
time.sleep(1)
m.update(dxScroll = -500, keyboard = kb)
time.sleep(1)
    #moving scrollbar up or right uses positive scroll numbers
m.update(dyScroll = 500)
time.sleep(1)
m.update(dxScroll = 500, keyboard = kb)
time.sleep(1)
#zoom out
kb.updateKey("LEFT CTRL", True)
kb.updateKey("-", True)
kb.updateKey("-", False)
kb.updateKey("-", True)
kb.updateKey("-", False)
kb.updateKey("LEFT CTRL", False)
time.sleep(1)

#hit tab until first link is selected
for i in range(0,18):
    kb.updateKey("TAB", True)
    kb.updateKey("TAB", False)
time.sleep(1)
kb.updateKey("ENTER", True)
kb.updateKey("ENTER", False)
time.sleep(5) #wait for website to load
#highlight text
m.update(x = 330, y = 135, pressLeft = True)
m.update(x = 930, y = 135, pressLeft = False)
#copy highlighted text
kb.updateKey("CTRL",True)
kb.updateKey("C", True)
kb.updateKey("C",False)
kb.updateKey("CTRL", False)
time.sleep(1)
#open new tab
kb.updateKey("CTRL",True)
kb.updateKey("T", True)
kb.updateKey("T",False)
kb.updateKey("CTRL", False)
time.sleep(2)
#paste in copied text
kb.updateKey("CTRL",True)
kb.updateKey("V", True)
kb.updateKey("V",False)
kb.updateKey("CTRL", False)
kb.updateKey("ENTER", True)
kb.updateKey("ENTER", False)
time.sleep(2)
m.update(x = 370, y = 285, pressLeft = True)
m.update(pressLeft = False)
time.sleep(2)
#right click to bring up menu
m.update(pressRight = True)
m.update(pressRight = False)
time.sleep(1)
#press "View page source" button
m.update(x = 390, y = 521, pressLeft = True)
m.update(pressLeft = False)
time.sleep(5)
#close google chrome window
m.update(x = m.getScreenWidth()-10, y = 10, pressLeft = True)
m.update(pressLeft = False)
#move mouse to center of screen (away from any X buttons that close windows)
m.update(x = 600,y = 350)