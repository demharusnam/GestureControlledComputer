import cv2
import numpy as np
import math
import time
import imutils

def calculateFingers(result, drawing, thresh):
    """ Calculate fingers visible in frame [TODO: ADD DIRECTION]"""
    #  convexity defect
    convexHull = cv2.convexHull(result, returnPoints=False)
    visibleFingers = 0
    diff = 0
    thumb = False

    if len(convexHull) > 3:
        try:
            defects = cv2.convexityDefects(result, convexHull)
            #drawCenterOfMass(drawing, contours[0])
        except:
            return (0, False, 0)

        if defects is not None:

            for i in range(defects.shape[0]):  # calculate the angle
                s, e, f, d = defects[i][0]
                start = tuple(result[s][0])
                end = tuple(result[e][0])
                far = tuple(result[f][0])
                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                theta = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  # cosine law

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

                if theta < math.pi / 2 and far[1] <= boundaryY:  # angle less than 90 degrees are fingers
                    if theta > 1.22: # angle greater than 70 degrees is thumb
                        diff = far[1] - top[1]  # height difference between thumb and index
                        thumb = True

                    visibleFingers += 1

                    #cv2.circle(drawing, start, 8, [0, 0, 255], -1) # top right
                    #cv2.circle(drawing, end, 8, [0, 255, 0], -1) # top left
                    cv2.circle(drawing, far, 8, [255, 0, 0], -1) # angle

    return (visibleFingers, thumb, diff)

def beginGestureRecognition():
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
        lower = np.array([0, 48, 80], dtype="uint8")
        upper = np.array([20, 255, 255], dtype="uint8")
        skinMask = cv2.inRange(hsv, lower, upper)
        cv2.namedWindow('Threshold', cv2.WINDOW_NORMAL)
        cv2.moveWindow('Threshold', winWidth * 2 + 15, 0)
        skinMask = cv2.resize(skinMask, (winWidth, winHeight))
        cv2.imshow('Threshold', skinMask)


        # Contouring and Convex Hull
        contours, _ = cv2.findContours(skinMask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        length = len(contours)
        maxArea = -1

        if length > 0:
            for i in range(length):
                cnt = contours[i]
                area = cv2.contourArea(cnt)

                if area > maxArea:
                    maxArea = area
                    ci = i
                    result = contours[ci]

            hull = cv2.convexHull(result)

            drawing = np.zeros(img.shape, np.uint8)

            cv2.drawContours(drawing, [result], 0, (0, 255, 0), 2)
            cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)

            # Calculate visible fingers
            (visibleFingers, thumb, diff) = calculateFingers(result, drawing, skinMask.copy())

            # Determine gesture
            gestureText = ""

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

            if gestureText:
                selectedGesture = gestures[gestureText]

            cv2.putText(drawing, gestureText, (int(winWidth * 0.5), winHeight - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.namedWindow('Output', cv2.WINDOW_NORMAL)
            cv2.moveWindow('Output', winWidth * 2 + 15, winHeight) #only changing this line because screen is too small to fit (winWidth * 2 + 15, winHeight)
            drawing = cv2.resize(drawing, (winWidth, winHeight))
            cv2.imshow('Output', drawing)

        if cv2.waitKey(1) == 27:  # press ESC to exit
            break

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