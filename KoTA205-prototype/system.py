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

def crowd_detection(threshold):

    # Var definition
    crowd = CrowdDetection
    frame_id = 0
    interval = 30
    report_duration = 0
    is_box_active = False
    create_roi = False

    threshold_confident = 0.05
    using_roi = False
    video_cap = cv2.VideoCapture(video_path)

    # GUI Layout
    sg.theme("DarkGrey")

    col1 = sg.Text("Occupancy (%)       : ", key="-OCCUP-") 
    col2 = sg.Text("", key="-OCCUP1-", size=(3,1))
    col3 = sg.Text("Crowd Estimation    : ", key="-CROWD-") 
    col4 = sg.Text("", key="-CROWD1-", size=(3,1))
    btn1 = sg.Button("Create ROI",button_color=('black', 'white'), size=(10, 1), key="-CREATE-", visible=True)
    btn2 = sg.Button("Finish Create ROI",button_color=('black', 'white'), size=(15, 1), key="-FINISH-", visible=False)
    btn3 = sg.Button("Bounding Box",button_color=('black', 'white'), size=(10, 1), key="-BOUND-", visible=True)
    btn4 = sg.Button("Reset ROI",button_color=('black', 'white'), size=(10, 1), key="-RESET-", visible=False)
    btn5 = sg.Button("Exit",button_color=('black', 'white'), size=(10, 1), key="-EXIT-", visible=True)

    # Define the window layout
    layout = [
        [sg.Column([[col1]]), sg.Column([[col2]])],
        [sg.Column([[col3]]), sg.Column([[col4]])],
        [sg.Column([[btn1, btn2]]), sg.Column([[btn3, btn4]])],
        [sg.Column([[sg.Text("", size=(1, 10))]])],
        [sg.Column([[btn5]])],
    ]

    window = sg.Window("Nama Sistem", layout, size=(300, 350), resizable=True, finalize=True)

    # Set Yolo
    net = cv2.dnn.readNet(yolo_weight_path, yolo_cfg_path)
    # Set CUDA usage
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    # Yolo Definition
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # Read until video is completed
    while video_cap.isOpened():
        event, values = window.read(timeout=20)
        if event in(None, 'Exit'):
            break
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
            window["-OCCUP1-"].update(value=percentage)
            # Debug
            # print(percentage)
            # print(threshold)

            # Person counting
            person_detected = crowd.people_counting(people)
            window["-CROWD1-"].update(value=person_detected)
            
            # Display frame
            if event == '-BOUND-':
                is_box_active = not is_box_active
                
            if is_box_active == True:
                crowd.draw_bounding_box(boxes, people, frame)
                

            crowd.display_frame(using_roi, frame)
            # Create report
            report_duration = crowd.create_report(report_duration, interval, image_path, log_path, percentage,
                                                  threshold, person_detected, frame)

            # Create ROI (hide button)
            if event == '-CREATE-':
                create_roi = not create_roi
            
            if create_roi == True:
                window.Element('-FINISH-').Update(visible=True)
                window["-OCCUP1-"].update(value='-')
                window["-CROWD1-"].update(value='-')
                window.Element('-CREATE-').Update(visible=False)
                window.Element('-BOUND-').Update(visible=False)
                window.Element('-EXIT-').Update(visible=False)
                window.Element('-RESET-').Update(visible=True)
                while True:
                    event = window.read(timeout=20)
                    print (create_roi)
                    #key = cv2.waitKey(1) & 0xFF
                    # Create windows and bind windows to callback functions
                    cv2.setMouseCallback('system', CrowdDetection.draw_roi, frame)
                    #print("mouse callback")

                    status_roi = str(event)

                    if status_roi == "('-FINISH-', {})" and (len(pts) >= 4 or len(pts) == 0):
                        create_roi = not create_roi
                        print("finsih ditekan")

                    #if create_roi == False:
                        window.Element('-FINISH-').Update(visible=False)
                        window["-OCCUP1-"].update(value=percentage)
                        window["-CROWD1-"].update(value=person_detected)
                        window.Element('-CREATE-').Update(visible=True)
                        window.Element('-BOUND-').Update(visible=True)
                        window.Element('-EXIT-').Update(visible=True)
                        window.Element('-RESET-').Update(visible=False)

                        cv2.setMouseCallback('system', lambda *args: None)
                        if len(pts) > 0:
                            using_roi = True
                            print("using ROI true")
                            break
                        else:
                            using_roi = False
                            print("using ROI false")
                            break
                            
                    if status_roi == "('-RESET-', {})":
                        pts.clear()

            if event == '-EXIT-':
                break

        else:
            break
    video_cap.release()
    cv2.destroyAllWindows()


def main():
    layout = [
        [sg.Text("Input Threshold (%)", justification='center')],
        [sg.InputText(justification='center', key='-INPUT-')],
        [sg.Column([[sg.Button("OK", button_color=('black', 'white'), size=(10, 1), key="-OK-"), sg.Button("Exit",button_color=('black', 'white'), size=(10, 1))]], justification='center')],
    ]

    # Create the window and show it without the plot
    window = sg.Window("Main Window", layout)
    
    while True:
        event, values = window.read()
        key = cv2.waitKey(1) & 0xFF
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "-OK-" or key == 27:
            value = (values['-INPUT-'])
            if value == '':
                print('Invalid, Input must be number')
            else:
                #try:
                    threshold = int(value)
                    if threshold > 100:
                        print('Invalid, Input must be less than 100')
                    else:
                        if threshold < 0:
                            threshold = abs(threshold)
                        print(threshold)
                        window.close()
                        crowd_detection(threshold)
                #except ValueError:
                #    print('Invalid, Input must be number')

    window.close()

if __name__ == "__main__":
    main()
# When everything done, release the video capture object

