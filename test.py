import cv2 

# script to test if I can read photos

img = cv2.imread("inputs/front_{0}.jpg".format(int(1.0)))
print(img.shape[:2])