import os

import cv2
import numpy as np

if __name__ == "__main__":
    from object_detection import ObjectDetection
else:
    from .object_detection import ObjectDetection

script_path = os.path.dirname(os.path.abspath(__file__))


def add_transparent_image(background, foreground, x_offset=0, y_offset=0):
    bg_h, bg_w, bg_channels = background.shape
    fg_h, fg_w, fg_channels = foreground.shape

    assert bg_channels == 3, f'background image should have exactly 3 channels (RGB). found:{bg_channels}'
    assert fg_channels == 4, f'foreground image should have exactly 4 channels (RGBA). found:{fg_channels}'

    x_offset -= int(fg_w / 2)
    y_offset -= int(fg_h / 2)

    w = min(fg_w, bg_w, fg_w + x_offset, bg_w - x_offset)
    h = min(fg_h, bg_h, fg_h + y_offset, bg_h - y_offset)

    if w < 1 or h < 1: return

    # clip foreground and background images to the overlapping regions
    bg_x = max(0, x_offset)
    bg_y = max(0, y_offset)
    fg_x = max(0, x_offset * -1)
    fg_y = max(0, y_offset * -1)
    foreground = foreground[fg_y:fg_y + h, fg_x:fg_x + w]
    background_subsection = background[bg_y:bg_y + h, bg_x:bg_x + w]

    # separate alpha and color channels from the foreground image
    foreground_colors = foreground[:, :, :3]
    alpha_channel = foreground[:, :, 3] / 255  # 0-255 => 0.0-1.0

    # construct an alpha_mask that matches the image shape
    alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))

    # combine the background with the overlay image weighted by alpha
    composite = background_subsection * (1 - alpha_mask) + foreground_colors * alpha_mask

    # overwrite the section of the background image that has been updated
    background[bg_y:bg_y + h, bg_x:bg_x + w] = composite


class OverlapImage():
    def __init__(self, object_detector, size=(50,50)):
        self.size = size
        item = cv2.imread(f'{script_path}/overlap.png', cv2.IMREAD_UNCHANGED)
        self.item = cv2.resize(item, self.size, interpolation = cv2.INTER_AREA)

        self.detector = object_detector
        self.detections = None

    def __call__(self, img):
        self.detections = self.detector(img)

    def draw(self, img):
        if self.detections is None:
            return img

        self.detector.draw(img)

        for i in range(len(self.detections.boxes)):
            label = self.detections.classes[self.detections.classIDs[i]]
            if label == "person":
                x = int(self.detections.boxes[i][0] + self.detections.boxes[i][2] / 2)
                y = int(self.detections.boxes[i][1])
                add_transparent_image(img, self.item, x_offset=x, y_offset=y)

        return img
