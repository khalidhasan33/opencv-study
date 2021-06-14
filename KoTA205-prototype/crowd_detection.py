import cv2
import joblib
import numpy as np

pts = []  # for storing points


class CrowdDetection:
    def draw_roi(self, x, y, flags, img):
        img2 = img.copy()

        if self == cv2.EVENT_LBUTTONDOWN:  # Left click, select point
            pts.append((x, y))

        if self == cv2.EVENT_RBUTTONDOWN:  # Right click to cancel the last selected point
            pts.pop()

        if self == cv2.EVENT_MBUTTONDOWN:
            mask = np.zeros(img.shape, np.uint8)
            points = np.array(pts, np.int32)
            points = points.reshape((-1, 1, 2))

            mask = cv2.polylines(mask, [points], True, (255, 255, 255), 2)
            mask2 = cv2.fillPoly(mask.copy(), [points], (255, 255, 255))  # for ROI
            mask3 = cv2.fillPoly(mask.copy(), [points], (0, 255, 0))  # for displaying images on the desktop

            show_image = cv2.addWeighted(src1=img, alpha=0.8, src2=mask3, beta=0.2, gamma=0)

            cv2.imshow("mask", mask2)
            cv2.imshow("show_img", show_image)

            roi = cv2.bitwise_and(mask2, img)
            cv2.imshow("ROI", roi)

            cv2.waitKey(0)

        if len(pts) > 0:
            # Draw the last point in pts
            cv2.circle(img2, pts[-1], 3, (0, 0, 255), -1)

        if len(pts) > 1:
            for i in range(len(pts) - 1):
                cv2.circle(img2, pts[i], 5, (0, 0, 255), -1)  # x ,y is the coordinates of the mouse click place
                cv2.line(img=img2, pt1=pts[i], pt2=pts[i + 1], color=(255, 0, 0), thickness=2)

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
