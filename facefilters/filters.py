import os
import math
import csv
import time

import numpy as np
import mediapipe as mp
import cv2


if __name__ == "__main__":
    import faceBlendCommon as fbc
    from helpers import *
else:
    from . import faceBlendCommon as fbc
    from .helpers import *


script_path = os.path.dirname(os.path.abspath(__file__))

filters_config = {
    'anonymous':
        [{'path': f"{script_path}/filters_data/anonymous.png",
          'anno_path': f"{script_path}/filters_data/anonymous_annotations.csv",
          'morph': True, 'animated': False, 'has_alpha': True}],
    'anime':
        [{'path': f"{script_path}/filters_data/anime.png",
          'anno_path': f"{script_path}/filters_data/anime_annotations.csv",
          'morph': True, 'animated': False, 'has_alpha': True}],
    'dog':
        [{'path': f"{script_path}/filters_data/dog-ears.png",
          'anno_path': f"{script_path}/filters_data/dog-ears_annotations.csv",
          'morph': False, 'animated': False, 'has_alpha': True},
         {'path': f"{script_path}/filters_data/dog-nose.png",
          'anno_path': f"{script_path}/filters_data/dog-nose_annotations.csv",
          'morph': False, 'animated': False, 'has_alpha': True}],
    'cat':
        [{'path': f"{script_path}/filters_data/cat-ears.png",
          'anno_path': f"{script_path}/filters_data/cat-ears_annotations.csv",
          'morph': False, 'animated': False, 'has_alpha': True},
         {'path': f"{script_path}/filters_data/cat-nose.png",
          'anno_path': f"{script_path}/filters_data/cat-nose_annotations.csv",
          'morph': False, 'animated': False, 'has_alpha': True}],
    'jason-joker':
        [{'path': f"{script_path}/filters_data/jason-joker.png",
          'anno_path': f"{script_path}/filters_data/jason-joker_annotations.csv",
          'morph': True, 'animated': False, 'has_alpha': True}],
    'gold-crown':
        [{'path': f"{script_path}/filters_data/gold-crown.png",
          'anno_path': f"{script_path}/filters_data/gold-crown_annotations.csv",
          'morph': False, 'animated': False, 'has_alpha': True}],
    'flower-crown':
        [{'path': f"{script_path}/filters_data/flower-crown.png",
          'anno_path': f"{script_path}/filters_data/flower-crown_annotations.csv",
          'morph': False, 'animated': False, 'has_alpha': True}],
}


