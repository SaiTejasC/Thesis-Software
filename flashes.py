import cv2
import numpy as np

# Constants
VIDEO_PATH = "youtube_CKa2HGuCNdE_852x480_h264.mp4"
FLASH_THRESHOLD = 220                # Brightness threshold for a flash
BRIGHTNESS_DIFF_THRESHOLD = 50       # Sensitivity to brightness changes
MIN_FLASHES = 3                      # Need at least 3 flashes
DETECTION_WINDOW = 1.3               # Increased from 1.0 to 1.5 seconds
MIN_DARK_DURATION = 0.1              # Minimum dark period between flashes (seconds)

# Initialize variables
prev_brightness = None
flash_timestamps = []                # Stores timestamps of valid flashes
in_flash = False
flash_start_time = None

def detect_flash(frame, timestamp):
    global prev_brightness, in_flash, flash_start_time, flash_timestamps

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    current_brightness = np.mean(gray)

    # Flash STARTS when brightness crosses threshold
    if not in_flash and current_brightness > FLASH_THRESHOLD:
        in_flash = True
        flash_start_time = timestamp

    # Flash ENDS when brightness drops below threshold
    elif in_flash and current_brightness <= FLASH_THRESHOLD:
        in_flash = False
        # Only register if there was a minimum dark period before this flash
        if flash_timestamps and (timestamp - flash_timestamps[-1]) < MIN_DARK_DURATION:
            return  # Ignore too-close flashes
        flash_timestamps.append(flash_start_time)

    prev_brightness = current_brightness

def find_flash_clusters(flash_timestamps):
    clusters = []
    current_cluster = []
    
    for timestamp in flash_timestamps:
        if not current_cluster:
            current_cluster.append(timestamp)
            continue
        
        # Key Change: 1.5-second window check (was 1.0)
        if timestamp - current_cluster[0] <= DETECTION_WINDOW:
            current_cluster.append(timestamp)
        else:
            # Save cluster if it has enough flashes
            if len(current_cluster) >= MIN_FLASHES:
                clusters.append((current_cluster[0], current_cluster[-1]))
            # Start new cluster
            current_cluster = [timestamp]
    
    # Add the last cluster if valid
    if len(current_cluster) >= MIN_FLASHES:
        clusters.append((current_cluster[0], current_cluster[-1]))
    
    return clusters

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        timestamp = frame_count / fps
        detect_flash(frame, timestamp)
        frame_count += 1
    
    cap.release()
    
    # Find flash clusters
    flash_clusters = find_flash_clusters(flash_timestamps)
    
    # Print results
    print(f"Total flashes detected: {len(flash_timestamps)}")
    print(f"Flash timestamps: {[f'{t:.2f}' for t in flash_timestamps]}")
    
    if flash_clusters:
        print(f"\nDetected {len(flash_clusters)} valid flash clusters (≥{MIN_FLASHES} flashes in {DETECTION_WINDOW} seconds):")
        for i, (start, end) in enumerate(flash_clusters, 1):
            cluster_flashes = [t for t in flash_timestamps if start <= t <= end]
            print(f"Cluster {i}: {start:.2f}s to {end:.2f}s")
            print(f"  Flashes: {len(cluster_flashes)} at {[f'{t:.2f}' for t in cluster_flashes]}")
            print(f"  Frequency: {len(cluster_flashes)/(end-start):.2f}Hz")
    else:
        print(f"No clusters with ≥{MIN_FLASHES} flashes in {DETECTION_WINDOW} seconds detected.")

if __name__ == "__main__":
    process_video(VIDEO_PATH)