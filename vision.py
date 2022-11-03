import time
import json
from PIL import Image
import base64
import io


import cv2
import numpy as np
import paho.mqtt.client as mqtt

detectors = {}

from features import EdgeDetector
detectors["edges"] = EdgeDetector()

from features import Segmentation
detectors["segmentation"] = Segmentation()

from detection import ObjectDetection
detectors["objects"] = ObjectDetection('yolov3.weights', 'yolov3.cfg')

from detection import OverlapImage
detectors["overlap"] = OverlapImage(detectors["objects"])

from detection import FaceDetection
detectors["faces"] = FaceDetection()

from facefilters import FacePoints
detectors["facemark"] = FacePoints()

from facefilters import FaceFilter
detectors["filter"] = FaceFilter(filter="dog")

from dotenv import dotenv_values

config = dotenv_values()
base_topic = f"cameracv/{config['USERNAME']}"

def on_connect(client, userdata, flags, rc):
    print("MQTT connected")
    
    client.subscribe(f"{base_topic}/raw")


def on_message(client, userdata, msg):
    topic = str(msg.topic)
    value = str(msg.payload.decode("utf-8"))

    if "/raw" in topic:
        img = json.loads(value)['imageData']
        img = img.replace('data:image/jpeg;base64,', '')
        img = img.replace(' ', '+')
        base64_decoded = base64.b64decode(img)
        image = Image.open(io.BytesIO(base64_decoded))

        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        config = dotenv_values()
        detector_type = config["DETECTOR_TYPE"]

        detectors[detector_type](img)
        outimg = detectors[detector_type].draw(img)

        #cv2.imwrite("output.jpg", outimg)
        _, im_arr = cv2.imencode('.jpg', outimg)  # im_arr: image in Numpy one-dim array format.
        im_bytes = im_arr.tobytes()
        im_b64 = base64.b64encode(im_bytes).decode('ascii')
        im_toDataUrl = 'data:image/jpeg;base64,' + im_b64
        post_topic = topic.replace("/raw", "")
        client.publish(f"{post_topic}/{detector_type}", json.dumps({"imageData": im_toDataUrl}))
    

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(config["MQTT_USER"], config["MQTT_PASSWORD"])
    client.connect(config["MQTT_BROKER"], int(config["MQTT_PORT"]), 10)
    client.loop_forever()
