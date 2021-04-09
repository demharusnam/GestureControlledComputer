import cv2
import numpy as np
import math
import time
import imutils

from Programmatic_Control import GestureID_to_PControl

def calculateFingers(result, drawing, thresh):
    """ Calculate fingers visible in frame [TODO: ADD DIRECTION]"""
    convexHull = cv2.convexHull(result, returnPoints=False)
    #  convexity defect
    visibleFingers = 0
    diff = 0
    thumb = False
    smallAngles = 0
    cX = cY = -1

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
            cv2.circle(drawing, (cX,cY), 8, [0, 255, 0], -1)  # center of mass
            # line below which thumb must lie
            thumbBound = int(cY-math.sqrt(area)/20)
            cv2.line(drawing, (cX-16, thumbBound), (cX+16, thumbBound), [255, 150, 150], 2)

            #line above which all points of concave triangles must lie
            concaveBound = cY+20 #int(cY+10+math.sqrt(area)/10)
            cv2.line(drawing, (cX-100, concaveBound), (cX+100, concaveBound), [255, 255, 255], 2)

            #defect_far = []
            #defect_angles = []

            defectPoints = []
            angles = []
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
                #if(start[1] <= concaveBound and end[1] <= concaveBound):
                w = end[0] - start[0]
                h = end[1] - start[1]
                dist_sq = w*w + h*h
                if (dist_sq > area or concave_dip_sq > area / 16):
                    defectPoints.append((start,end,far))
                    angles.append(theta)
                    visibleFingers += 1
                    # ignore any concave triangles with angles over 120 degrees, or whose triangle depth (aka the dip) is not "big enough" relative to the size of the hand
                    # changes in concave triangle depth are relative to area of hand to account for distance of hand from camera
                    #if theta < math.pi / 1.5 and concave_dip_sq > area / 16:  # angle less than 90 degrees are fingers
                    if True:  # angle less than 90 degrees are fingers
                        #print("distance to convex defect: "+str(concave_dip_sq)+", area = "+str(math.sqrt(area)))
                        #defect_far.append(far)
                        #defect_angles.append(theta)
                        #rad = math.sqrt(area)
                        #cv2.circle(drawing, far, int(rad/1.5), [255, 255, 255], 1)  # angle
                        #cv2.circle(drawing, far, int(rad/4), [255, 255, 255], 1)  # angle

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

                        cv2.circle(drawing, end, 8, [255, 255, 0], -1)  # angle
                        cv2.circle(drawing, start, 8, [0, 255, 255], -1)  # angle

            biggestAngle = 0
            biggestDist_sq = 0
            lowest_y = 0
            thumbSideWrist = -1
            pinkySideWrist = -1
            #search for wrist side by pinky
            totalFingersCentroid = np.array((0,0))
            totalFingersArea = 0
            x = cX
            y = cY

            if(len(angles) > 1):
                #search for sides of wrist
                for i in range(0,len(angles)):
                    # search for wrist features
                    (start, end, far) = defectPoints[i]
                    theta = angles[i]

                    w = end[0] - start[0]
                    h = end[1] - start[1]
                    dist_sq = w * w + h * h

                    # search for the biggest angle or the biggest distance from valid finger angles

                    if (True):
                        if (far[1] > lowest_y):
                            lowest_y = far[1]
                            thumbSideWrist = pinkySideWrist
                            pinkySideWrist = i

                    """
                    if(theta > biggestAngle):
                        biggestAngle = theta
                        index = i
                    """

                #calculate total finger area and center of mass
                for i in range(0,len(angles)):
                    if((i == pinkySideWrist and i-1 != thumbSideWrist) or (i == thumbSideWrist and i-1 != pinkySideWrist)):
                        #estimate rectangle around length from start point to far point
                        a = np.array(defectPoints[i][0])  # start point of this angle
                        b = np.array(defectPoints[i][2])  # far point of this angle

                        w = a[0]-b[0]
                        h = a[1]-b[1]
                        length_ab = math.sqrt(w*w + h*h)
                        length_bc = 50.0
                        fingerArea = length_ab*length_bc

                        unit_vec_ab = (a-b)/length_ab
                        #rotate unit vector of ab by 90 degrees
                        unit_vec_bc = np.array([unit_vec_ab[1], -unit_vec_ab[0]])
                        c = b + length_bc*unit_vec_bc
                        #round point c to nearest int coordinates
                        c = (int(c[0]), int(c[1]))
                        d = (b-a)+c
                        print((a,b,c,d))
                        cv2.line(drawing, tuple(a), tuple(b), [200, 0, 0], 2)
                        cv2.line(drawing, tuple(b), tuple(c), [255, 255, 255], 2)
                        cv2.line(drawing, tuple(c), tuple(d), [200, 0, 0], 2)
                        cv2.line(drawing, tuple(d), tuple(a), [0, 0, 200], 2)

                    else:
                        #get quadrilateral of finger between previous angle and this angle
                        a = np.array(defectPoints[i][0]) #start point of this angle
                        b = np.array(defectPoints[i][2]) #far point of this angle
                        if(i == 0):
                            c = np.array(defectPoints[len(angles)-1][2])  # far point of last angle
                            d = np.array(defectPoints[len(angles)-1][1])  # end point of last angle
                        else:
                            c = np.array(defectPoints[i-1][2]) #far point of last angle
                            d = np.array(defectPoints[i-1][1]) #end point of last angle

                        #diagonals of quadrilateral
                        diagAC = c-a
                        diagDB = b-d

                        #cross product of diagonal ac with diagonal db
                        crossProd = diagAC[0]*diagDB[1] - diagAC[1]*diagDB[0]
                        if crossProd < 0:
                            fingerArea = -0.5*crossProd
                        else:
                            fingerArea = 0.5*crossProd

                        # draw quadrilateral
                        # pts = np.array([a,b,c,d], np.int32)
                        # pts = pts.reshape((-1,1,2))
                        # cv2.polylines(drawing, tuple(pts), True, [255,255,255], 3)
                        cv2.line(drawing, tuple(a), tuple(b), [200, 200, 200], 2)
                        cv2.line(drawing, tuple(b), tuple(c), [255, 255, 255], 2)
                        cv2.line(drawing, tuple(c), tuple(d), [200, 200, 200], 2)
                        cv2.line(drawing, tuple(d), tuple(a), [200, 200, 200], 2)

                    #rough way of estimating centroid of quadrilateral
                    fingerCentroid = (a+b+c+d)/4

                    #add to centroid and area of all fingers
                    totalFingersCentroid = totalFingersCentroid + fingerArea*fingerCentroid
                    totalFingersArea = totalFingersArea + fingerArea

            #draw improved center of mass and wrist features
            print("totalFingersArea = "+str(totalFingersArea))
            if(totalFingersArea != 0):
                totalFingersCentroid = totalFingersCentroid/totalFingersArea
                x = int((area*cX - totalFingersArea*totalFingersCentroid[0])/(area-totalFingersArea))
                y = int((area*cY - totalFingersArea*totalFingersCentroid[1])/(area-totalFingersArea))

            print("x = " + str(x) + ", y = " + str(y))
            cv2.circle(drawing, (x, y), 4, [255, 255, 255], -1)  # center of mass w/o fingers

            if(pinkySideWrist != -1):
                far = defectPoints[pinkySideWrist][2]
                cv2.circle(drawing, far, 8, [255, 255, 255], -1)  # angle

            if (thumbSideWrist != -1):
                far = defectPoints[thumbSideWrist][2]
                cv2.circle(drawing, far, 8, [255, 255, 255], -1)  # angle

    return (visibleFingers, thumb, diff, smallAngles, x, y)


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

    screenWidth = 1480 #1280
    screenHeight = 920 #720
    offsetX = 50
    offsetY = 50
    ratioX = int((screenWidth)/(winWidth-2*offsetX))
    ratioY = int((screenHeight)/(winHeight-2*offsetY-10))

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
        #time.sleep(0.5)
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

            #print("angles = " + str(visibleFingers) + " smallAngles = " + str(smallAngles)+" thumb = "+str(thumb))
            cv2.rectangle(drawing, (offsetX, offsetY), (winWidth-offsetX, winHeight-offsetY), [255, 255, 255], 1)
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
                    else:
                        if smallAngles == 3:
                            gestureText = "Show/Hide KB"

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
        #print("key = "+str(key))
        if key == 27:  # press ESC to exit
            break

        elif key == 8: #press BACKSPACE to let gestures control mouse
            enableControl = True

        elif key == 32: #press SPACEBAR to stop gestures from controlling mouse
            enableControl = False
        #print(centerX, centerY)
        #print("control = "+str(enableControl))
        if(enableControl):
            #programmatic control section
            fsm.controlComputer(selectedGesture, (centerX-offsetX)*ratioX, y = (centerY-offsetY)*ratioY)

# Toni use these as gesture codes
gestures = {
    "Move Mouse": 0,
    "Left Click" : 1,
    "Double Click" : 2,
    "Right Click" : 3,
    "Drag" : 4,
    "Show/Hide KB" : 5,
}

# SELECTED GESTURE CODE
selectedGesture = -1;

if __name__ == '__main__':
    beginGestureRecognition()