import cv2
import numpy as np
from luminance import *
from flashes import *
from color import *
from typing import List


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 15)
fps = cap.get(cv.CAP_PROP_FPS)
print("click 'q' to close camera")
print(f"FPS: {fps}")
framesFlashes: List[bool] = []
frames = []
totalFrames = 0
time = 0
redTimestamps = []
flashTimestamps = []
#how to see the amount of time passed since the start of the program
while cap.isOpened():
    totalFrames += 1
    time = totalFrames / fps
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
                flashTimestamps.append((time, (totalFrames + 1)/ fps))
                triggers.append("flashes")

            if colorTrigger:
                redTimestamps.append((time, (totalFrames + 1)/ fps))
                triggers.append("saturated red")
        
        triggers_text = ", ".join(triggers)
        camFrameUpscale = cv2.resize(camFrame, (int(camFrame.shape[1] * 1.5), int(camFrame.shape[0] * 1.5)))
        camFrame = cv2.putText(camFrameUpscale, "triggers: " + triggers_text, (2, camFrameUpscale.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        cv2.imshow("frame", camFrame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()

finalRedTimestamps = []
finalFlashTimestamps = []
for start, end in flashTimestamps:
        # if current range does not overlap with prev range, then add it
        if not finalFlashTimestamps or finalFlashTimestamps[-1][1] < start - 0.01:
            finalFlashTimestamps.append((start, end))
        else:
            #if current range does overlap with prev range, then change the prev end to current end
            finalFlashTimestamps[-1] = (finalFlashTimestamps[-1][0], max(finalFlashTimestamps[-1][1], end))
for start, end in redTimestamps:
        # if current range does not overlap with prev range, then add it
        if not finalRedTimestamps or finalRedTimestamps[-1][1] < start - 0.01:
            finalRedTimestamps.append((start, end))
        else:
            #if current range does overlap with prev range, then change the prev end to current end
            finalRedTimestamps[-1] = (finalRedTimestamps[-1][0], max(finalRedTimestamps[-1][1], end))
print(f"flash timestamps: {finalFlashTimestamps}")
print(f"red timestamps: {finalRedTimestamps}")