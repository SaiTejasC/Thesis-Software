import cv2
from color import *
from flashes import *

#cam = cv2.VideoCapture(0)
INPUT_PATH = "youtube_pokemon.mp4"
OUTPUT_PATH = "OUTPUT_" + INPUT_PATH
red_timestamps = []

cap = cv2.VideoCapture(INPUT_PATH)
fps = cap.get(cv2.CAP_PROP_FPS)
video_format = cv2.VideoWriter_fourcc(*'mp4v')
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
if height < 1080:
    height = 1080
    width = int(width * (height / cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

out = cv2.VideoWriter(OUTPUT_PATH, video_format, int(fps), (int(width), int(height)))

flashes_clusters = process_video(INPUT_PATH)
ret = True
frame_count = 0
print("FPS:", fps)
print("video length:", cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps, "seconds")


while cap.isOpened():
    timestamp = frame_count/fps
    triggers = []

    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.resize(frame, (width, height))
    flashTrigger = any(start <= timestamp <= end for start, end in flashes_clusters)
    colorTrigger, frame2 = detect_red(frame)

    #here you can OR it with the other triggeres :D
    if colorTrigger or flashTrigger:
        if flashTrigger:
            triggers.append("flashes")

        if colorTrigger:
            red_timestamps.append((timestamp, ((frame_count + 1) / fps)))
            triggers.append("saturated red")
    
    triggers_text = ", ".join(triggers)
    frameAlt = cv2.putText(frame, "triggers: " + triggers_text, (2, frame.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 2)
    out.write(frameAlt)
    frame_count += 1
    
cap.release()
out.release()

 #combine red timestamps where the next timestamp start is the same as the previous end
final_red_timestamps = []
for start, end in red_timestamps:
        # if current range does not overlap with prev range, then add it
        if not final_red_timestamps or final_red_timestamps[-1][1] < start - 0.01:
            final_red_timestamps.append((start, end))
        else:
            #if current range does overlap with prev range, then change the prev end to current end
            final_red_timestamps[-1] = (final_red_timestamps[-1][0], max(final_red_timestamps[-1][1], end))
print("red timestamps ranges:", final_red_timestamps)
print("detection finished >:D")