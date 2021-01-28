from Mouse import Mouse
from Keyboard import Keyboard
from MouseKeyboardInput import changeKeyState
import time

m = Mouse()
kb = Keyboard()
#open google chrome
kb.updateKey("LEFT WINDOWS", pressDown = True)
kb.updateKey("LEFT WINDOWS", pressDown = False)
time.sleep(1)
kb.typeText("google")
time.sleep(0.1)
kb.updateKey("ENTER", True)
kb.updateKey("ENTER", False)
time.sleep(1)
#search for "apples" in the search bar
kb.typeText("apples")
kb.updateKey("ENTER", True)
kb.updateKey("ENTER", False)
time.sleep(2)
#zoom in twice
kb.updateKey("LEFT CTRL", True)
kb.updateKey("+", True)
kb.updateKey("+", False)
kb.updateKey("+", True)
kb.updateKey("+", False)
kb.updateKey("LEFT CTRL", False)
time.sleep(1.5)
#scroll in a square
    #moving scrollbar down or left uses negative scroll numbers
m.update(x = 500, y = 500, dyScroll = -500)
time.sleep(1)
m.update(dxScroll = -500, keyboard = kb)
time.sleep(1)
    #moving scrollbar up or right uses positive scroll numbers
m.update(dyScroll = 500)
time.sleep(1)
m.update(dxScroll = 500, keyboard = kb)
time.sleep(1)
#zoom out twice
kb.updateKey("LEFT CTRL", True)
kb.updateKey("-", True)
kb.updateKey("-", False)
kb.updateKey("-", True)
kb.updateKey("-", False)
kb.updateKey("LEFT CTRL", False)
time.sleep(1)
#close google chrome window
m.update(x = m.getScreenWidth()-10, y = 10, pressLeft = True)
m.update(pressLeft = False)
#move mouse to center of screen (away from any X buttons that close windows)
m.update(x = 600,y = 350)

"""m = Mouse()
m.update() #test if no updates to mouse do nothing (as intended)
m.update(x = 500, y = 500)

changeKeyState("ALT", True);
changeKeyState("TAB", True);
changeKeyState("TAB", False);
changeKeyState("ALT", False);
sleep(1)
changeKeyState("CTRL", True);
changeKeyState("N", True);
changeKeyState("N", False);
changeKeyState("CTRL", False);

for c in "apples":
    changeKeyState(c, True);
    changeKeyState(c, False);
changeKeyState("ENTER", True);
changeKeyState("ENTER", False);

#scroll mouse cursor in a square path
sleep(2)
#moving scrollbar down or left uses negative scroll numbers
m.update(dyScroll = -500)
sleep(1)
changeKeyState("SHIFT", True)
m.update(dxScroll = -500)
changeKeyState("SHIFT", False)
sleep(1)
#moving scrollbar up or right uses positive scroll numbers
m.update(dyScroll = 500)
sleep(1)
changeKeyState("SHIFT", True)
m.update(dxScroll = 500);
changeKeyState("SHIFT", False)

sleep(1)
m.update(x = 1240, y = 10, pressLeft = True)
m.update(pressLeft = False)

sleep(1)
changeKeyState("ALT", True);
changeKeyState("TAB", True);
changeKeyState("TAB", False);
changeKeyState("ALT", False);
m.update(x = 600,y = 350)"""