import cv2 as cv
from color import *
cam = cv.VideoCapture(0)
while True:
    ret, frame = cam.read()
    frame2 = detect_red(frame)
    cv.imshow('frame2', frame2)
    cv.imshow('frame', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    
cam.release()
cv.destroyAllWindows()

detect_red(1)
