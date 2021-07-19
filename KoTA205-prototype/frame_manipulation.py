import cv2


class FrameManipulation:

    @staticmethod
    def draw_bounding_box(boxes, confidences, people, frame):
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in people:
                x, y, w, h = boxes[i]
                confidence = confidences[i]
                cv2.rectangle(frame, (x, y), (x + w, y + h), 0, 2)
                cv2.putText(frame, "Confidence " + str(round(confidence, 2)), (x, y + 30), font, 1, (255, 255, 255), 2)

    @staticmethod
    def draw_object_detected(boxes, people, mask):
        for i in range(len(boxes)):
            if i in people:
                x, y, w, h = boxes[i]
                cv2.rectangle(mask, (x, y), (x + w, y + h), (0, 0, 255), -1)
