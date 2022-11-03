import os
import cv2

from detection import ObjectDetection, OverlapImage

image = cv2.imread('images/people.jpg')

yolo = ObjectDetection('yolov3.weights', 'yolov3.cfg')
overlap = OverlapImage(yolo)

overlap(image)
image = overlap.draw(image)

cv2.imwrite("outputs/image_overlap.jpg", image)