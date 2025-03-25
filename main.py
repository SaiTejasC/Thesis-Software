import cv2 as cv
from color import *
cam = cv.VideoCapture(0)
while True:
    ret, frame1 = cam.read()
    colorTrigger, frame2 = detect_red(frame1)

    #here you can OR it with the other triggeres :D
    if  colorTrigger:
        frame1Alt = cv.putText(frame1, "trigger >:(", (2, frame1.shape[0] - 30), cv.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 2)
        frame2Alt = cv.putText(frame2, "trigger >:(", (2, frame1.shape[0] - 30), cv.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 2)
    else:
        frame1Alt = frame1
        frame2Alt = frame2
    cv.imshow('frame1', frame1Alt)
    cv.imshow('frame2', frame2Alt)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    
cam.release()
cv.destroyAllWindows()
