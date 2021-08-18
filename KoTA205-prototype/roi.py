import cv2


class Roi:

    @staticmethod
    def define_roi(window, pts, frame, percentage, person_detected, threshold):
        window.Element('-FINISH-').Update(visible=True)
        window["-OCCUPY1-"].update(value='-')
        window["-CROWD1-"].update(value='-')
        window["-THRESHOLD1-"].update(value='-')
        window.Element('-CREATE-').Update(visible=False)
        window.Element('-BOUND-').Update(visible=False)
        window.Element('-EXIT-').Update(visible=False)
        window.Element('-RESET-').Update(visible=True)

        while True:
            event = window.read(timeout=20)
            status_roi = str(event)
            # Create windows and bind windows to callback functions
            cv2.setMouseCallback('Video', Roi.select_roi, pts)
            Roi.draw_roi(pts, frame)

            if status_roi == "('-FINISH-', {})" and (len(pts) >= 4 or len(pts) == 0):
                window.Element('-FINISH-').Update(visible=False)
                window["-OCCUPY1-"].update(value=percentage)
                window["-CROWD1-"].update(value=person_detected)
                window["-THRESHOLD1-"].update(value=threshold)
                window.Element('-CREATE-').Update(visible=True)
                window.Element('-BOUND-').Update(visible=True)
                window.Element('-EXIT-').Update(visible=True)
                window.Element('-RESET-').Update(visible=False)
                cv2.setMouseCallback('system', lambda *args: None)

                if len(pts) > 0:
                    return True
                    break
                else:
                    return False

            if status_roi == "('-RESET-', {})":
                pts.clear()
                cv2.imshow('Video', frame)

    @staticmethod
    def draw_roi(pts, frame):
        img2 = frame.copy()

        if len(pts) > 0:
            # Draw the last point in pts
            cv2.circle(img2, pts[-1], 3, (0, 0, 255), -1)

        if len(pts) > 1:
            for i in range(len(pts) - 1):
                cv2.circle(img2, pts[i], 5, (0, 0, 255), -1)  # x ,y is the coordinates of the mouse click place
                cv2.line(img=img2, pt1=pts[i], pt2=pts[i + 1], color=(255, 0, 0), thickness=2)

        cv2.imshow('Video', img2)

    def select_roi(self, x, y, flags, pts):

        if self == cv2.EVENT_LBUTTONDOWN and len(pts) < 8:  # Left click, select point
            pts.append((x, y))

        if self == cv2.EVENT_RBUTTONDOWN and len(pts) > 0:  # Right click to cancel the last selected point
            pts.pop()
