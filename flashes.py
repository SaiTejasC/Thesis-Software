import cv2
import numpy as np

#logic of the code:
#prev = previous image
#prevIluminance = get a heatmap of the illuminance of the image
# - probabbly where you check illuminnace and measure record it
#curr = current image
#identify coord of the patterns in the current image
#magic function that checks the illuminancne and compare it with prevIlluminance if theres big spots with difference of 20


# Constants
VIDEO_PATH = "vr_video.mp4"  # Change this to your video file
FLASH_THRESHOLD = 220  # Adjust as needed
BRIGHTNESS_DIFF_THRESHOLD = 50  # Adjust sensitivity
MIN_INTERVAL_WIDTH = 0.5  # Minimum interval width in seconds

# Initialize variables
prev_brightness = None
flash_intervals = []
current_interval = None

def detect_flash(frame, timestamp):
    global prev_brightness, current_interval
    
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Calculate brightness
    current_brightness = np.mean(gray)
    
    # Compare with previous frame
    if prev_brightness is not None:
        brightness_change = abs(current_brightness - prev_brightness)
        if brightness_change > BRIGHTNESS_DIFF_THRESHOLD or current_brightness > FLASH_THRESHOLD:
            if current_interval is None:
                current_interval = [timestamp, timestamp]
            else:
                current_interval[1] = timestamp
        elif current_interval is not None:
            # Ensure minimum interval width
            if current_interval[1] - current_interval[0] >= MIN_INTERVAL_WIDTH:
                flash_intervals.append(tuple(current_interval))
            current_interval = None
    
    # Update previous brightness
    prev_brightness = current_brightness

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    
    fps = cap.get(cv2.CAP_PROP_FPS)  # Get frames per second
    frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        timestamp = frame_count / fps  # Calculate timestamp in seconds
        detect_flash(frame, timestamp)
        frame_count += 1
    
    cap.release()
    
    # Append last interval if it wasn't closed and meets the minimum width
    if current_interval is not None and current_interval[1] - current_interval[0] >= MIN_INTERVAL_WIDTH:
        flash_intervals.append(tuple(current_interval))
    
    print("Processing complete.")
    print("Detected flash intervals:", flash_intervals)
    
if __name__ == "__main__":
    process_video(VIDEO_PATH)