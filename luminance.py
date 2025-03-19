import cv2 as cv

MAX_LUMINANCE = 200

def bgr_to_luminance(bgr: tuple[int,int,int]):
    def convert(val:int):
        if val/255 > 0.04045:
            return ((val/25 + 0.055)/1.055)^2.4
        else:
            return (val/(255 * 12.92))

    blue, green, red = bgr
    luBlue = convert(blue)
    luGreen = convert(green)
    luRed = convert(red)

    luminance = MAX_LUMINANCE * (0.2126*luRed + 0.7152*luGreen + 0.0722*luBlue)
    return luminance
    
