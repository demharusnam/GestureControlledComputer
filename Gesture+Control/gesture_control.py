import cv2
import numpy as np

if __name__ == '__main__':
    # Begin video capture
    cap = cv2.VideoCapture(0)

    # perform image processing as long as camera is available
    while cap.isOpened():
        ret, frame = cap.read()

        # check frame is captured appropriately
        if not ret:
            print("Unable to retrieve frame. Exiting...")
            break

        # gray out image
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # add rectangle to indicate window of gesture capture
        height, width, _ = frame.shape
        sf = 0.3

        rect_width = int(width*sf)
        rect_height = int(height*(sf + 0.05))

        frame = cv2.rectangle(frame, (0, rect_height), (rect_width, 0), (0, 255, 0), 3)

        cv2.imshow('frame', frame)

        # press 'q' to quit
        if cv2.waitKey(1) == ord('q'):
            break

    # Release camera capture
    cap.release()
    cv2.destroyAllWindows()