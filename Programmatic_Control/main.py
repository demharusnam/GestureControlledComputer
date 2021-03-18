from time import sleep

from MouseKeyboardInput import changeMouseState, changeKeyState

#switch to browser
changeKeyState("ALT", True)
changeKeyState("TAB", True)
changeKeyState("TAB", False)
changeKeyState("ALT", False)
sleep(1)

#open tab in browser
changeKeyState("CTRL", True)
changeKeyState("N",True)
changeKeyState("N",False)
changeKeyState("CTRL", False)
sleep(1)

#type search query
for c in "windows api":
    print(c)
    changeKeyState(c, True)
    changeKeyState(c, False)

#press enter on search bar
changeKeyState("Enter", True)
changeKeyState("Enter", False)
sleep(1)

#click first link
changeMouseState(200, 280, True, 0, 0, True, False)
changeMouseState(200, 280, True, 0, 0, False, False)
sleep(1)

#scroll
changeMouseState(200, 280, True, 0, -500, False, False)
sleep(1)

#close new tab
changeMouseState(230, 15, True, 0, 0, True, False)
changeMouseState(230, 15, True, 0, 0, False, False)