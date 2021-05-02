# Python program to illustrate
# arithmetic operation of
# addition of two images

# organizing imports
import cv2
import numpy as np

# path to input images are specified and
# images are loaded with imread command
image1 = cv2.imread('input1.jpeg')
image2 = cv2.imread('input2.jpeg')

# cv2.addWeighted is applied over the
# Syntax: cv2.addWeighted(img1, wt1, img2, wt2, gammaValue)
# Parameters:
# img1: First Input Image array(Single-channel, 8-bit or floating-point)
# wt1: Weight of the first input image elements to be applied to the final image
# img2: Second Input Image array(Single-channel, 8-bit or floating-point)
# wt2: Weight of the second input image elements to be applied to the final image
# gammaValue: Measurement of light
weightedSum = cv2.addWeighted(image1, 0.5, image2, 0.9, 1)

# the window showing output image
# with the weighted sum
cv2.namedWindow('arithmetic-additional', cv2.WINDOW_NORMAL)
cv2.imshow('WeightedImage', weightedSum)

# De-allocate any associated memory usage
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()
