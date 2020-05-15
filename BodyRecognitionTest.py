from cv2 import cv2
import numpy as np
import matplotlib.pyplot as plt

# The cascade
cascade = cv2.CascadeClassifier("haarcascades/haarcascade_fullbody.xml")

# Starting cv2 thread for performance reasons
# cv2.startWindowThread()
# cv2.namedWindow("Result")

# SNAPSHOT
# img = cv2.imread("media/tokyo_snapshot.png")
# imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# faces = cascade.detectMultiScale(imgGray, 1.05, 1)

# for (x, y, w, h) in faces:
#     cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

# img = cv2.resize(img, (1280, 720))
# cv2.imshow("Result", img)
# cv2.waitKey(0)


# SAMPLE VIDEO
cap = cv2.VideoCapture("media/tokyo.mp4")
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = cascade.detectMultiScale(imgGray, 1.05, 1)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        frame = cv2.resize(frame, (1280, 720))
        cv2.imshow("Result", frame)
        cv2.waitKey(1)
    else:
        break
cap.release()
cv2.destroyAllWindows() 

#hello