from cv2 import cv2
import numpy as np
from Shape import Shape 

class Analysis:
    # Default values
    cascade = cv2.CascadeClassifier("haarcascades/haarcascade_fullbody.xml")
    path = shapes = None
    frameBuffer = people = []


    # Constructor
    def __init__(self, path, shapes):
        self.path = path
        self.shapes = shapes

    
    # Find the midpoint of the rectangle
    def summarize(self, x, y, w, h):
        return (x + w/2, y + h/2)
    
    
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

            # ML model processing
            if ret == True:
                # Detecting bodies using haarcascades model
                imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                bodies = self.cascade.detectMultiScale(imgGray, scaleFactor = 1.05, maxSize = (70, 100))

                # Looping through all the squares
                for (x, y, w, h) in bodies:
                    # Store the people in a list
                    self.people.append(self.summarize(x, y, w, h))
                    
                    # Draw the rectangle
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    self.countPeople()

                # If there are already 5 frames stored, cut out the first one 
                if len(self.frameBuffer) == 5:
                    self.frameBuffer = self.frameBuffer[1:]
                self.frameBuffer.append(self.people)

                # Scale the frame down to 720p for resolution compatibility 
                frame = cv2.resize(frame, (1280, 720))
                cv2.imshow("Result", frame)

                # The escape key
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows() 


    # This function takes in the shapes (the selected doorways)
    # and then outputs a csv file with the counts of unique people that
    # entered each doorway
    # See data/testdata.csv for what the file should look like
    def countPeople(self):
        pass