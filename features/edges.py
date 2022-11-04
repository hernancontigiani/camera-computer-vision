import time
import cv2
import numpy as np

class EdgeDetector():
    def __init__(self, edge_only=False):
        self.edged = None
        self.contornos = None
        self.edge_only = edge_only
    
    def __call__(self, image):
        t0 = time.time()
       
        # Transformar la imagen en esacala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Aplicar algortimo Canny para encontrar bordes
        # Hay que ajustar los filtros min y max según el
        # fondo y la luz
        self.edged = cv2.Canny(gray, 50, 150)
        
        # Encontrar los contornos formados por esos bordes
        contours, hierarchy = cv2.findContours(self.edged, 
            cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
        self.contornos = contours

        t = time.time()
        print(self.__class__.__name__,'time =', t-t0)

    def draw(self, image):
        # Dibujar todos los contornos en la imagen
        if self.edge_only == False and self.contornos is not None:
            cv2.drawContours(image, self.contornos, -1, (0, 255, 0), 1)
        if self.edge_only == True and self.edged is not None:
            image = self.edged
        return image
