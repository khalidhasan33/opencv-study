import PySimpleGUI as sg
import cv2
import numpy as np

def detect():

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

    # Create the window and show it without the plot
    window = sg.Window("Nama Sistem", layout, resizable=True, finalize=True)
    window.Maximize()

    cap = video_cap

    while True:
        event, values = window.read(timeout=20)
        if event in(None, 'Exit'):
            break
        if event == '-CREATE-':
            window.Element('-FINISH-').Update(visible=True)
            window.Element('-OCCUP-').Update(visible=False)
            window.Element('-CROWD-').Update(visible=False)
            window.Element('-CREATE-').Update(visible=False)

        if event == '-FINISH-':
            window.Element('-FINISH-').Update(visible=False)
            window.Element('-OCCUP-').Update(visible=True)
            window.Element('-CROWD-').Update(visible=True)
            window.Element('-CREATE-').Update(visible=True)

        ret, frame = cap.read()
        if ret == True:
            renew = cv2.resize(frame,(1600, 900),fx=0,fy=0, interpolation = None)

        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        imgbytes = cv2.imencode(".png", renew)[1].tobytes()
        window["-IMAGE-"].update(data=imgbytes)

    window.close()

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
                    detect()
                except:
                    print('Invalid, Input must be number')

    window.close()

if __name__ == "__main__":
    main()
