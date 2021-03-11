import time
import Keyboard
import Mouse

gestures = {
    0 : "Move Mouse",
    1 : "## Press Left (replaced Drag)",
    2 : "## Release Left (replaced Drag)",
    3 : "Double Click",
    4 : "Left Click",
    5 : "Right Click",
    6 : "## Toggle Keyboard Visibility (not a gesture yet)",
}

m = Mouse.Mouse()
kb = Keyboard.Keyboard()

def controlComputer(gestureID, x = None, y = None,):

    if(gestureID == 0):     # move mouse (dynamic)
        m.update(x = x, y = y)

        """
        # just press/release left click when needed (2) and move mouse to replace drag function
        elif(gestureID == 1):   # drag (left click+ hold, dynamic)
            if(hold == False):
                hold == True
                m.update(pressLeft=True)
            else:
    
        """

    elif(gestureID == 1): # press left click
        m.update(pressLeft = True)

    elif(gestureID == 2): # release left click
        m.update(pressLeft = False)

    elif(gestureID == 3):   # double left click (static)
        m.update(pressLeft = True)
        time.sleep(0.01)
        m.update(pressLeft = False)
        time.sleep(0.01)
        m.update(pressLeft = True)
        time.sleep(0.01)
        m.update(pressLeft = False)

    elif(gestureID == 4):   # left click (static)
        m.update(pressLeft = True)
        time.sleep(0.01)
        m.update(pressLeft = False)

    elif(gestureID == 5):   # right click (static)
        m.update(pressRight = True)
        time.sleep(0.01)
        m.update(pressRight = False)

    elif(gestureID == 6): # show/hide keyboard keyboard
        kb.updateKey("CTRL", pressDown = True)
        kb.updateKey("LEFT WINDOWS", pressDown = True)
        kb.updateKey("O", pressDown = True)
        kb.updateKey("O", pressDown=False)
        kb.updateKey("LEFT WINDOWS", pressDown=False)
        kb.updateKey("CTRL", pressDown=False)

    else:
        m.update(pressLeft = False, pressRight = False)
        print("Gesture ID "+str(gestureID)+" not recognized")

if __name__ == "__main__":
    print("Hi")
    controlComputer(6) #show keyboard
    time.sleep(1)
    controlComputer(4) #left click
    time.sleep(1)
    controlComputer(6) #show keyboard
