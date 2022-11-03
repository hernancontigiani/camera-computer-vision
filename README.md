# Camera streaming with computer vision
![banner](images/hc_computer_vision.png)

# About this project 🚀
Small example of how to use and play with different techniques of computer vision using your PC web camera or cellphone by a Python web Flask server.

# Requirements 📋
| Package     | Version |
| ----------- | ------- |
| Python      | >3.7    |
| Flask       | >2.0    |
| OpenCV      | 4.5.5   |
| mediapipe   | 0.8.9   |
| Docker      |         |

# Algorithms 
- features folder
    - Edge detector
    - Color segmentation
- detection
    - object detection
    - face detection
    - image overlap with detections
- filters
    - face relevant point detection
    - face filters

# Main application 🔧⚙️
__vision.py__ is the main script waiting for frames coming from MQTT camera (PC or cellphone) and apply computer vision algorithms. Open ".env" file and setup your MQTT broker configuration and CV algorithm to play around.

# Coming soon 🔧⚙️
- Docker container for CV application.

# Author ✒️
:octocat: Hernán Contigiani 

# Thanks!
Feel free to contact me by mail _hernan4790@gmail.com_ for any doubt.\
Enjoy :smile:!!
