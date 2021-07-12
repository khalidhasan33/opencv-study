import cv2


class Counting:

    @staticmethod
    def occupancy_counting(mask, mask2):
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        mask2 = cv2.cvtColor(mask2, cv2.COLOR_BGR2GRAY)
        occupancy_pixel = cv2.countNonZero(mask)
        all_pixel = cv2.countNonZero(mask2)
        percentage = (occupancy_pixel / all_pixel) * 100
        percentage = round(percentage)
        # Debug
        # print(occupancy_pixel)
        # print(all_pixel)

        return percentage

    @staticmethod
    def people_counting(people):
        person_detected = len(people)
        return person_detected
