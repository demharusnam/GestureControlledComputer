import cv2
import numpy as np
import math
import time

def drawCenterOfMass(img, cnt):
    """ Determine center of hand """
    M = cv2.moments(cnt)

    if len(cnt) == 0 and M['m00'] == 0:
        return

    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    cv2.circle(img, (cX,cY), 8, [255, 0, 0], 3)

def calculateFingers(res, drawing, contours):
    """ Calculate fingers visible in frame [TODO: ADD DIRECTION]"""
    #  convexity defect
    convexHull = cv2.convexHull(res, returnPoints=False)
    visibleFingers = 0

    if len(convexHull) > 3:
        try:
            defects = cv2.convexityDefects(res, convexHull)
            #drawCenterOfMass(drawing, contours[0])
        except:
            return 0

        if defects is not None:

            for i in range(defects.shape[0]):  # calculate the angle
                s, e, f, d = defects[i][0]
                start = tuple(res[s][0])
                end = tuple(res[e][0])
                far = tuple(res[f][0])
                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                theta = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  # cosine law
                if theta < math.pi / 2:  # angle less than 90 degree are fingers
                    visibleFingers += 1
                    cv2.circle(drawing, far, 8, [255, 0, 0], -1)

    return visibleFingers

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
        contours, _ = cv2.findContours(skinMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
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

            # Calculating Fingers visible
            visibleFingers = calculateFingers(result, drawing, contours)

            try:
                gestureText = gestures[visibleFingers]
            except:
                gestureText = ""

            cv2.putText(drawing, gestureText, (int(winWidth * 0.5), winHeight - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.namedWindow('Output', cv2.WINDOW_NORMAL)
            cv2.moveWindow('Output', winWidth * 3 + 15, 0)
            drawing = cv2.resize(drawing, (winWidth, winHeight))
            cv2.imshow('Output', drawing)

        if cv2.waitKey(10) == 27:  # press ESC to exit
            break


gestures = {
    0 : "Move Mouse",
    1 : "Drag",
    2 : "Double Click",
}

if __name__ == '__main__':
    beginGestureRecognition()