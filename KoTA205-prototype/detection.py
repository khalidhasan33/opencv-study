import cv2
import numpy as np
import PySimpleGUI as sg

from counting import Counting
from display import Display
from frame_manipulation import FrameManipulation
from report import Report
from roi import Roi

# Path definition
video_path = r'C:\Users\User\Documents\Git\opencv-study\KoTA205-prototype\resource\nani.mp4'
yolo_weight_path = r'C:\Users\User\Documents\Git\opencv-study\KoTA205-prototype\yolo\yolov4-obj_final.weights'
yolo_cfg_path = r'C:\Users\User\Documents\Git\opencv-study\KoTA205-prototype\yolo\yolov4-obj.cfg'
image_path = r'C:\Users\User\Documents\Git\opencv-study\KoTA205-prototype\crowd-image'
log_path = r'C:\Users\User\Documents\Git\opencv-study\KoTA205-prototype\crowd-log'


class Detection:

    @staticmethod
    def crowd_detection(threshold, layout):

        # Class definition
        counting = Counting()
        display = Display()
        frame_manipulation = FrameManipulation()
        report = Report()
        roi = Roi()

        # Var definition
        create_roi = False
        frame_id = 0
        interval = 30
        is_box_active = False
        pts = []
        report_duration = 0
        threshold_confident = 0.05
        using_roi = False
        video_cap = cv2.VideoCapture(video_path)

        # Set Yolo
        net = cv2.dnn.readNet(yolo_weight_path, yolo_cfg_path)
        # Set CUDA usage
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        # Yolo Definition
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        # Set window
        window = sg.Window("Crowd detection system ", layout, size=(300, 350), resizable=False, finalize=True)

        # Read until video is completed
        while video_cap.isOpened():
            event, values = window.read(timeout=20)
            ret, frame = video_cap.read()
            frame_id += 1

            if ret:
                # Var definition
                boxes = []
                mask = np.zeros((frame.shape[0], frame.shape[1], 3), np.uint8)
                mask2 = np.zeros((frame.shape[0], frame.shape[1], 3), np.uint8)

                if using_roi:
                    points = np.array(pts, np.int32)
                    points = points.reshape((-1, 1, 2))
                    mask2 = cv2.fillPoly(mask.copy(), [points], (255, 255, 255))
                    frame_roi = cv2.bitwise_and(mask2, frame)
                    frame_to_detect = frame_roi
                else:
                    mask2[:] = (255, 255, 255)
                    frame_to_detect = frame

                # Detection object
                people = Detection.detection_object(net, output_layers, boxes, threshold_confident, frame_to_detect)
                # Draw object detected on mask
                frame_manipulation.draw_object_detected(boxes, people, mask)

                if using_roi:
                    mask = cv2.bitwise_and(mask2, mask)

                # Crowd counting
                percentage = counting.occupancy_counting(mask, mask2)

                # Person counting
                person_detected = counting.people_counting(people)

                # Draw bounding box
                if is_box_active:
                    frame_manipulation.draw_bounding_box(boxes, people, frame)

                # Define ROI
                if create_roi:
                    using_roi = roi.define_roi(window, pts, frame, percentage, person_detected)
                    create_roi = not create_roi

                # Show FPS
                display.show_fps(frame_id, frame)

                # Display frame
                display.display_frame(using_roi, pts, frame)
                # Create report
                report_duration = report.create_report(report_duration, interval, image_path, log_path, percentage,
                                                       threshold, person_detected, frame)

                # Window update
                window["-CROWD1-"].update(value=person_detected)
                window["-OCCUPY1-"].update(value=percentage)

            else:
                break

            # Display frame
            if event == '-BOUND-':
                is_box_active = not is_box_active

            # Create ROI (hide button)
            if event == '-CREATE-':
                create_roi = not create_roi

            if event == '-EXIT-':
                break

        video_cap.release()
        cv2.destroyAllWindows()

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
