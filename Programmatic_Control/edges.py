import numpy as np
import cv2
import time

def nothing(x):
    pass

cap = cv2.VideoCapture(0)

cv2.namedWindow('steps')
cv2.createTrackbar('max threshold','steps',0,255,nothing)
cv2.createTrackbar('min threshold','steps',0,255,nothing)

ret, frame = cap.read()
smallFrame = cv2.resize(frame, (int(frame.shape[0] / 2), int(frame.shape[1] / 2)))
grey = cv2.cvtColor(smallFrame, cv2.COLOR_BGR2GRAY)
prev_edges = np.zeros((grey.shape[0], grey.shape[1],5), dtype = np.uint8)
diff_edges = np.zeros(grey.shape, dtype = np.uint8)
while(True):
    max_threshold = cv2.getTrackbarPos('max threshold','steps')
    min_threshold = cv2.getTrackbarPos('min threshold','steps')
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    smallFrame = cv2.resize(frame, (int(frame.shape[0]/2),int(frame.shape[1]/2)))
    grey = cv2.cvtColor(smallFrame, cv2.COLOR_BGR2GRAY)
    for i in [4,3,2,1]:
        prev_edges[:,:,i] = prev_edges[:,:,i-1].copy()
    prev_edges[:,:,0] = cv2.Canny(grey, min_threshold, max_threshold)
    avg_edges = np.mean(prev_edges, axis=2)
    diff_edges = prev_edges[:,:,0].copy()
    indices = np.where(avg_edges != prev_edges[:,:,0])
    err = diff_edges[indices]-avg_edges[indices]
    diff_edges[indices] = diff_edges[indices]-err;
    kernel = np.ones((2, 2), np.uint8)
    erosion = cv2.erode(diff_edges, kernel, iterations=1)
    #laplacian = cv2.Laplacian(diff_edges, cv2.CV_8U, 1, 1, 0, cv2.BORDER_DEFAULT)
    #canny2 = cv2.Canny(diff_edges, min_threshold, max_threshold)

    max = np.amax(grey)
    min = np.amin(grey)
    delta = max-min
    light = 0.75*delta + min
    midlight = 0.5*delta + min
    middark = 0.25*delta + min
    dark = min
    shades = np.zeros(grey.shape, dtype = np.uint8)
    shades[np.where(grey >= [light])] = [light]
    shades[np.where(([light] > grey) & (grey >= [midlight]))] = [midlight]
    shades[np.where(([midlight] >= grey) & (grey >= [middark]))] = [middark]
    shades[np.where(([middark] >= grey) & (grey >= [dark]))] = [dark]
    shades[np.where([dark] >= grey)] = [0]
    shadeBounds = np.zeros(shades.shape, dtype = np.uint8)
    #shadeBounds[np.where(([150] > grey) & (grey > [100]))] = [100]
    shadeCanny = cv2.Canny(grey, min_threshold, max_threshold)

    shadeEdges = np.zeros(shades.shape, dtype = np.uint8)
    shadeContours = np.zeros(grey.shape, dtype=np.uint8)
    d = 5;
    shadeEdges[np.where(([light+d] >= grey) & (grey >= [light-d]))] = [255]

    contours, hierarchy = cv2.findContours(shadeEdges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(shadeContours, contours, -1, 180, -1)

    shadeEdges[np.where(([midlight+d] >= grey) & (grey >= [midlight-d]))] = [200]
    shadeEdges[np.where(([middark+d] >= grey) & (grey >= [middark-d]))] = [150]
    shadeEdges[np.where(([dark+d] >= grey) & (grey >= [dark-d]))] = [100]

    shadeEdgeCanny = cv2.Canny(grey, min_threshold, max_threshold)

    # Display the resulting images
    top = np.concatenate((grey, shades, shadeEdges), axis = 1)
    bottom = np.concatenate((prev_edges[:,:,0], diff_edges, erosion), axis = 1)
    final = np.concatenate((top, bottom), axis = 0)
    cv2.imshow('steps', final)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(0.035)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()