import cv2
import time

starting_time_system = time.time()


class Display:

    @staticmethod
    def display_frame(using_roi, pts, frame):
        frame_show = frame.copy()
        if using_roi:
            # Draw line ROI
            for i in range(len(pts) - 1):
                cv2.circle(frame_show, pts[i], 5, (0, 0, 255), -1)  # x ,y is the coordinates of the mouse click place
                cv2.line(img=frame_show, pt1=pts[i], pt2=pts[i + 1], color=(255, 0, 0), thickness=2)

            cv2.line(img=frame_show, pt1=pts[0], pt2=pts[i + 1], color=(255, 0, 0), thickness=2)

        cv2.imshow('system', frame_show)

    @staticmethod
    def show_fps(frame_id, frame):
        font = cv2.FONT_HERSHEY_PLAIN
        elapsed_time_fps = time.time() - starting_time_system
        fps = frame_id / elapsed_time_fps
        cv2.putText(frame, "FPS:" + str(round(fps, 2)), (10, 50), font, 2, (0, 0, 0), 1)
