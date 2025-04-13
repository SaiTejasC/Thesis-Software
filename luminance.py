import cv2 as cv
import numpy as np

MAX_LUMINANCE = 200

def bgr_to_luminance(bgr: tuple[int, int, int]):
    def convert(val: int):
        normalized = val / 255
        return ((normalized + 0.055) / 1.055) ** 2.4 if normalized > 0.04045 else normalized / 12.92

    if isinstance(bgr, tuple):
        blue, green, red = bgr
        luminance = MAX_LUMINANCE * (
            0.2126 * convert(red) + 0.7152 * convert(green) + 0.0722 * convert(blue)
        )
        return luminance

    if isinstance(bgr, np.ndarray):
        bgr = bgr.astype(float) / 255
        blue, green, red = bgr[..., 0], bgr[..., 1], bgr[..., 2]
        luminance = MAX_LUMINANCE * (
            0.2126 * ((red + 0.055) / 1.055) ** 2.4 * (red > 0.04045) + 0.2126 * (red / 12.92) * (red <= 0.04045) +
            0.7152 * ((green + 0.055) / 1.055) ** 2.4 * (green > 0.04045) + 0.7152 * (green / 12.92) * (green <= 0.04045) +
            0.0722 * ((blue + 0.055) / 1.055) ** 2.4 * (blue > 0.04045) + 0.0722 * (blue / 12.92) * (blue <= 0.04045)
        )
        return luminance
    
