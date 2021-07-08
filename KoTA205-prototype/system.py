import cv2
import numpy as np

from crowd_detection import CrowdDetection, pts

# Path definition
video_path = r'C:\Users\User\Documents\Git\opencv-study\KoTA205-prototype\resource\nani.mp4'
yolo_weight_path = r'C:\Users\User\Documents\Git\opencv-study\KoTA205-prototype\yolo\yolov4-obj_3100.weights'
yolo_cfg_path = r'C:\Users\User\Documents\Git\opencv-study\KoTA205-prototype\yolo\yolo-v4-obj.cfg'
image_path = r'C:\Users\User\Documents\Git\opencv-study\KoTA205-prototype\crowd-image'
log_path = r'C:\Users\User\Documents\Git\opencv-study\KoTA205-prototype\crowd-log'
# Var definition
crowd = CrowdDetection
frame_id = 0
interval = 30
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

# Check if camera opened successfully
if video_cap.isOpened():
    # Input ROI
    threshold = input("Please defined the threshold you want? ")
    threshold = int(threshold)
else:
    print("Failed opening video stream or file")
# Read until video is completed
while video_cap.isOpened():
    ret, frame = video_cap.read()
    frame_id += 1

    if ret:
        # Var definition
        boxes = []
        key = cv2.waitKey(1) & 0xFF
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
        people = crowd.detection_object(net, output_layers, boxes, threshold_confident, frame_to_detect)
        # Draw object detected on mask
        crowd.draw_object_detected(boxes, people, mask)
        # Show FPS
        crowd.show_fps(frame_id, frame)

        if using_roi:
            mask = cv2.bitwise_and(mask2, mask)

        # Crowd counting
        percentage = crowd.occupancy_counting(mask, mask2)
        # Debug
        # print(percentage)
        # print(threshold)

        # Person counting
        person_detected = crowd.people_counting(people)
        # Display frame
        crowd.display_frame(using_roi, frame)
        # Create report
        report_duration = crowd.create_report(report_duration, interval, image_path, log_path, percentage,
                                              threshold, person_detected, frame)

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
