from cv2 import cv2
import numpy as np

class BodyRecognition:
    # Default values
    cascade = cv2.CascadeClassifier("haarcascades/haarcascade_fullbody.xml")
    path = None


    # Constructor
    def __init__(self, path):
        self.path = path
        cap = cv2.VideoCapture(self.path)
        while(cap.isOpened()):
            ret, frame = cap.read()
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