import cv2

from facefilters.filters import FaceFilter, FacePoints

frame = cv2.imread('images/face_1.jpg')
face_filter = FacePoints()
face_filter(frame)
frame = face_filter.draw(frame)
cv2.imwrite("outputs/points_output.jpg", frame)

frame = cv2.imread('images/face_1.jpg')
face_filter = FaceFilter()
face_filter(frame)
frame = face_filter.draw(frame)
cv2.imwrite("outputs/filter_output.jpg", frame)