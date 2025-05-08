import cv2 as cv

#logic of the code:
#prev = previous image
#prevPatterns = identify the coords of the patterns in the previous image
# - probabbly where you check illuminnace of patterns if its >50
#curr = current image
#identify coord of the patterns in the current image
# - also probabbly where you check illuminnace of the patterns if its >50
#check how much the patterns moved
#magic function that checks how much the pattern moved

#PseudoCodeish below

def pattern_detection(image):
    #somehow detects the coords of the patterns(pattern is only detected when its >50 cd/m2)
    #returns a list with the coords of the patterns(you can get the number of stripes from the length of the list)

    #ex:
    patternCoords = [[[1,2],[1,3],[1,4],[1,5]],[[3,2],[3,3],[3,4],[3,5]],[[5,2],[5,3],[5,4],[5,5]]]
    return patternCoords

#this looks at the previous frame's pattern coords, and sees how much they have moved in the current frame
def patten_comparision(prevImage, currImage):
    prevPatternCoords = pattern_detection(prevImage)
    currentPatternCoords = pattern_detection(currImage)
    #number of pixels that are part of the patterns
    prevPatternPixels = 0

    #number of pixels that are in the previous pattern, that are also in the current pattern
    prevPatternInCurrPattern = 0
    for pattern in prevPatternCoords:
        for coord in pattern:
            prevPatternPixels += 1
            if (any(coord in pattern2 for pattern2 in currentPatternCoords)):
                prevPatternInCurrPattern += 1
    
    patternChange = prevPatternInCurrPattern/prevPatternPixels
    #if patternChange is above a certain threshhold, that means the patterns moved alot and this a trigger.
    # if it = 0, that means the patterns have not moved, hence no trigger
    return patternChange < 0.5 #0.5 can be changed, just a placeholder



    
