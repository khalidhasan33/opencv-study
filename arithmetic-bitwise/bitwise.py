# Python program to illustrate
# arithmetic operation of
# bitwise AND of two images

# organizing imports
import cv2
import numpy as np

# path to input images are specified and
# images are loaded with imread command
image1 = cv2.imread('input1.png')
image2 = cv2.imread('input2.png')

# cv2.bitwise_and is applied over the
# image inputs with applied parameters
des_and = cv2.bitwise_and(image2, image1, mask=None)

# cv2.bitwise_or is applied over the
# image inputs with applied parameters
des_or = cv2.bitwise_or(image2, image1, mask=None)

# cv2.bitwise_xor is applied over the
# image inputs with applied parameters
des_xor = cv2.bitwise_xor(image2, image1, mask=None)

# font
font = cv2.FONT_HERSHEY_SIMPLEX
org = (25, 30)
fontScale = 1
color = (255, 0, 0)
thickness = 2
# give name on the image
des_and = cv2.putText(des_and, 'AND Bitwise', org, font,
                      fontScale, color, thickness, cv2.LINE_AA)
des_or = cv2.putText(des_or, 'OR Bitwise', org, font,
                     fontScale, color, thickness, cv2.LINE_AA)
des_xor = cv2.putText(des_xor, 'XOR Bitwise', org, font,
                      fontScale, color, thickness, cv2.LINE_AA)

# the window showing output image
# with the Bitwise AND operation
# on the input images
cv2.namedWindow('arithmetic-bitwise', cv2.WINDOW_NORMAL)
cv2.imshow('image1', des_and)
cv2.imshow('image2', des_or)
cv2.imshow('image3', des_xor)

# De-allocate any associated memory usage
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()
