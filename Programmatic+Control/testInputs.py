from Mouse import updateMouse
from MouseKeyboardInput import changeKeyState
from time import sleep

updateMouse() #test if no updates to mouse do nothing (as intended)
updateMouse(x = 500, y = 500)

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
updateMouse(dyScroll = -500)
sleep(1)
changeKeyState("SHIFT", True)
updateMouse(dxScroll = -500)
changeKeyState("SHIFT", False)
sleep(1)
#moving scrollbar up or right uses positive scroll numbers
updateMouse(dyScroll = 500)
sleep(1)
changeKeyState("SHIFT", True)
updateMouse(dxScroll = 500);
changeKeyState("SHIFT", False)

sleep(1)
updateMouse(x = 1240, y = 10, pressLeft = True)
updateMouse(pressLeft = False)
