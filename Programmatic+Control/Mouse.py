from WINDOWS_API_STRUCTS import UINT, LONG, DWORD, ULONG_PTR, INPUT_MOUSE
from WINDOWS_API_STRUCTS import MOUSEINPUT, DUMMYUNIONNAME, INPUT, LPINPUT, INPUT_BYTES
from WINDOWS_API_STRUCTS import windll
from WINDOWS_VIRTUAL_KEY_CODES import VK_LBUTTON, VK_RBUTTON
#from Keyboard import updateKey

# flags for MOUSEINPUT dwFlags parameter
MOUSEEVENTF_ABSOLUTE = 0x8000  # specify absolute coordinates to move mouse to
MOUSEEVENTF_MOVE = 0x0001  # mouse has moved
MOUSEEVENTF_HWHEEL = 0x01000  # mouse wheel moved horizontally (+ for right, - for left)
MOUSEEVENTF_WHEEL = 0x0800  # mouse wheel moved vertically (+ for up, - for down)
MOUSEEVENTF_VIRTUALDESK = 0x4000  # move mouse to absolute desktop screen coordinates
# Must be used with MOUSEEVENTF_ABSOLUTE.
MOUSEEVENTF_LEFTDOWN = 0x0002  # press left mouse button
MOUSEEVENTF_LEFTUP = 0x0004  # release left mouse button
MOUSEEVENTF_RIGHTDOWN = 0x0008  # press right mouse button
MOUSEEVENTF_RIGHTUP = 0x0010  # release right mouse button

# https://stackoverflow.com/questions/4631292/how-detect-current-screen-resolution
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getsystemmetrics?redirectedfrom=MSDN
# parameters codes for getting a specific system metric
SM_CMONITORS = 80
SM_CXVIRTUALSCREEN = 78
SM_CYVIRTUALSCREEN = 79

class Mouse:
    def __init__(self):
        # use a single INPUT struct so its memory can be reused when the mouse is updated multiple times
        self.inputStructPtr = LPINPUT(INPUT(INPUT_MOUSE, DUMMYUNIONNAME(mi = MOUSEINPUT())))
        self.inputStructPtr.contents.dummyUnion.mouseInput.time = DWORD(0)  # set time to 0 so system assigns its own time
        self.inputStructPtr.contents.dummyUnion.mouseInput.dwExtraInfo = ULONG_PTR(LONG(windll.user32.GetMessageExtraInfo()))  # get data for dwExtraInfo from calling GetMessageExtraInfo()


        print("number of monitors is ",windll.user32.GetSystemMetrics(SM_CMONITORS))
        self.screenWidth = windll.user32.GetSystemMetrics(SM_CXVIRTUALSCREEN)
        self.screenHeight = windll.user32.GetSystemMetrics(SM_CYVIRTUALSCREEN)
        print("screen is ", self.screenWidth," px wide by ", self.screenHeight," px tall")

    # must normalize x and y if using absolute coordinates
    # https://stackoverflow.com/questions/49026921/sendinput-always-moves-mouse-pointer-to-left-top-corner
    def __normalizePos(self, dxPos, dyPos):
        print("screen width = %d px, screen height = %d px" % (self.screenWidth, self.screenHeight))
        #screen coords go from 0 to 65535 in both directions
        return (round(dxPos*65535/self.screenWidth), round(dyPos*65535/self.screenHeight))

    #Movement of mouse pointer position works best when using absolute coordinates for screen pixels
    #Relative coordinates for mouse pointer position uses a different scaling factor which I haven't accounted for
    #Scrolling units seems to be relative to "wheel ticks", not screen pixels
    def update(self, x = -1, y = -1, absPos = True, dxScroll = 0, dyScroll = 0, pressLeft = False, pressRight = False):
        self.dwFlags = 0

        if (absPos):
            if((x > -1) or (y > -1)):
                self.dwFlags = self.dwFlags | MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_VIRTUALDESK | MOUSEEVENTF_MOVE
                print("mouse will move to pos (%s, %s)" % (x, y))
                (x,y) = self.__normalizePos(x,y)

        elif((x != 0) or (y != 0)): #if the x or y positions of the mouse changed
            self.dwFlags = self.dwFlags | MOUSEEVENTF_MOVE
            print("mouse will change pos by (%s, %s)" % (x,y))

        if((dyScroll != 0) or (dxScroll != 0)):
            self.dwFlags = self.dwFlags | MOUSEEVENTF_WHEEL

        if(pressLeft):
            if ((windll.user32.GetKeyState(VK_LBUTTON) & 0x100) == 0):
                self.dwFlags = self.dwFlags | MOUSEEVENTF_LEFTDOWN
                print("pressing left button")
            else:
                print("left button already pressed")
        else:
            if((windll.user32.GetKeyState(VK_LBUTTON) & 0x100) != 0):
                self.dwFlags = self.dwFlags | MOUSEEVENTF_LEFTUP
                print("releasing left button")
            else:
                print("left button already released")

        if (pressRight):
            if ((windll.user32.GetKeyState(VK_RBUTTON) & 0x100) == 0):
                self.dwFlags = self.dwFlags | MOUSEEVENTF_RIGHTDOWN
                print("pressing right button")
            else:
                print("right button already pressed")
        else:
            if ((windll.user32.GetKeyState(VK_RBUTTON) & 0x100) != 0):
                self.dwFlags = self.dwFlags | MOUSEEVENTF_RIGHTUP
                print("releasing right button")
            else:
                print("right button already released")

        #if any part of mouse should be changed, dwFlags will be non-zero
        if(self.dwFlags != 0):

            self.inputStructPtr.contents.dummyUnion.mouseInput.dx = LONG(x)
            self.inputStructPtr.contents.dummyUnion.mouseInput.dy = LONG(y)
            self.inputStructPtr.contents.dummyUnion.mouseInput.mouseData = DWORD(0) #specifies mouse scroll wheel value relative to WHEEL_TICKS = 120?
            self.inputStructPtr.contents.dummyUnion.mouseInput.dwFlags = DWORD(self.dwFlags)

            """resources on converting from WN_WHEELTICKS to pixels
                https://stackoverflow.com/questions/7763326/how-many-pixels-are-scrolled-on-a-website-with-a-mouse-wheel-down-event
                https: // docs.microsoft.com / en - us / previous - versions / ms997498(v=msdn.10)?redirectedfrom = MSDN
            """

            #check for vertical scrolling
            if(dyScroll != 0):
                print("scrolling vertically by %s" % (dyScroll))
                self.inputStructPtr.contents.dummyUnion.mouseInput.mouseData = DWORD(dyScroll)

            #update mouse
            # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendinput
            # parameters of sendInput are:
            # UINT cInputs = number of structs in pInput,
            # LPINPUT pInputs = pointer to array of INPUT structs
            # int cbSize = size (in bytes) of an INPUT struct
            windll.user32.SendInput(UINT(1), self.inputStructPtr, INPUT_BYTES)

            #check for horizontal scrolling, update mouse a second time
            if(dxScroll != 0):
                print("scrolling horizontally by %s" % (dyScroll))
                # repeat the input change with dxScroll replacing dyScroll
                #changeKeyState("shift", False)
                self.inputStructPtr.contents.dummyUnion.mouseInput.mouseData = DWORD(dxScroll)
                windll.user32.SendInput(UINT(1), self.inputStructPtr, INPUT_BYTES)
                #changeKeyState("shift", False)
        print()