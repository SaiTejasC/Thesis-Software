import cv2
import numpy as np
from luminance import *
from flashes import *
from color import *

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 15)
fps = cap.get(cv.CAP_PROP_FPS)
print("click 'q' to close camera")
print(f"FPS: {fps}")
from typing import List

framesFlashes: List[bool] = []
frames = []
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    framesFlashes.append(detect_flash2(frame, frames[len(frames) - 1] if len(frames) > 1 else frame))
    frames.append(frame)
    if len(frames) > fps:
        triggers = []
        camFrame = frames.pop(0)
        framesFlashes.pop(0)
        colorTrigger, _ = detect_red(camFrame)
        flashTrigger = framesFlashes.count(True) > MIN_FREQUENCY

        if colorTrigger or flashTrigger:
            if flashTrigger:
                triggers.append("flashes")

            if colorTrigger:
                triggers.append("saturated red")
        
        triggers_text = ", ".join(triggers)
        camFrameUpscale = cv2.resize(camFrame, (int(camFrame.shape[1] * 1.5), int(camFrame.shape[0] * 1.5)))
        camFrame = cv2.putText(camFrameUpscale, "triggers: " + triggers_text, (2, camFrameUpscale.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)

        cv2.imshow("frame", camFrame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()