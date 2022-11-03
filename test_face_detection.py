import os
import cv2

from detection import FaceDetection

image = cv2.imread('images/people.jpg')

face_detector = FaceDetection()
face_detector(image)
image = face_detector.draw(image)

cv2.imwrite("outputs/face_detection.jpg", image)