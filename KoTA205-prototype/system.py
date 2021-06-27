import cv2
import numpy as np
import time

from crowd_detection import CrowdDetection, pts

# Definition
video_path = "resource/video.mp4"
yolo_weight_path = "yolo/yolo-v4-obj.weights"
yolo_cfg_path = "yolo/yolo-v4-obj.cfg"

crowd = CrowdDetection
font = cv2.FONT_HERSHEY_PLAIN
frame_id = 0
starting_time = time.time()
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

# Check if camera opened successfully
if not video_cap.isOpened():
    print("Error opening video stream or file")

# Input ROI
threshold = input("Please defined the threshold you want? ")
# Read until video is completed
while video_cap.isOpened():
    ret, frame = video_cap.read()
    frame_id += 1

    if ret:
        # define
        boxes = []
        confidences = []
        height, width, channels = frame.shape
        key = cv2.waitKey(1) & 0xFF
        mask = np.zeros((frame.shape[0], frame.shape[1], 3), np.uint8)
        mask2 = np.zeros((frame.shape[0], frame.shape[1], 3), np.uint8)
        person_detected = 0

        if using_roi:
            points = np.array(pts, np.int32)
            points = points.reshape((-1, 1, 2))
            mask2 = cv2.fillPoly(mask.copy(), [points], (255, 255, 255))
            frame_roi = cv2.bitwise_and(mask2, frame)
            frame_to_detect = frame_roi
        else:
            frame_to_detect = frame

        # detecting objects reduce 416 to 320
        blob = cv2.dnn.blobFromImage(frame_to_detect, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        # Showing info on screen/ get confidence score of algorithm in detecting an object in blob
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > threshold_confident:
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

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.6)

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                confidence = confidences[i]
                cv2.rectangle(frame, (x, y), (x + w, y + h), 0, 2)
                cv2.rectangle(mask, (x, y), (x + w, y + h), (0, 0, 255), -1)
                person_detected += 1

        # Crowd counting
        percentage = crowd.occupancy_counting(mask, mask2)
        if percentage >= threshold:
            person_detected = str(person_detected)
            print('Overcrowd the occupancy is ' + percentage + '%, the person detected is ' + person_detected)

        # show FPS
        elapsed_time = time.time() - starting_time
        fps = frame_id / elapsed_time
        cv2.putText(frame, "FPS:" + str(round(fps, 2)), (10, 50), font, 2, (0, 0, 0), 1)

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
