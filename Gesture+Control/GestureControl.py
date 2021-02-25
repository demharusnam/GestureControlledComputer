import cv2
import numpy as np
import copy
import math

def identifyGesture():
    return

def calculateFingers(res, drawing):
    #  convexity defect
    convexHull = cv2.convexHull(res, returnPoints=False)

    if len(convexHull) > 3:
        defects = cv2.convexityDefects(res, convexHull)
        if defects is not None:
            count = 1
            for i in range(defects.shape[0]):  # calculate the angle
                s, e, f, d = defects[i][0]
                start = tuple(res[s][0])
                end = tuple(res[e][0])
                far = tuple(res[f][0])
                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                theta = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  # cosine law
                if theta <= math.pi / 2:  # angle less than 90 degree are fingers
                    count += 1
                    cv2.circle(drawing, far, 8, [211, 84, 0], -1)
            if count > 1:
                return count

    return 0

def beginGestureRecognition():
    # Open Camera
    camera = cv2.VideoCapture(0)
    #camera.set(10, 200)

    while camera.isOpened():
        # Camera setup
        ret, frame = camera.read()
        frame = cv2.bilateralFilter(frame, 5, 50, 100)  # Smoothing
        frame = cv2.flip(frame, 1)  # Horizontal Flip
        cv2.imshow('Input', frame)

        # Background Removal
        bgModel = cv2.createBackgroundSubtractorMOG2(0, 50)
        fgMask = bgModel.apply(frame)
        kernel = np.ones((3, 3), np.uint8)
        fgMask = cv2.erode(fgMask, kernel, iterations=1)
        img = cv2.bitwise_and(frame, frame, mask=fgMask)

        # Skin detect and thresholding
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = np.array([0, 48, 80], dtype="uint8")
        upper = np.array([20, 255, 255], dtype="uint8")
        skinMask = cv2.inRange(hsv, lower, upper)
        cv2.imshow('Threshold', skinMask)

        # Getting the contours and convex hull
        skinMask1 = copy.deepcopy(skinMask)
        contours, _ = cv2.findContours(skinMask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        length = len(contours)
        maxArea = -1

        if length > 0:
            for i in range(length):
                temp = contours[i]
                area = cv2.contourArea(temp)

                if area > maxArea:
                    maxArea = area
                    ci = i
                    result = contours[ci]

            hull = cv2.convexHull(result)
            drawing = np.zeros(img.shape, np.uint8)

            cv2.drawContours(drawing, [result], 0, (0, 255, 0), 2)
            cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)

            count = calculateFingers(result, drawing)

            print("Fingers Detected: ", count)

            cv2.imshow('Output', drawing)

        if cv2.waitKey(10) == 27:  # press ESC to exit
            break

if __name__ == '__main__':
    beginGestureRecognition()