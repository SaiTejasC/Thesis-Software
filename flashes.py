import cv2
import numpy as np
from luminance import bgr_to_luminance  # Ensure the specific function is imported

# Constants
VIDEO_PATH = "youtube_pokemon.mp4"  # Change this to your video file
FLASH_THRESHOLD = 220  # Adjust as needed
LUMINANCE_DIFF_THRESHOLD = 20  # Adjust sensitivity
MIN_FREQUENCY = 3 # Min frequency of flashes per second

# Initialize variables
prev_luminance = None  # Initialize prev_luminance
flash_timestamps = []


def detect_flash(frame, timestamp):
    global prev_luminance, flash_timestamps
    pixels = frame.reshape(-1, 3)
    current_luminance = bgr_to_luminance(np.array(pixels))
    if prev_luminance is not None:
        luminance_diff = np.mean(np.abs(current_luminance - prev_luminance) > LUMINANCE_DIFF_THRESHOLD)
    else:
        luminance_diff = 0

    if luminance_diff > 0.5:
        flash_timestamps.append(timestamp)

    prev_luminance = current_luminance

def detect_flash2(currentFrame, prevFrame):
    pixels = currentFrame.reshape(-1, 3)
    current_luminance = bgr_to_luminance(np.array(pixels))
    prev_luminance = prevFrame.reshape(-1, 3)
    prev_luminance = bgr_to_luminance(np.array(prev_luminance))
    luminance_diff = np.mean(np.abs(current_luminance - prev_luminance) > LUMINANCE_DIFF_THRESHOLD)
    return luminance_diff > 0.5

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    
    fps = cap.get(cv2.CAP_PROP_FPS)  # Get frames per second
    frame_count = 0
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        timestamp = frame_count / fps  # Calculate timestamp in seconds
        # print(f"frame {frame_count}/{video_length} ({timestamp:.2f}s)")
        detect_flash(frame, timestamp)
        frame_count += 1
    
    cap.release()
    # Calculate ranges with at least 3 flashes in a second
    flash_ranges = []
    if flash_timestamps:
        # start at a frame, go through all frames within a second. if theres at least MIN_FREQUENCY flashes, add to flash_ranges
        # then move on to the next frame
        for i in range(0, len(flash_timestamps)):
            count = 1
            start = flash_timestamps[i]
            end = start
            for j in range(i + 1, len(flash_timestamps)):
                # Check if the next timestamp is within 1 second of the start timestamp
                if flash_timestamps[j] - start <= 1.0:
                    count += 1
                    end = flash_timestamps[j]
                else:
                    break
            if count >= MIN_FREQUENCY:
                flash_ranges.append((start, end))
        
    final_ranges = []
    #merge overlapping ranges
    for start, end in flash_ranges:
        # if current range does not overlap with prev range, then add it
        if not final_ranges or final_ranges[-1][1] < start:
            final_ranges.append((start, end))
        else:
            #if current range does overlap with prev range, then change the prev end to current end
            final_ranges[-1] = (final_ranges[-1][0], max(final_ranges[-1][1], end))

    print(f"Flash ranges with at least {MIN_FREQUENCY} flashes in a second:", final_ranges)
    return final_ranges
    
if __name__ == "__main__":
    process_video(VIDEO_PATH)