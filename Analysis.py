from cv2 import cv2
import numpy as np
from BodyRecognition import BodyRecognition

class Analysis:
    # Default values
    cascade = cv2.CascadeClassifier("haarcascades/haarcascade_fullbody.xml")
    path = None
    bodyRecognition = None


    # Constructor
    def __init__(self, path):
        self.path = path
    
    
    # Masking the doorways
    def execMasking(self):
        pass

    
    # Detecting people
    def execBodyRecognition(self):
        self.bodyRecognition = BodyRecognition(self.path)


# a = Analysis("media/tokyo.mp4")
# a.bodyRecognition()