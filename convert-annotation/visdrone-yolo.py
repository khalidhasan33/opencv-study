import os
import glob
import cv2

source_directory = r'D:\VisDrone2019-DET-train\images'

image_filenames = glob.glob(os.path.join(source_directory, '*.jpg'))
for img_name in image_filenames:
    annotation_name = img_name.replace('.jpg', '.txt')
    img = cv2.imread(img_name, cv2.IMREAD_COLOR)
    height, width, chance = img.shape
    # read the initial lines in the txt
    with open(annotation_name, 'r') as f:
        annotations = f.read().strip().split('\n')
    # split them on commas ','
    annotations = [x.split(',') for x in annotations]
    with open(annotation_name.replace('.txt', '_yolo.txt'), 'w') as f:
        for ann in annotations:
            x_min, y_min, x_width, y_height, score, cat, trunc, occ = ann
            x_ctr = (int(x_min) + (int(x_width) / 2)) / width
            y_ctr = (int(y_min) + (int(y_height) / 2)) / height
            temp_width = int(x_width) / float(width)
            temp_height = int(y_height) / float(height)
            f.write('{cat} {x_ctr} {y_ctr} {width} {height}\n'.format(cat=cat, x_ctr=x_ctr,
                                                                      y_ctr=y_ctr, width=temp_width,
                                                                      height=temp_height))

    os.remove(annotation_name)
    print("succeed")