class FacePoints():
    def __init__(self, max_num_faces=1, min_detection_confidence=0.5, static_image_mode=True):
        mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = mp_face_mesh.FaceMesh(max_num_faces=max_num_faces,
                                          min_detection_confidence=min_detection_confidence,
                                          static_image_mode=static_image_mode
                                         )      

    # (preprocess) detect facial landmarks in image
    def __getLandmarks(self, img):
        
        selected_keypoint_indices = [127, 93, 58, 136, 150, 149, 176, 148, 152, 377, 400, 378, 379, 365, 288, 323, 356, 70, 63, 105, 66, 55,
                    285, 296, 334, 293, 300, 168, 6, 195, 4, 64, 60, 94, 290, 439, 33, 160, 158, 173, 153, 144, 398, 385,
                    387, 466, 373, 380, 61, 40, 39, 0, 269, 270, 291, 321, 405, 17, 181, 91, 78, 81, 13, 311, 306, 402, 14,
                    178, 162, 54, 67, 10, 297, 284, 389]

        relevant_keypnts = []
        height, width = img.shape[:-1]
        results = self.face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                values = np.array(face_landmarks.landmark)
                face_keypnts = np.zeros((len(values), 2))

                for idx,value in enumerate(values):
                    face_keypnts[idx][0] = value.x
                    face_keypnts[idx][1] = value.y

                # Convert normalized points to image coordinates
                face_keypnts = face_keypnts * (width, height)
                face_keypnts = face_keypnts.astype('int')

                for i in selected_keypoint_indices:
                    relevant_keypnts.append(face_keypnts[i])
        
        return relevant_keypnts

    def __model_inference(self, img):
        points2 = self.__getLandmarks(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        return points2

    def __call__(self, img):
        t0 = time.time()
        points2 = self.__model_inference(img)
        if not points2 or (len(points2) != 75):
            return False
        
        self.points2 = points2
        t = time.time()
        print(self.__class__.__name__,'time =', t-t0)

    def draw(self, img):
        if self.points2 is None:
            return

        for idx, point in enumerate(self.points2):
            cv2.circle(img, tuple(point), 2, (255, 0, 0), -1)
            #cv2.putText(img, str(idx), tuple(point), cv2.FONT_HERSHEY_SIMPLEX, .3, (255, 255, 255), 1)

        return img


class FaceFilter(FacePoints):
    def __init__(self, filter="dog", max_num_faces=1, min_detection_confidence=0.5, static_image_mode=True):

        super().__init__(max_num_faces=max_num_faces,
                         min_detection_confidence=min_detection_confidence,
                         static_image_mode=static_image_mode
                        )

        self.filter = filter
        self.filters, self.multi_filter_runtime = load_filter(filters_config, self.filter)
        self.points2 = None

    def apply_filter(self, img):
        if self.points2 is None:
            return

        for idx, filter in enumerate(self.filters):
            filter_runtime = self.multi_filter_runtime[idx]
            img1 = filter_runtime['img']
            points1 = filter_runtime['points']
            img1_alpha = filter_runtime['img_a']

            if filter['morph']:
                hullIndex = filter_runtime['hullIndex']
                dt = filter_runtime['dt']
                hull1 = filter_runtime['hull']

                # create copy of frame
                warped_img = np.copy(img)

                # Find convex hull
                hull2 = []
                for i in range(0, len(hullIndex)):
                    hull2.append(self.points2[hullIndex[i][0]])

                mask1 = np.zeros((warped_img.shape[0], warped_img.shape[1]), dtype=np.float32)
                mask1 = cv2.merge((mask1, mask1, mask1))
                img1_alpha_mask = cv2.merge((img1_alpha, img1_alpha, img1_alpha))

                # Warp the triangles
                for i in range(0, len(dt)):
                    t1 = []
                    t2 = []

                    for j in range(0, 3):
                        t1.append(hull1[dt[i][j]])
                        t2.append(hull2[dt[i][j]])

                    fbc.warpTriangle(img1, warped_img, t1, t2)
                    fbc.warpTriangle(img1_alpha_mask, mask1, t1, t2)

                # Blur the mask before blending
                mask1 = cv2.GaussianBlur(mask1, (3, 3), 10)

                mask2 = (255.0, 255.0, 255.0) - mask1

                # Perform alpha blending of the two images
                temp1 = np.multiply(warped_img, (mask1 * (1.0 / 255)))
                temp2 = np.multiply(img, (mask2 * (1.0 / 255)))
                output = temp1 + temp2
            else:
                dst_points = [self.points2[int(list(points1.keys())[0])], self.points2[int(list(points1.keys())[1])]]
                tform = fbc.similarityTransform(list(points1.values()), dst_points)
                # Apply similarity transform to input image
                trans_img = cv2.warpAffine(img1, tform, (img.shape[1], img.shape[0]))
                trans_alpha = cv2.warpAffine(img1_alpha, tform, (img.shape[1], img.shape[0]))
                mask1 = cv2.merge((trans_alpha, trans_alpha, trans_alpha))

                # Blur the mask before blending
                mask1 = cv2.GaussianBlur(mask1, (3, 3), 10)

                mask2 = (255.0, 255.0, 255.0) - mask1

                # Perform alpha blending of the two images
                temp1 = np.multiply(trans_img, (mask1 * (1.0 / 255)))
                temp2 = np.multiply(img, (mask2 * (1.0 / 255)))
                output = temp1 + temp2

            img = np.uint8(output)

        return img
        
    def draw(self, img):
        output = self.apply_filter(img)
        img[:,:,:] = output[:,:,:]
        return img


if __name__ == "__main__":
    frame = cv2.imread('face_1.jpg')
    face_filter = FacePoints()
    face_filter(frame)
    face_filter.draw(frame)
    cv2.imwrite("outputs/points_output.jpg", frame)

    frame = cv2.imread('face_1.jpg')
    face_filter = FaceFilter()
    face_filter(frame)
    face_filter.draw(frame)
    cv2.imwrite("outputs/filter_output.jpg", frame)


