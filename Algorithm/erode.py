import cv2
import numpy as np
def calu2DImageErode(image,size):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (size, size))
    image[:, :] = cv2.erode(image[:, :], kernel)
    return image
def calu2DImageExpand(image, size):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (size, size))
    image[:, :] = cv2.dilate(image[:, :], kernel)
    return image