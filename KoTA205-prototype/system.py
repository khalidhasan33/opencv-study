import cv2
import numpy as np
import PySimpleGUI as sg

from crowd_detection import CrowdDetection, pts


# Path definition
video_path = r'C:\Users\Wangoo\source\repos\opencv-study\KoTA205-prototype\resource\videoplayback.mp4'
yolo_weight_path = r'C:\Users\Wangoo\source\repos\opencv-study\KoTA205-prototype\yolo\yolo-obj_1000.weights'
yolo_cfg_path = r'C:\Users\Wangoo\source\repos\opencv-study\KoTA205-prototype\yolo\yolov4.cfg'
image_path = r'C:\Users\Wangoo\source\repos\opencv-study\KoTA205-prototype\crowd-image'
log_path = r'C:\Users\Wangoo\source\repos\opencv-study\KoTA205-prototype\crowd-log'



def crowd_detection():

    # Var definition
    crowd = CrowdDetection
    frame_id = 0
    interval = 30
    report_duration = 0

    threshold_confident = 0.05
    using_roi = False
    video_cap = cv2.VideoCapture(video_path)
    
    sg.theme("DarkGrey")

    col1 = sg.Text("Occupancy : ", key="-OCCUP-")
    col2 = sg.Text("Crowd Estimation : ", key="-CROWD-")
    btn1 = sg.Button("Create ROI",button_color=('black', 'white'), size=(10, 1), key="-CREATE-", visible=True)
    btn2 = sg.Button("Finish Create ROI",button_color=('black', 'white'), size=(15, 1), key="-FINISH-", visible=False)

    # Define the window layout
    layout = [
        [sg.Column([[col1]]), sg.Column([[col2]]), sg.Column([[btn1, btn2]])],
        [sg.Column([[sg.Image(key="-IMAGE-")]], justification='center')],
        [sg.Button("Exit",button_color=('black', 'white'), size=(10, 1))],
    ]

    print ('layout jalan')
    
    # Create the window and show it without the plot
    window = sg.Window("Nama Sistem", layout, resizable=True, finalize=True)
    window.Maximize()

    video_cap = cv2.VideoCapture(video_path)

    print ('video cap jalan')
    
    # Set Yolo
    net = cv2.dnn.readNet(yolo_weight_path, yolo_cfg_path)
    # Set CUDA usage
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    # Yolo Definition
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    print ('yolo jalan')

#    Check if camera opened successfully
#    if video_cap.isOpened():
#        # Input ROI
#        threshold = input("Please defined the threshold you want? ")
#        threshold = int(threshold)
#    else:
#        print("Failed opening video stream or file")
    # Read until video is completed
    
    while video_cap.isOpened():
        event, values = window.read(timeout=20)
        if event in(None, 'Exit'):
            break
        

        ret, frame = video_cap.read()
        frame_id += 1

        if ret == True:
            # Var definition
            boxes = []
            key = cv2.waitKey(1) & 0xFF
            mask = np.zeros((frame.shape[0], frame.shape[1], 3), np.uint8)
            mask2 = np.zeros((frame.shape[0], frame.shape[1], 3), np.uint8)

            # Resize Video
            frame = cv2.resize(frame,(1600, 900),fx=0,fy=0, interpolation = None)

            print ('renew jalan')
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

            print ('people jalan')
            # Draw object detected on mask
            crowd.draw_object_detected(boxes, people, mask)
            print ('crowd draw jalan')
            # Show FPS
            crowd.show_fps(frame_id, frame)
            print ('crowd jalan')

            
            if using_roi:
                mask = cv2.bitwise_and(mask2, mask)

            # Crowd counting
            percentage = crowd.occupancy_counting(mask, mask2)

            print ('percentage jalan')
            # Debug
            # print(percentage)
            # print(threshold)

            # Person counting
            person_detected = crowd.people_counting(people)
            # Display frame
            frame = crowd.display_frame(using_roi, frame)
            crowd.draw_bounding_box(boxes, people, frame)
            #crowd.display_frame(using_roi, frame)
            # Create report
            #report_duration = crowd.create_report(report_duration, interval, image_path, log_path, percentage,
            #                                  threshold, person_detected, frame)
            
            if event == '-CREATE-':
                window.Element('-FINISH-').Update(visible=True)
                window.Element('-OCCUP-').Update(visible=False)
                window.Element('-CROWD-').Update(visible=False)
                window.Element('-CREATE-').Update(visible=False)
                using_roi = crowd.define_roi(frame)

            if event == '-FINISH-':
                window.Element('-FINISH-').Update(visible=False)
                window.Element('-OCCUP-').Update(visible=True)
                window.Element('-CROWD-').Update(visible=True)
                window.Element('-CREATE-').Update(visible=True)

            # Press a on keyboard to create ROI
            #if key == ord("a"):
            #    using_roi = crowd.define_roi(frame)
            # Press Esc on keyboard to  exit
            #if key == 27:
            #    break
            # Press Exit Button
            if event == "Exit" or event == sg.WIN_CLOSED:
                break

        #imgbytes = cv2.imshow('system', frame)
        imgbytes = cv2.imencode(".png", frame)[1].tobytes()
        window["-IMAGE-"].update(data=imgbytes)

    window.close()

    # When everything done, release the video capture object


def main():
    layout = [
        [sg.Text("Input Threshold", justification='center')],
        [sg.InputText(justification='center', key='-THRS-')],
        [sg.Button("OK", button_color=('black', 'white'), size=(10, 1), key="-OK-"), 
         sg.Button("Exit",button_color=('black', 'white'), size=(10, 1))],
    ]

    # Create the window and show it without the plot
    window = sg.Window("Main Window", layout)
    
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "-OK-":
            value = (values['-THRS-'])
            if value == '':
                print('Invalid, Input must be number')
            else:
                try:
                    threshold = int(value)
                    if threshold < 0:
                        threshold = abs(threshold)
                    print(threshold)
                    window.close()
                    crowd_detection()
                except:
                    print('Invalid, Input must be number')

    window.close()

if __name__ == "__main__":
    main()
