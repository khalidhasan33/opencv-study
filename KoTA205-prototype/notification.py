from win10toast import ToastNotifier


class Notification:

    @staticmethod
    def send_notification():
        toaster = ToastNotifier()
        toast_title = "Warning!!"
        toast_description = "System detects the occurrence of crowd"
        toaster.show_toast(toast_title, toast_description, icon_path=None, duration=10, threaded=True)
