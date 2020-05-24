from cv2 import cv2

cascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")


# SNAPSHOT
img = cv2.imread("media/tokyo_snapshot.png")
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = cascade.detectMultiScale(imgGray, 1.1, 4)

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)


# SAMPLE VIDEO


img = cv2.resize(img, (1280, 720))
cv2.imshow("Result", img)
cv2.waitKey(0)