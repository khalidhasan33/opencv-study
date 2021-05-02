# Python program to illustrate
# arithmetic operation of
# subtraction of pixels of two images

# organizing imports
import cv2
import numpy as np

# path to input images are specified and
# images are loaded with imread command
image1 = cv2.imread('input1.jpeg')
image2 = cv2.imread('input2.jpeg')
image3 = cv2.imread('input3.jpeg')
image4 = cv2.imread('input4.jpeg')

# cv2.subtract is applied over the
# image inputs with applied parameters
sub1 = cv2.subtract(image1, image2)
sub2 = cv2.subtract(image3, image4)

# the window showing output image
# with the subtracted image
cv2.imshow('Subtracted Image 1', sub1)
cv2.imshow('Subtracted Image 2', sub2)

# De-allocate any associated memory usage
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()
