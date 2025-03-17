import cv2 as cv
#logic of the code:
#prev = previous image
#prevIluminance = get a heatmap of the illuminance of the image
# - probabbly where you check illuminnace and measure record it
#curr = current image
#identify coord of the patterns in the current image
#magic function that checks the illuminancne and compare it with prevIlluminance if theres big spots with difference of 20