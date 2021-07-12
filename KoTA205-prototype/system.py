import PySimpleGUI as sg

from detection import Detection
from user_interface import UserInterface


def define_threshold(layout):

    # Create the window and show it without the plot
    window = sg.Window("Main Window", layout)

    while True:
        event, values = window.read()

        if event == "-OK-":
            value = (values['-INPUT-'])
            try:
                threshold = int(value)
            except ValueError:
                print('Invalid, Input must be number')
                continue

            if threshold < 0:
                print("Sorry, your response must not be negative.")
                continue

            if threshold >= 100:
                print("Sorry, should be below or equal 100")
                continue
            else:
                window.close()
                return threshold

        if event == "Exit" or event == sg.WIN_CLOSED:
            window.close()
            threshold = 'exit'
            return threshold


def main():

    # Define class
    detection = Detection()
    user_interface = UserInterface()
    # Define var
    layout_crowd_detection = user_interface.layout_crowd_detection()
    layout_define_threshold = user_interface.layout_define_threshold()
    # Define threshold
    threshold = define_threshold(layout_define_threshold)
    # Crowd detection
    if not threshold == 'exit':
        detection.crowd_detection(threshold, layout_crowd_detection)

    print("Exit system")


if __name__ == "__main__":
    main()
