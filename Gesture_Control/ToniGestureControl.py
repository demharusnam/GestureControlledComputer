import cv2
import numpy as np
import math
import time
import imutils

from Programmatic_Control import GestureID_to_PControl

def calculateFingers(result, drawing, thresh):
    """ Calculate fingers visible in frame [TODO: ADD DIRECTION]"""
    #  convexity defect
    convexHull = cv2.convexHull(result, returnPoints=False)
    visibleFingers = 0
    diff = 0
    thumb = False
    smallAngles = 0

    if len(convexHull) > 3:
        try:
            defects = cv2.convexityDefects(result, convexHull)
            #drawCenterOfMass(drawing, contours[0])
        except:
            return (0, False, 0)

        if defects is not None:
            area = cv2.contourArea(result)

            #center point of hand
            M = cv2.moments(result)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(drawing, (cX,cY), 8, [255, 255, 255], -1)  # center of mass
            # line below which thumb must lie
            thumbBound = int(cY-math.sqrt(area)/10)
            cv2.line(drawing, (cX-16, thumbBound), (cX+16, thumbBound), [255, 150, 150], 2)

            #line above which all points of concave triangles must lie
            concaveBound = int(cY+10+math.sqrt(area)/10)
            cv2.line(drawing, (cX-100, concaveBound), (cX+100, concaveBound), [255, 255, 255], 2)

            #defect_far = []
            #defect_angles = []
            for i in range(defects.shape[0]):  # calculate the angle
                s, e, f, d = defects[i][0]

                start = tuple(result[s][0])
                end = tuple(result[e][0])
                far = tuple(result[f][0])

                # calculate distance of the concave dip in the convex shell
                # calculates the shortest distance from the far point to the line connecting the start and end points
                # Note: Square roots are SLOW!
                # This section of code tries to use the squared version of distance where possible
                w = start[0]-end[0]
                h = start[1]-end[1]
                L1 = math.sqrt(w*w + h*h) # Length 1
                w = start[0]-far[0]
                h = start[1]-far[1]
                L2_sq = w*w + h*h #Length 2 squared
                w = far[0]-end[0]
                h = far[1]-end[1]
                L3_sq = w*w + h*h #Length 3 squared
                delta = (L1/2)+(L2_sq-L3_sq)/(2*L1)
                concave_dip_sq = L2_sq - delta*delta
                #print(concave_dip_sq)

                """
                cv2.circle(drawing, far, 8, [255, 0, 0], -1)  # angle
                cv2.circle(drawing, end, 8, [255, 255, 0], -1)  # angle
                cv2.circle(drawing, start, 8, [0, 255, 255], -1)  # angle
                """
                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                theta = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  # cosine law

                """
                try:
                    cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    cnts = imutils.grab_contours(cnts)
                    c = max(cnts, key=cv2.contourArea)
                    top = tuple(c[c[:, :, 1].argmin()][0])
                    bot = tuple(c[c[:, :, 1].argmax()][0])
                    boundaryY = int(float(bot[1]) * 0.7) # only mark fingers above this point i.e. reduce false positives
                    #cv2.circle(drawing, top, 8, (255, 255, 0), -1) # topmost point in hand contour
                    #cv2.circle(drawing, bot, 8, (255, 255, 0), -1) # bottom-most point in hand contour
                except:
                    boundaryY = 0
                """

                #if theta < math.pi / 2 and far[1] <= boundaryY:  # angle less than 90 degrees are fingers

                # ignore any concave triangles whose start OR end points are below the center of mass (or somewhere close to it)
                # screen cordinates go down from the top left corner, which is why all the height logic looks backwards
                if(start[1] <= concaveBound and end[1] <= concaveBound):

                    # ignore any concave triangles with angles over 120 degrees, or whose triangle depth (aka the dip) is not "big enough" relative to the size of the hand
                    # changes in concave triangle depth are relative to area of hand to account for distance of hand from camera
                    if theta < math.pi / 1.5 and concave_dip_sq > area/16:  # angle less than 90 degrees are fingers
                        #print("distance to convex defect: "+str(concave_dip_sq)+", area = "+str(math.sqrt(area)))
                        #defect_far.append(far)
                        #defect_angles.append(theta)

                        if theta >= math.pi/2.75: # angle less than 60 degrees is small

                            # convexity defect far point that is close-ish to center of mass height is probably connected thumb
                            # cY-sqrt(area) to account for changes in center of mass due to arm?
                            # was testing code with sweater until this point
                            if (far[1] >= thumbBound):
                                thumb = True
                                cv2.rectangle(drawing, (far[0]-8,far[1]-8), (far[0]+8,far[1]+8), [255, 150, 150], -1)  # angle
                            else:
                                cv2.circle(drawing, far, 8, [255, 100, 100], -1)  # angle
                        else:
                            smallAngles += 1
                            cv2.circle(drawing, far, 8, [255, 0, 255], -1)  # angle


                        """
                        if theta > 1.22:  # angle greater than 70 degrees is thumb
                            # diff = far[1] - top[1]  # height difference between thumb and index
    
                            #w = start[0] - end[0]
                            #h = start[1] - end[1]
                            #diff = math.sqrt(w * w + h * h)  # distance between thumb joint and index joint
                            #if (diff > 10):
                            #    thumb = True
                        """

                        visibleFingers += 1

                        #cv2.circle(drawing, start, 8, [0, 0, 255], -1) # top right
                        #cv2.circle(drawing, end, 8, [0, 255, 0], -1) # top left
                        #cv2.circle(drawing, far, 8, [255, 0, 0], -1) # angle
                        cv2.circle(drawing, end, 8, [255, 255, 0], -1)  # angle
                        cv2.circle(drawing, start, 8, [0, 255, 255], -1)  # angle

            """
            # assumes left hand
            for i in range(0, visibleFingers):

                if defect_angles[i] > 1.22:  # angle greater than 70 degrees is thumb
                    #test if distance to 2 nearest knuckles are not similar
                    if(i > 0):
                        w = defect_far[i][0] - defect_far[i-1][0]
                        h = defect_far[i][1] - defect_far[i-1][1]
                        diff = math.sqrt(w * w + h * h)  # distance between thumb joint and index joint
                        if (diff > 10):
                            thumb = True
                            break
                    if(i < visibleFingers-1):
                        w = defect_far[i][0] - defect_far[i + 1][0]
                        h = defect_far[i][1] - defect_far[i + 1][1]
                        diff = math.sqrt(w * w + h * h)  # distance between thumb joint and index joint
                        if (diff > 10):
                            thumb = True
                            break
            """

    return (visibleFingers, thumb, diff, smallAngles, cX, cY)


