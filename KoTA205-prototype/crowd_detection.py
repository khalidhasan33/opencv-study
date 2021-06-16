import cv2
import joblib
import numpy as np

pts = []  # for storing points


class CrowdDetection:

    @staticmethod
    def display_frame(img):
        cv2.imshow('system', img)

    @staticmethod
    def display_frame_roi(img):
        img2 = img.copy()
        for i in range(len(pts) - 1):
            cv2.circle(img2, pts[i], 5, (0, 0, 255), -1)  # x ,y is the coordinates of the mouse click place
            cv2.line(img=img2, pt1=pts[i], pt2=pts[i + 1], color=(255, 0, 0), thickness=2)

        cv2.line(img=img2, pt1=pts[0], pt2=pts[i + 1], color=(255, 0, 0), thickness=2)
        cv2.imshow('system', img2)

    @staticmethod
    def occupancy_counting(frame, mask):
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        occupancy_pixel = cv2.countNonZero(mask)
        all_pixel = frame.shape[0] * frame.shape[1]
        percentage = (occupancy_pixel / all_pixel) * 100
        percentage = round(percentage)
        percentage = str(percentage)

        return percentage

    @staticmethod
    def define_roi(frame):
        print("[INFO] Click the left button: select the point")
        print("[INFO] Click the right button: delete the last selected point")
        print("[INFO] Click the middle button: determine the ROI area")
        print("[INFO] Press ‘a’ to determine the selection area")
        print("[INFO] Press ESC to quit")

        while True:
            key = cv2.waitKey(1) & 0xFF
            # Create windows and bind windows to callback functions
            cv2.setMouseCallback('system', CrowdDetection.draw_roi, frame)

            if key == ord("a") and len(pts) >= 4:
                cv2.setMouseCallback('system', lambda *args: None)
                return True

            if key == 27:
                cv2.setMouseCallback('system', lambda *args: None)
                return False

    def draw_roi(self, x, y, flags, img):
        img2 = img.copy()

        if self == cv2.EVENT_LBUTTONDOWN and len(pts) <= 8:  # Left click, select point
            pts.append((x, y))

        if self == cv2.EVENT_RBUTTONDOWN:  # Right click to cancel the last selected point
            pts.pop()

        if len(pts) > 0:
            # Draw the last point in pts
            cv2.circle(img2, pts[-1], 3, (0, 0, 255), -1)

        if len(pts) > 1:
            for i in range(len(pts) - 1):
                cv2.circle(img2, pts[i], 5, (0, 0, 255), -1)  # x ,y is the coordinates of the mouse click place
                cv2.line(img=img2, pt1=pts[i], pt2=pts[i + 1], color=(255, 0, 0), thickness=2)

        cv2.imshow('system', img2)
