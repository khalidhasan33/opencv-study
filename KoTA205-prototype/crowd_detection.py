import cv2
import time
import numpy as np
import logging

from datetime import datetime

from win10toast import ToastNotifier

pts = []  # for storing points
starting_time_system = time.time()


class CrowdDetection:

    @staticmethod
    def create_report(report_duration, interval, image_path, log_path, percentage, threshold, person_detected, frame):
        elapsed_time = time.time() - starting_time_system
        if threshold < percentage:
            if report_duration <= elapsed_time:
                report_duration = elapsed_time + interval
                CrowdDetection.send_notification()
                CrowdDetection.save_crowd_image(image_path, frame)
                CrowdDetection.write_log(log_path, percentage, person_detected)

        return report_duration

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

            if key == ord("a") and (len(pts) >= 4 or len(pts) == 0):
                cv2.setMouseCallback('system', lambda *args: None)
                if len(pts) > 0:
                    return True
                else:
                    return False

            if key == 27:
                cv2.setMouseCallback('system', lambda *args: None)
                return False

    @staticmethod
    def detection_object(net, output_layers, boxes, threshold, frame):
        confidences = []
        height, width, channels = frame.shape

        # detecting objects reduce 416 to 320
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        # Showing info on screen/ get confidence score of algorithm in detecting an object in blob
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > threshold:
                    # object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    # put all rectangle areas
                    boxes.append([x, y, w, h])
                    # how confidence was that object detected and show that percentage
                    confidences.append(float(confidence))

        people = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.6)
        return people

    @staticmethod
    def display_frame(using_roi, img):
        img_show = img.copy()
        if using_roi:
            # Draw line ROI
            for i in range(len(pts) - 1):
                cv2.circle(img_show, pts[i], 5, (0, 0, 255), -1)  # x ,y is the coordinates of the mouse click place
                cv2.line(img=img_show, pt1=pts[i], pt2=pts[i + 1], color=(255, 0, 0), thickness=2)

            cv2.line(img=img_show, pt1=pts[0], pt2=pts[i + 1], color=(255, 0, 0), thickness=2)

        return img_show

    @staticmethod
    def draw_bounding_box(boxes, people, frame):
        for i in range(len(boxes)):
            if i in people:
                x, y, w, h = boxes[i]
                cv2.rectangle(frame, (x, y), (x + w, y + h), 0, 2)

    @staticmethod
    def draw_object_detected(boxes, people, mask):
        for i in range(len(boxes)):
            if i in people:
                x, y, w, h = boxes[i]
                cv2.rectangle(mask, (x, y), (x + w, y + h), (0, 0, 255), -1)

    def draw_roi(self, x, y, flags, img):
        img2 = img.copy()

        if self == cv2.EVENT_LBUTTONDOWN and len(pts) <= 8:  # Left click, select point
            pts.append((x, y))

        if self == cv2.EVENT_RBUTTONDOWN and len(pts) > 0:  # Right click to cancel the last selected point
            pts.pop()

        if len(pts) > 0:
            # Draw the last point in pts
            cv2.circle(img2, pts[-1], 3, (0, 0, 255), -1)

        if len(pts) > 1:
            for i in range(len(pts) - 1):
                cv2.circle(img2, pts[i], 5, (0, 0, 255), -1)  # x ,y is the coordinates of the mouse click place
                cv2.line(img=img2, pt1=pts[i], pt2=pts[i + 1], color=(255, 0, 0), thickness=2)

        imgbytes = cv2.imencode(".png", img2)[1].tobytes()
        window["-IMAGE-"].update(data=imgbytes)
        #cv2.imshow('system', img2)

    @staticmethod
    def occupancy_counting(mask, mask2):
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        mask2 = cv2.cvtColor(mask2, cv2.COLOR_BGR2GRAY)
        occupancy_pixel = cv2.countNonZero(mask)
        all_pixel = cv2.countNonZero(mask2)
        percentage = (occupancy_pixel / all_pixel) * 100
        percentage = round(percentage)
        # Debug
        # print(occupancy_pixel)
        # print(all_pixel)

        return percentage

    @staticmethod
    def people_counting(people):
        person_detected = len(people)
        return person_detected

    @staticmethod
    def save_crowd_image(path, frame):
        ini_time_for_now = datetime.now().strftime("%Y%m%d-%H%M%S")
        ini_time_for_now = str(ini_time_for_now)
        filename = '/crowd-occurred-' + ini_time_for_now + '.jpg'
        path = path + filename
        status = cv2.imwrite(path, frame)
        # Debug
        # print("Image written to file-system : ", status)

    @staticmethod
    def send_notification():
        toaster = ToastNotifier()
        toast_title = "Warning!!"
        toast_description = "System detects the occurrence of crowd"
        toaster.show_toast(toast_title, toast_description)

    @staticmethod
    def show_fps(frame_id, frame):
        font = cv2.FONT_HERSHEY_PLAIN
        elapsed_time_fps = time.time() - starting_time_system
        fps = frame_id / elapsed_time_fps
        cv2.putText(frame, "FPS:" + str(round(fps, 2)), (10, 50), font, 2, (0, 0, 0), 1)

    @staticmethod
    def write_log(log_path, occupancy, person_detected):
        ini_time_for_now = datetime.now().strftime("%Y%m%d-%H%M%S")
        ini_time_for_now = str(ini_time_for_now)
        filename = log_path + '/crowd-occurred-' + ini_time_for_now + '.log'
        log_message = "Warning!! Crowd occurred, Occupancy: " + str(occupancy) + \
                      "%, Person Detected: " + str(person_detected)

        # now we will Create and configure logger
        logging.basicConfig(filename=filename,
                            format='%(asctime)s %(message)s',
                            filemode='w')
        # Let us Create an object
        logger = logging.getLogger()
        # Now we are going to Set the threshold of logger to DEBUG
        logger.setLevel(logging.DEBUG)
        logger.warning(log_message)
