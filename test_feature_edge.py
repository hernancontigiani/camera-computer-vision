import os
import cv2

from features import EdgeDetector

image = cv2.imread('images/objects.jpg')

detector = EdgeDetector()
detector(image)
image = detector.draw(image)

cv2.imwrite("outputs/edge_detection.jpg", image)