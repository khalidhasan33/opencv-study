import PySimpleGUI as sg


class UserInterface:

    @staticmethod
    def layout_define_threshold():
        layout = [
            [sg.Text("Input Threshold (%)", justification='center')],
            [sg.InputText(justification='center', key='-INPUT-')],
            [sg.Column([[sg.Button("OK", button_color=('black', 'white'), size=(10, 1), key="-OK-"),
                         sg.Button("Exit", button_color=('black', 'white'), size=(10, 1))]], justification='center')],
        ]
        return layout

    @staticmethod
    def layout_crowd_detection():
        # GUI Layout
        sg.theme("DarkGrey")
        col1 = sg.Text("Threshold (%)       : ", key="-THRESHOLD-")
        col2 = sg.Text("", key="-THRESHOLD1-", size=(3, 1))
        col3 = sg.Text("Occupancy (%)       : ", key="-OCCUPY-")
        col4 = sg.Text("", key="-OCCUPY1-", size=(3, 1))
        col5 = sg.Text("Crowd Estimation    : ", key="-CROWD-")
        col6 = sg.Text("", key="-CROWD1-", size=(3, 1))
        btn1 = sg.Button("Create ROI", button_color=('black', 'white'), size=(10, 1), key="-CREATE-", visible=True)
        btn2 = sg.Button("Finish Create ROI", button_color=('black', 'white'), size=(15, 1), key="-FINISH-",
                         visible=False)
        btn3 = sg.Button("Bounding Box", button_color=('black', 'white'), size=(10, 1), key="-BOUND-", visible=True)
        btn4 = sg.Button("Reset ROI", button_color=('black', 'white'), size=(10, 1), key="-RESET-", visible=False)
        btn5 = sg.Button("Exit", button_color=('black', 'white'), size=(10, 1), key="-EXIT-", visible=True)

        # Define the window layout
        layout = [
            [sg.Column([[col1]]), sg.Column([[col2]])],
            [sg.Column([[col3]]), sg.Column([[col4]])],
            [sg.Column([[col5]]), sg.Column([[col6]])],
            [sg.Column([[btn1, btn2]]), sg.Column([[btn3, btn4]])],
            [sg.Column([[sg.Text("", size=(1, 10))]])],
            [sg.Column([[btn5]])],
        ]
        return layout
