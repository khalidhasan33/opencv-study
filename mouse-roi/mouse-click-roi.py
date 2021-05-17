import cv2
import imutils

img = cv2.imread('image.png')
img = imutils.resize(img, width=500)

roi = cv2.selectROI(windowName="roi", img=img, showCrosshair=True, fromCenter=False)
x, y, w, h = roi

cv2.rectangle(img=img, pt1=(x, y), pt2=(x + w, y + h), color=(0, 0, 255), thickness=2)
cv2.imshow("roi", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
