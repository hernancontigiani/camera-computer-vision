import os
import cv2

from features import Segmentation

image = cv2.imread('images/objects.jpg')

detector = Segmentation()
detector(image)
image = detector.draw(image)

cv2.imwrite("outputs/segmentation.jpg", image)