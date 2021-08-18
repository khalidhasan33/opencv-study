import cv2
import logging
import time

from notification import Notification
from datetime import datetime

starting_time_system = time.time()


class Report:

    @staticmethod
    def create_report(report_duration, interval, image_path, log_path, percentage, threshold, person_detected, frame):
        elapsed_time = time.time() - starting_time_system
        notification = Notification()
        if threshold < percentage:
            if report_duration <= elapsed_time:
                report_duration = elapsed_time + interval
                notification.send_notification()
                Report.save_crowd_image(image_path, frame)
                Report.write_log(log_path, percentage, person_detected)

        return report_duration

    @staticmethod
    def save_crowd_image(path, frame):
        ini_time_for_now = datetime.now().strftime("%Y%m%d-%H%M%S")
        ini_time_for_now = str(ini_time_for_now)
        filename = '/crowd-occurred-' + ini_time_for_now + '.jpg'
        path = path + filename
        status = cv2.imwrite(path, frame)
        # Debug
        # print("Image written to file-system : ", status)

    @staticmethod
    def write_log(log_path, occupancy, person_detected):
        ini_time_for_now = datetime.now().strftime("%Y%m%d-%H%M%S")
        ini_time_for_now = str(ini_time_for_now)
        filename = log_path + '/crowd-occurred-' + ini_time_for_now + '.log'
        log_message = "Warning!! Crowd occurred, Occupancy: " + str(occupancy) + \
                      "%, Person Detected: " + str(person_detected)

        # now we will Create and configure logger
        logging.basicConfig(filename=filename,
                            format='%(asctime)s %(message)s',
                            filemode='w')
        # Let us Create an object
        logger = logging.getLogger()
        # Now we are going to Set the threshold of logger to DEBUG
        logger.setLevel(logging.WARNING)
        logger.warning(log_message)
