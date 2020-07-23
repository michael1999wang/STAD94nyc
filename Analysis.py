from cv2 import cv2
import numpy as np
from Shape import Shape 
import math
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

class Point:
    # Default values
    x = y = None

    # Constructor
    def __init__(self, x, y):
        self. x = x
        self. y = y

class Analysis:
    # THRESHOLD CONSTANTS
    RADIUS_OF_DETECTION = 10

    # Default values
    cascade = cv2.CascadeClassifier("haarcascades/haarcascade_fullbody.xml")
    path = shapes = None
    frameBuffer = people = tracked = []

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

        # Boolean to store if it is the first frame
        firstFrame = True

        # Loop through all the frames
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
                    # Store the people in a list of point objects
                    self.people.append(Point(self.summarize(x, y, w, h)[0], self.summarize(x, y, w, h)[1]))

                    # Draw the rectangle
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    self.countPeople()

                # If it is the first frame, load up the tracked array with all the people
                if firstFrame:
                    self.tracked = self.people
                    firstFrame = False

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

    # See if a point is within a given radius of the previous point
    def checkRadius(self, oldPoint, newPoint):
        # Use the Pythagorean theorem to check the new point is within the old point's constant defined radius
        d = math.sqrt((oldPoint.x - newPoint.x)**2 + (oldPoint.y - newPoint.y)**2)
        
        # Return the verdict as a boolean
        if d < self.RADIUS_OF_DETECTION:
            return True
        return False

    # This function takes in the shapes (the selected doorways)
    # and then outputs a csv file with the counts of unique people that
    # entered each doorway
    # See data/testdata.csv for what the file should look like
    def countPeople(self):   
        # Look for new people in the oldest frame
        for framePerson in self.frameBuffer[0]:
            close = False
            for trackedPerson in self.tracked:
                # Check the radius on everyone
                close = close or self.checkRadius(framePerson, trackedPerson)
            # If the person is new
            if not close:
                self.tracked.append(framePerson)

        # Keep track of the found status of each tracked person
        status = []
        for trackedPerson in self.tracked:
            status.append((trackedPerson, False))

        # Loop through the list of tracked people
        for trackedPerson in self.tracked:
            # Index for status reasons
            i = 0

            # Loop through each frame
            for frame in self.frameBuffer[1:]:
                # Loop through each person in the frame
                for framePerson in frame:
                    # If found/update is required
                    if self.checkRadius(trackedPerson, frame):
                        # Update the coordinates to the newest one
                        trackedPerson.x = framePerson.x
                        trackedPerson.y = framePerson.y
                        status[i][1] = True

            # Bump the index
            i += 1

        # Convert shapes into shapely objects
        shapelyShapes = []
        for shape in self.shapes:
            shapelyShapes.append(Polygon(shape.coordinates))

        # Open the csv file for writing

        # All orgiginal, tracked elements with a status of False are counted as "disappeared"
        for person in status:
            if not person[1]:
                # Check if it is in any of the boundaries
                for i in range(0, len(self.shapes)):
                    # Convert person to shapely object
                    point = Point(person[0][0], person[0][1])
                    # If the person disappeared in the doorway
                    if shapelyShapes[i].contains(point):
                        # Tally up in the csv file
                        pass