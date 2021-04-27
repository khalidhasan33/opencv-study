# Importing the OpenCV library
import cv2

# Reading the image
image = cv2.imread('image.jpg')

# Extracting the height and width of an image
h, w = image.shape[:2]
print("Displays the image height and width values")
print("Height = {},  Width = {}".format(h, w))
print("=====================================")

# Extracting RGB values.
# Here we have randomly chosen a pixel
# by passing in 100, 100 for height and width.
(B, G, R) = image[100, 100]
print("Displays RGB value of specific pixel")
print("R = {}, G = {}, B = {}".format(R, G, B))

# We can also pass the channel to extract
# the value for a specific channel
B = image[100, 100, 0]
print("B = {}".format(B))
print("=====================================")

# We will calculate the region of interest
# by slicing the pixels of the image
roi = image[100: 300, 200: 250]

# resize() function takes 2 parameters,
# the image and the dimensions
resize = cv2.resize(image, (800, 800))

# Calculating the ratio
ratio = 400 / w
# Creating a tuple containing width and height
dim = (800, int(h * ratio))
# Resizing the image
resize_aspect = cv2.resize(image, dim)

# Calculating the center of the image
center = (w // 2, h // 2)
# Generating a rotation matrix (3 argument -> center, angle, scale)
matrix = cv2.getRotationMatrix2D(center, -45, 1.0)
# Performing the affine transformation
rotated = cv2.warpAffine(image, matrix, (w, h))

# We are copying the original image,
# as it is an in-place operation.
output = image.copy()
# Start coordinate, here (5, 5)
# represents the top left corner of rectangle
start_point = (5, 5)
# Ending coordinate, here (220, 220)
# represents the bottom right corner of rectangle
end_point = (220, 220)
# Blue color in BGR
color = (255, 0, 0)
# Line thickness of 2 px
thickness = 2
# Using the rectangle() function to create a rectangle.
rectangle = cv2.rectangle(output, start_point,
                          end_point, color, thickness)

output_with_font = image.copy()
# font
font = cv2.FONT_HERSHEY_SIMPLEX
# org
org = (50, 50)
# fontScale
fontScale = 1
# Blue color in BGR
color = (255, 0, 0)
# Line thickness of 2 px
thickness = 2
# Using cv2.putText() method
image_with_font = cv2.putText(output_with_font, 'OpenCV', org, font,
                              fontScale, color, thickness, cv2.LINE_AA)

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.imshow('image', image_with_font)
cv2.waitKey(0)
cv2.destroyAllWindows()
