import os
import time
import cv2

script_path = os.path.dirname(os.path.abspath(__file__))


class FaceDetection():
    def __init__(self):
        self.faces = []
        self.threshold = 8

        # Clasificador de caras
        self.face_cascade = cv2.CascadeClassifier(f'{script_path}/haarcascade_frontalface_default.xml')
    
    def __call__(self, image):
        t0 = time.time()
       
        # Transformar a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detectar caras (faces) en la imagen
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=8,  # threashold (más alto es más exigente)
            minSize=(30, 30),  # tamaño de la cara minima
        )
        self.faces = faces

        t = time.time()
        print(self.__class__.__name__,'time =', t-t0)

    def draw(self, image):
        # Dibujar las caras
        for (x, y, w, h) in self.faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        return image
