import cv2
import numpy as np
from tensorflow.keras.preprocessing import image
import tensorflow as tf

class camera: 

    def __init__(self):
        self.cap = cv2.VideoCapture('http://192.168.2.29:8080/video')


    def check_camera(self):
        if not self.cap.isOpened():
            return False
        else:
            return True

        

    def capture_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        else:
            return frame


    def process_frame(self, frame):
        img = cv2.resize(frame, (160, 160))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
        return img_array

    def close_camera(self):
        self.cap.release()