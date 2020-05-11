# COLOR DETECTION
from cv2 import cv2
import numpy as np

def empty(something):
    pass

# Function made by Murtaza's Workshop
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

path = 'media/test_image.jpg'
cv2.namedWindow("Threshold")
cv2.resizeWindow("Threshold", 720, 240)
cv2.createTrackbar("Hue Min", "Threshold", 0, 179, empty)
cv2.createTrackbar("Hue Max", "Threshold", 179, 179, empty)
cv2.createTrackbar("Saturation Min", "Threshold", 0, 255, empty)
cv2.createTrackbar("Saturation Max", "Threshold", 255, 255, empty)
cv2.createTrackbar("Brightness Min", "Threshold", 0, 255, empty)
cv2.createTrackbar("Brightness Max", "Threshold", 255, 255, empty)

while(True):
    # Initializing initial images
    img = cv2.imread(path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Getting current trackbar values
    h_min = cv2.getTrackbarPos("Hue Min", "Threshold")
    h_max = cv2.getTrackbarPos("Hue Max", "Threshold")
    s_min = cv2.getTrackbarPos("Saturation Min", "Threshold")
    s_max = cv2.getTrackbarPos("Saturation Max", "Threshold")
    v_min = cv2.getTrackbarPos("Brightness Min", "Threshold")
    v_max = cv2.getTrackbarPos("Brightness Max", "Threshold")

    # Setting upper and lower bounds
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    # Setting mask and finding overlaps
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)

    # Resizing images
    img = cv2.resize(img, (640, 360))
    hsv = cv2.resize(hsv, (640, 360))
    mask = cv2.resize(mask, (640, 360))
    result = cv2.resize(result, (640, 360))

    # Stacking and displaying images
    stack = stackImages(0.6, ([img, hsv], [mask, result]))
    # stack = stackImages(0.6, ([mask], [result]))
    cv2.imshow("Stack", stack)

    cv2.waitKey(1)

    # Debugging line
    print(h_min, h_max, s_min, s_max, v_min, v_max)