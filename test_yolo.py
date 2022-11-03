import os
import cv2

from detection import ObjectDetection

image = cv2.imread('images/objects.jpg')

yolo = ObjectDetection('yolov3.weights', 'yolov3.cfg')
detections = yolo(image)
print(detections.to_json())
image = yolo.draw(image)

cv2.imwrite("outputs/object_detection.jpg", image)