#face = cv2.imread("face.png",cv2.IMREAD_GRAYSCALE)
#faceContours, _ = cv2.findContours(face, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

def beginGestureRecognition():
    fsm = GestureID_to_PControl.FSM()
    enableControl = False

    """ Perform Gesture Recognition """
    # Open Camera
    camera = cv2.VideoCapture(0)

    winWidth = 426
    winHeight = 240

    # OPENCV's DEFAULT FPS CHECKING METHOD ONLY WORKS ON VIDEO FILES - NOT LIVE FEED
    # Checking FPS
    fps = 15

    startTime = time.time()

    for _ in range(fps):
        _, _ = camera.read()

    endTime = time.time()
    timeElapsed = endTime - startTime
    fps = fps / timeElapsed

    print("~FPS: ", int(fps))

    # HAVEN'T CODED IN FPS CONTROL YET. THE ABOVE CODE JUST IDENTIFIES THE CAMERA FPS.
    # GOAL IS TO KEEP IT UNDER 30FPS FOR PERFORMANCE EFFICIENCY.

    while camera.isOpened():
        #time.sleep(0.2)
        # Camera setup
        ret, frame = camera.read()
        frame = cv2.bilateralFilter(frame, 5, 50, 100)  # Smoothing
        frame = cv2.flip(frame, 1)  # Horizontal Flip
        cv2.namedWindow('Input', cv2.WINDOW_NORMAL)
        frame = cv2.resize(frame, (winWidth, winHeight))
        cv2.moveWindow('Input', winWidth + 15, 0)
        cv2.imshow('Input', frame)

        # Background Removal
        bgModel = cv2.createBackgroundSubtractorMOG2(0, 50)
        fgMask = bgModel.apply(frame)
        kernel = np.ones((3, 3), np.uint8)
        fgMask = cv2.erode(fgMask, kernel, iterations=1)
        img = cv2.bitwise_and(frame, frame, mask=fgMask)

        # Skin detection and thresholding
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        #hsv = cv2.bilateralFilter(hsv,5,75,75)
        hsv = cv2.blur(hsv, (5, 5))
        hsv = cv2.medianBlur(hsv, 5)
        cv2.imshow('Blur', hsv)

        lower = np.array([0, 48, 80], dtype="uint8")
        upper = np.array([20, 255, 255], dtype="uint8")
        skinMask = cv2.inRange(hsv.copy(), lower, upper)
        cv2.namedWindow('Threshold', cv2.WINDOW_NORMAL)
        cv2.moveWindow('Threshold', winWidth * 2 + 15, 0)
        #skinMask = cv2.resize(skinMask, (winWidth, winHeight))

        skinMask = cv2.blur(skinMask, (10, 10))
        #skinMask = cv2.erode(skinMask, (10, 10))
        #skinMask = cv2.bilateralFilter(skinMask,5,75,75)
        #skinMask = cv2.medianBlur(skinMask, 5)

        cv2.imshow('Threshold', skinMask)

        """
        edges = cv2.Canny(hsv.copy(), 130,150)
        edges = cv2.dilate(edges, (10,10), iterations = 3)
        #edges = cv2.blur(edges, (5,5))
        #edges = cv2.resize(edges, (winWidth, winHeight))
        cv2.namedWindow('edges', cv2.WINDOW_NORMAL)
        cv2.moveWindow('edges', 0, winHeight)
        cv2.imshow('edges', edges)

        skinMask2 = skinMask.copy()
        skinMask2[np.where(edges != [0])] = [0]
        skinMask2 = cv2.erode(skinMask2, (10,10), iterations = 3)
        cv2.namedWindow('thresh w div', cv2.WINDOW_NORMAL)
        cv2.moveWindow('thresh w div', 2*winWidth, winHeight)
        cv2.imshow('thresh w div', skinMask2)
        
        skinMaskCircles = skinMask2.copy()
        circles = cv2.HoughCircles(skinMaskCircles, cv2.HOUGH_GRADIENT, 1.2, 5)
        if(circles is not None):
            circles = np.round(circles[0,:]).astype("int")

            for (x,y,r) in circles:
                cv2.circle(skinMaskCircles, (x,y), r, (255, 0, 255), 4)

        cv2.namedWindow('circles', cv2.WINDOW_NORMAL)
        cv2.moveWindow('circles', 2 * winWidth, winHeight)
        cv2.imshow('circles', skinMaskCircles)
        """
        # Contouring and Convex Hull
        contours, _ = cv2.findContours(skinMask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        length = len(contours)
        maxArea = -1

        if length > 0:
            for i in range(length):
                cnt = contours[i]
                area = cv2.contourArea(cnt)
                #faceSimilarity = cv2.matchShapes(contours[0], faceContours[0],1,0.0)
                #if(faceSimilarity > 0.1):
                if area > maxArea:
                    maxArea = area
                    ci = i
                    result = contours[ci]

            hull = cv2.convexHull(result)

            drawing = np.zeros(img.shape, np.uint8)

            cv2.drawContours(drawing, [result], 0, (0, 255, 0), 2)
            cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)

            # Calculate visible fingers
            (visibleFingers, thumb, diff, smallAngles, centerX, centerY) = calculateFingers(result, drawing, skinMask.copy())
            #print("visible fingers = " + str(visibleFingers) + " smallAngles = " + str(smallAngles) + " diff = " + str(diff))

            print("angles = " + str(visibleFingers) + " smallAngles = " + str(smallAngles)+" thumb = "+str(thumb))

            # Determine gesture
            gestureText = ""

            """
            if len(hull) >= 18:  # a hand
                if visibleFingers == 1:
                    if thumb and diff < 80:
                        gestureText = "Left Click"
                    elif thumb and diff > 80:
                        gestureText = "Right Click"
                    elif not thumb and diff > 80:
                        gestureText = "Drag"
                elif visibleFingers == 2 and diff > 80:
                        gestureText = "Double Click"
                else:
                    gestureText = "Move Mouse"
            """
            angles = visibleFingers
            selectedGesture = -1
            if len(hull) >= 18:  # a hand
                if angles == 0:
                    gestureText = "Move Mouse"
                    #m.update(x = mouseX, y = mouseY)
                elif angles == 1:
                    if thumb:
                        gestureText = "Left Click"
                    else:
                        if smallAngles != 0:
                            gestureText = "Drag"
                elif angles == 2:
                    if thumb:
                        if smallAngles == 0:
                            gestureText = "Right Click"
                        else:
                            gestureText = "Double Click"
                    else:
                        gestureText = "Drag"
                elif angles == 3:
                    if thumb:
                        gestureText = "Double Click"

                if gestureText == "":
                    gestureText = "None"
                else:
                    selectedGesture = gestures[gestureText]

            cv2.putText(drawing, gestureText, (int(winWidth * 0.5), winHeight - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.namedWindow('Output', cv2.WINDOW_NORMAL)
            cv2.moveWindow('Output', winWidth, winHeight)
            drawing = cv2.resize(drawing, (winWidth, winHeight))
            cv2.imshow('Output', drawing)

        key = cv2.waitKey(1)
        print("key = "+str(key))
        if key == 27:  # press ESC to exit
            break

        elif key == 8: #press BACKSPACE to let gestures control mouse
            enableControl = True

        elif key == 32: #press SPACEBAR to stop gestures from controlling mouse
            enableControl = False

        print("control = "+str(enableControl))
        if(enableControl):
            #programmatic control section
            fsm.controlComputer(selectedGesture, centerX*3, y = centerY*3)

# Toni use these as gesture codes
gestures = {
    "Move Mouse": 0,
    "Left Click" : 1,
    "Double Click" : 2,
    "Right Click" : 3,
    "Drag" : 4,
}

# SELECTED GESTURE CODE
selectedGesture = -1;

if __name__ == '__main__':
    beginGestureRecognition()