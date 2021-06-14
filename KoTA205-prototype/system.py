import cv2
import imutils
import numpy as np
from crowd_detection import CrowdDetection

# Definition
crowd = CrowdDetection
frame = cv2.imread("image.jpg")
frame = imutils.resize(frame, width=500)
# Crowd counting
mask = np.zeros((500, 500, 3), np.uint8)
cv2.circle(mask, (400, 100), 100, 255, -1)
# Input ROI
threshold = input("Please defined the threshold you want? ")

cv2.namedWindow('system')
cv2.imshow('system', frame)
cv2.imshow('mask', mask)
percentage = crowd.occupancy_counting(frame, mask)
print('Occupancy = ' + percentage + '%')
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord("a"):
        key = cv2.waitKey(1) & 0xFF
        # Create windows and bind windows to callback functions
        cv2.setMouseCallback('system', crowd.draw_roi, frame)

        print("[INFO] Click the left button: select the point")
        print("[INFO] Click the right button: delete the last selected point")
        print("[INFO] Click the middle button: determine the ROI area")
        print("[INFO] Press ‘S’ to determine the selection area and save it")
        print("[INFO] Press ESC to quit")

    if key == 27:
        break

cv2.destroyAllWindows()
