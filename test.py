import cv2 

# script to test if I can read photos

img = cv2.imread("inputs/back_{0}.jpg".format(int(1.0)))
print(img.shape[:2])