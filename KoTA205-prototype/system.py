import cv2
import imutils
import numpy as np
import random
from crowd_detection import CrowdDetection, pts

# Definition
crowd = CrowdDetection
using_roi = False
video_cap = cv2.VideoCapture('resource/video.mp4')

# Check if camera opened successfully
if not video_cap.isOpened():
    print("Error opening video stream or file")

# Input ROI
threshold = input("Please defined the threshold you want? ")
# Read until video is completed
while video_cap.isOpened():
    ret, frame = video_cap.read()

    if ret:
        key = cv2.waitKey(1) & 0xFF
        # Crowd counting
        random_radius = random.randint(0, 400)
        mask = np.zeros((frame.shape[0], frame.shape[1], 3), np.uint8)
        cv2.circle(mask, (500, 450), 100 + random_radius, 255, -1)
        percentage = crowd.occupancy_counting(frame, mask)
        print('Occupancy = ' + percentage + '%')
        if using_roi:
            crowd.display_frame_roi(frame)
        else:
            crowd.display_frame(frame)

        # Press a on keyboard to create ROI
        if key == ord("a"):
            print("[INFO] Click the left button: select the point")
            print("[INFO] Click the right button: delete the last selected point")
            print("[INFO] Click the middle button: determine the ROI area")
            print("[INFO] Press ‘a’ to determine the selection area")
            print("[INFO] Press ESC to quit")

            while True:
                key = cv2.waitKey(1) & 0xFF
                # Create windows and bind windows to callback functions
                cv2.setMouseCallback('system', crowd.draw_roi, frame)

                if key == ord("a") and len(pts) >= 4:
                    using_roi = True
                    cv2.setMouseCallback('system', lambda *args: None)
                    break

                if key == 27:
                    using_roi = False
                    cv2.setMouseCallback('system', lambda *args: None)
                    break

        # Press Esc on keyboard to  exit
        if key == 27:
            break

    # Break the loop
    else:
        break

# When everything done, release the video capture object
video_cap.release()
# Closes all the frames
cv2.destroyAllWindows()
