from cv2 import cv2
import numpy as np
import matplotlib.pyplot as plt

def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1, y1, x2, y2])

def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1) 
        slope = parameters[0]   
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    if len(left_fit) and len(right_fit):
        left_fit_average  = np.average(left_fit, axis=0)
        right_fit_average = np.average(right_fit, axis=0)
        left_line  = make_coordinates(image, left_fit_average)
        right_line = make_coordinates(image, right_fit_average)
        averaged_lines = [left_line, right_line]
        return averaged_lines

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) # converting to grayscale
    blur = cv2.blur(gray, (10, 5)) # blurring (averaging each pixel with neighbours)
    canny = cv2.Canny(blur, 10, 100) # Finding strong gradient lines
    return canny

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            try:
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10) # drawing detected lines
            except Exception:
                pass
    return line_image

def region_of_interest(image): # isolating the triangle of focus in the picture
    height = image.shape[0]
    width = image.shape[1]
    polygons = np.array([[(205, 621), (1254, 311), (751, 721), (1672, 429)]]) # creating the polygon
    mask = np.zeros_like(image) # the array of mask
    cv2.fillPoly(mask, polygons, 255) # triangle
    masked_image = cv2.bitwise_and(image, mask) # masking the image
    return masked_image

frame = cv2.imread('test_image.jpg')
cv2.imshow("Output", frame)
canny_image = canny(frame)
cropped_canny = region_of_interest(canny_image)
lines = cv2.HoughLinesP(cropped_canny, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
averaged_lines = average_slope_intercept(frame, lines)
line_image = display_lines(frame, averaged_lines)
combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
plt.imshow(combo_image)
plt.show()

# # video
# cap = cv2.VideoCapture("nyc.mp4")
# while(cap.isOpened()):
#     ret, frame = cap.read()
#     if ret == True:
#         canny_image = canny(frame)
#         cropped_canny = region_of_interest(canny_image)
#         lines = cv2.HoughLinesP(cropped_canny, 2, np.pi/180, 100, np.array([]), minLineLength=40,maxLineGap=5)
#         averaged_lines = average_slope_intercept(frame, lines)
#         line_image = display_lines(frame, averaged_lines)
#         combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)     
#         cv2.imshow("result", canny_image)
#         if cv2.waitKey(10) & 0xFF == ord('q'):
#             break
#     else:
#         break
# cap.release()
# cv2.destroyAllWindows() 