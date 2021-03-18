import time
import Keyboard
import Mouse
from GestureControl import gestures

idToGesture = dict((id, gestureText) for (gestureText, id) in gestures.items())

"""
gestures = {
    0 : "Move Mouse",
    1 : "## Press Left (replaced Drag)",
    2 : "## Release Left (replaced Drag)",
    3 : "Double Click",
    4 : "Left Click",
    5 : "Right Click",
    6 : "## Toggle Keyboard Visibility (not a gesture yet)",
}"""

class FSM:
    def __init__(self, mouse, keyboard):
        self.m = mouse
        self.kb = keyboard
        self.isDrag = False

        self.inputs = [-1,-1,-1,-1,-1]
        self.i = 0

    def controlComputer(self, gestureID, x = None, y = None,):
        """
        #only let gesture ID through if previous 5 ids match
        self.inputs[self.i] = gestureID
        allMatch = True
        for i in inputs:
            if(i != gestureID):
                allMatch = False
                break

        #do not process input if id numbers not stable enough
        if(allMatch == False):
            return
        """

        # account for drag having 2 states, the press and release of left click
        if(gestureID == 4): # press left click for drag
            if(self.isDrag):
                self.m.update(x=x, y=y)
            else:
                self.isDrag = True
                self.m.update(pressLeft = True, x=x, y=y)

        else:
            if(self.isDrag): # release left click from drag
                isDrag = False
                self.m.update(pressLeft = False)

            else:

                if(gestureID == 0):     # move mouse (dynamic)
                    self.m.update(x = x, y = y)

                    """
                    # just press/release left click when needed (2) and move mouse to replace drag function
                    elif(gestureID == 1):   # drag (left click+ hold, dynamic)
                        if(hold == False):
                            hold == True
                            m.update(pressLeft=True)
                        else:
                
                    """

                elif(gestureID == 1):   # left click (static)
                    self.m.update(pressLeft = True)
                    time.sleep(0.01)
                    self.m.update(pressLeft = False)

                elif (gestureID == 2):  # double left click (static)
                    self.m.update(pressLeft=True)
                    time.sleep(0.01)
                    self.m.update(pressLeft=False)
                    time.sleep(0.01)
                    self.m.update(pressLeft=True)
                    time.sleep(0.01)
                    self.m.update(pressLeft=False)

                elif (gestureID == 3):  # right click (static)
                    self.m.update(pressRight=True)
                    time.sleep(0.01)
                    self.m.update(pressRight=False)

                elif(gestureID == 5): # show/hide keyboard keyboard
                    self.kb.updateKey("CTRL", pressDown = True)
                    self.kb.updateKey("LEFT WINDOWS", pressDown = True)
                    self.kb.updateKey("O", pressDown = True)
                    self.kb.updateKey("O", pressDown=False)
                    self.kb.updateKey("LEFT WINDOWS", pressDown=False)
                    self.kb.updateKey("CTRL", pressDown=False)

                else:
                    self.m.update(pressLeft = False, pressRight = False)
                    print("Gesture ID "+str(gestureID)+" not recognized")

if __name__ == "__main__":
    print("Hi")
    m = Mouse.Mouse()
    kb = Keyboard.Keyboard()
    fsm = FSM(m,kb)
    fsm.controlComputer(5) #show keyboard
    time.sleep(1)
    fsm.controlComputer(1) #left click
    time.sleep(1)
    fsm.controlComputer(5) #hide keyboard
    time.sleep(1)
    fsm.controlComputer(4,0,0)
    time.sleep(1)
    fsm.controlComputer(4, 100, 100)
    time.sleep(1)
    fsm.controlComputer(0, 200, 200)
