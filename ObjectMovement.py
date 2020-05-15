from collections import deque
from imutils.video import VideoStream
import numpy as np 
import argparse
import cv2
import imutils 
import time 

#Construst the argument parse and parse the arguments 
ap = argparse.ArgumentParser()

ap.add_argument("--v", "--video", help = "media/tokyo.mp4" )

#Controls maximum size of deque points set as 32 
ap.add_argument("-b", "--buffer", type = int, default = 32)

args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
pts = deque(maxlen=args["buffer"])
counter = 0
(dX, dY) = (0, 0)
direction = ""
# if a video path was not supplied, use webcam
if not args.get("Video", False):
	vs = VideoStream(src=0).start()
# otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["media/tokyo.mp4"])
# allow the camera or video file to warm up
time.sleep(2.0)
