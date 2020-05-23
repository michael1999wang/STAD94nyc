from cv2 import cv2
import numpy as np

class Focus:
    # Default values
    path, image = None, None
    shapes, points = [], []

    # Constructor
    def __init__(self, path):
        # Setting up the cv2 window
        self.path = path
        self.image = cv2.imread(path)
        cv2.namedWindow("Focus")
        cv2.setMouseCallback("Focus", self.create_polygon)
        
        # Infinite loop to run polygon creation
        while(True):
            # Drawing the original/modified image every time
            cv2.imshow('Focus', self.image)

            # Key presses
            command = cv2.waitKey(10) & 0xFF
            
            # Local parameters
            pts = np.asarray(self.points, np.int32).reshape(-1, 1, 2)
            color = (0, 0, 255)
            thickness = 2

            # Submit shape
            if command == ord('a'):
                # Save the points as a new shape
                self.shapes.append(self.points)

                # Debugging lines
                print(self.shapes)
                
                # Draw the polygon
                cv2.polylines(self.image, [pts], True, color, thickness, lineType = cv2.LINE_AA)

                # Clear the points for a new polygon
                self.points = []

            # Delete previous shape if a mistake was made
            elif command == ord('d'):
                self.shapes = self.shapes[:-1]
                self.image = cv2.imread(path)
                for shape in self.shapes:
                    cv2.polylines(self.image, [np.asarray(shape, np.int32).reshape(-1, 1, 2)], True, color, thickness, lineType = cv2.LINE_AA)
           
            # Exit condition
            elif command == ord('q'):
                break
        
        # Close all windows after exit
        cv2.destroyAllWindows() 


    # Detecting keypresses
    def create_polygon(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONUP:
            self.points.append([x, y])

    
    # Returning shapes for masks
    def getShapes(self):
        return self.shapes

    
    # Returning shape string in a more readable format
    def shapeString(self):
        output = "\n"
        for shape in self.shapes:
            for coordinates in shape:
                output += "(" + str(coordinates[0]) + "," + str(coordinates[1]) + ") "
            output += "\n"
        return output