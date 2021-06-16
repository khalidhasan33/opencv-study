import cv2
import numpy as np
import random
from crowd_detection import CrowdDetection

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
            using_roi = crowd.define_roi(frame)

        # Press Esc on keyboard to  exit
        if key == 27:
            break

    else:
        break

# When everything done, release the video capture object
video_cap.release()
cv2.destroyAllWindows()
