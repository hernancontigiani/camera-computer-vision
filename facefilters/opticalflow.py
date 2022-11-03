import math

import numpy as np
import cv2


if __name__ == "__main__" or __name__ == "opticalflow":
    import faceBlendCommon as fbc
else:
    from . import faceBlendCommon as fbc


class OpticalFlow():
    def __init__(self, points2, frame):
        self.points2Prev = np.array(points2, np.float32)
        self.img2Gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.img2GrayPrev = np.copy(self.img2Gray)

        self.sigma = 50

    def step(self, points2, frame):
        lk_params = dict(winSize=(101, 101), maxLevel=15,
        criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 20, 0.001))
        points2Next, st, err = cv2.calcOpticalFlowPyrLK(
                        self.img2GrayPrev, self.img2Gray, 
                        self.points2Prev,
                        np.array(points2, np.float32),
                        **lk_params)

        # Final landmark points are a weighted average of detected landmarks and tracked landmarks
        for k in range(0, len(points2)):
            d = cv2.norm(np.array(points2[k]) - points2Next[k])
            alpha = math.exp(-d * d / self.sigma)
            points2[k] = (1 - alpha) * np.array(points2[k]) + alpha * points2Next[k]
            points2[k] = fbc.constrainPoint(points2[k], frame.shape[1], frame.shape[0])
            points2[k] = (int(points2[k][0]), int(points2[k][1]))


        # Update variables for next pass
        self.points2Prev = np.array(points2, np.float32)
        self.img2GrayPrev = self.img2Gray

        return points2