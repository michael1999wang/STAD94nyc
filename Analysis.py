from cv2 import cv2
import numpy as np
from Shape import Shape

class Analysis:
    # Default values
    cascade = cv2.CascadeClassifier("haarcascades/haarcascade_fullbody.xml")
    path, shapes = None, None


    # Constructor
    def __init__(self, path, shapes):
        self.path = path
        self.shapes = shapes
    
    
    # Detecting people
    def execBodyRecognition(self):
        cap = cv2.VideoCapture(self.path)
        while(cap.isOpened()):
            ret, frame = cap.read()

            # Drawing polygons over initial picture (if there are shapes)
            if self.shapes is not None:
                color = (0, 0, 255)
                thickness = 2
                for shape in self.shapes:
                    pts = np.asarray(shape.coordinates, np.int32).reshape(-1, 1, 2)
                    cv2.polylines(frame, [pts], True, color, thickness, lineType = cv2.LINE_AA)

            # Machine Learning 
            if ret == True:
                imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                bodies = self.cascade.detectMultiScale(imgGray, scaleFactor = 1.05, maxSize = (70, 100))
                for (x, y, w, h) in bodies:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                frame = cv2.resize(frame, (1280, 720))
                cv2.imshow("Result", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows() 