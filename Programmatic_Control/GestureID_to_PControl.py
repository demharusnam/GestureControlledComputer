import time

#from Gesture_Control.GestureControl import gestures      # <- Mansur's Gesture Recognition Code
from Gesture_Control.ToniGestureControl import gestures # <- Toni's Gesture Recognition Code
idToGesture = dict((id, gestureText) for (gestureText, id) in gestures.items())
idToGesture[-1] = "None"

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
    def __init__(self, mouse = None, keyboard = None):
        if(mouse == None):
            from Programmatic_Control import Mouse
            self.m = Mouse.Mouse()
        else:
            self.m = mouse

        if(keyboard == None):
            from Programmatic_Control import Keyboard
            self.kb = Keyboard.Keyboard()
        else:
            self.kb = keyboard

        self.inputs = [-1,-1,-1,-1,-1]
        self.i = 0
        self.prevID = 0

    def controlComputer(self, gestureID, x = None, y = None,):
        #print("gestureID = "+str(gestureID)+", gesture:")

        #prevent negative ID inputs
        if(gestureID < 0):
            #self.m.update(pressLeft=False, pressRight=False)
            print("not recognized")
            return

        """
        #only let gesture ID through if previous 5 ids match
        self.inputs[self.i] = gestureID
        if(self.i < len(self.inputs)-1):
            self.i += 1
        else:
            self.i = 0
        allMatch = True
        for i in self.inputs:
            if(i != gestureID):
                allMatch = False
                break

        #do not process input if id numbers not stable enough
        if(allMatch == False):
            return
        """

        #gestures with no button state change and are continually applied when active
        if (gestureID == 0):  # move mouse (dynamic)
            self.m.update(x=x, y=y)
            print("move mouse")

        else:
            # print("prev id = "+str(self.prevID)+", id now = "+str(gestureID))
            # gestures which are continually applied when active after button state change
            if (self.prevID == gestureID):
                if(gestureID == 4): # continue dragging
                    self.m.update(x=x, y=y)
                    print("drag")

            # gestures with button state change applied only once when ID changes (not continually as above)
            # test if previous id is different to avoid repeated actions
            else:
                #check if any previous actions need to be finished before starting the next action
                if (self.prevID == 4):  # release left click from drag
                    self.m.update(pressLeft=False)
                    print("drag end")

                #check which action should be done now
                if (gestureID == 1):  # left click (static)
                    self.m.update(pressLeft=True)
                    time.sleep(0.01)
                    self.m.update(pressLeft=False)
                    print("left click")

                elif (gestureID == 2):  # double left click (static)
                    self.m.update(pressLeft=True)
                    time.sleep(0.01)
                    self.m.update(pressLeft=False)
                    time.sleep(0.01)
                    self.m.update(pressLeft=True)
                    time.sleep(0.01)
                    self.m.update(pressLeft=False)
                    print("double click")

                elif (gestureID == 3):  # right click (static)
                    self.m.update(pressRight=True)
                    time.sleep(0.01)
                    self.m.update(pressRight=False)
                    print("right click")

                elif(gestureID == 4): # press left click for drag
                    #start drag
                    self.m.update(pressLeft=True, x=x, y=y)
                    print("drag start")

                elif (gestureID == 5):  # show/hide keyboard keyboard
                    self.kb.updateKey("CTRL", pressDown=True)
                    self.kb.updateKey("LEFT WINDOWS", pressDown=True)
                    self.kb.updateKey("O", pressDown=True)
                    self.kb.updateKey("O", pressDown=False)
                    self.kb.updateKey("LEFT WINDOWS", pressDown=False)
                    self.kb.updateKey("CTRL", pressDown=False)
                    print("show/hide keyboard")

        self.prevID = gestureID

if __name__ == "__main__":
    import Mouse
    import Keyboard

    m = Mouse.Mouse()
    kb = Keyboard.Keyboard()

    fsm = FSM(m,kb)
    fsm.controlComputer(5) #show keyboard
    time.sleep(1)
    fsm.controlComputer(1) #left click
    time.sleep(1)
    fsm.controlComputer(5) #hide keyboard
    time.sleep(1)
    fsm.controlComputer(4,0,0) #start drag at first coordinates
    time.sleep(1)
    fsm.controlComputer(0, 100, 100) #end drag at second coordinatess
    time.sleep(1)
    #gets stuck in drag state?
    fsm.controlComputer(0, 200, 200) #move mouse to third coordinates away from drag area
