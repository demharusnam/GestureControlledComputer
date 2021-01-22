from Mouse import Mouse
from MouseKeyboardInput import changeKeyState
from time import sleep

m = Mouse()
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