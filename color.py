import cv2 as cv
import numpy as np

def detect_red(image):
    hsvImage = cv.cvtColor(image,cv.COLOR_BGR2HSV)
    lower1 = np.array([0, 100, 150])
    upper1 = np.array([10, 255, 255])
    lower2 = np.array([160, 100, 150])
    upper2 = np.array([180, 255, 255])
    
    mask1 = cv.inRange(hsvImage, lower1 ,upper1)
    mask2 = cv.inRange(hsvImage, lower2 ,upper2)
    mask = mask1 + mask2

    white_pixels = np.sum(mask == 255)
    black_pixels = np.sum(mask == 0)
    red_percentage = white_pixels/(white_pixels + black_pixels)
    trigger = red_percentage > 0.2
    return trigger, mask
