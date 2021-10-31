# https://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/
# https://techvidvan.com/tutorials/detect-objects-of-similar-color-using-opencv-in-python/

import numpy as np
import cv2
import time

image = cv2.imread("./test.png")

boundaries = [
	([17, 15, 100], [200, 56, 200]),
	([86, 31, 4], [220, 88, 50]),
	([25, 146, 190], [62, 174, 250]),
	([103, 86, 65], [145, 133, 128])
]

cap = cv2.VideoCapture(0)

while True:
	isSuccess, image = cap.read()
	if not isSuccess:
		print("Camera Error")
		break

	lower = np.array(boundaries[0][0], dtype="uint8")
	upper = np.array(boundaries[0][1], dtype="uint8")

	mask = cv2.inRange(image, lower, upper)

	# Remove noise
	kernel = np.ones((7,7), np.uint8)
	mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
	mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

	segmented_img = cv2.bitwise_and(image, image, mask=mask)

	contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	output = cv2.drawContours(segmented_img, contours, -1, (0, 0, 255), 3)

	cv2.imshow("images", output)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cv2.destroyAllWindows()
cap.release()