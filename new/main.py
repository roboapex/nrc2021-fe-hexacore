# https://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/
# https://techvidvan.com/tutorials/detect-objects-of-similar-color-using-opencv-in-python/

import numpy as np
import cv2
# import serial

# ser = serial.Serial("/dev/ttyACM0", 115200, timeout=1)

image = cv2.imread("./test.png")

boundaries = [
	([0,50,50], [15,255,255], "Red"), # red
	([35,50,50], [75,255,255], "Green"), # green
]

cap = cv2.VideoCapture(1)

while True:
	isSuccess, image = cap.read()
	if not isSuccess:
		print("Camera Error")
		break
	
	image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	max_countours = []

	for bound in boundaries:
		lower = np.array(bound[0], dtype="uint8")
		upper = np.array(bound[1], dtype="uint8")
		mask = cv2.inRange(image, lower, upper)

		# Remove noise
		# kernel = np.ones((7,7), np.uint8)
		# mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
		# mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

		segmented_img = cv2.bitwise_and(image, image, mask=mask)

		contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		# image = cv2.drawContours(segmented_img, contours, -1, (0, 0, 255), 3)

		# for c in contours:
		# 	x,y,w,h = cv2.boundingRect(c)
		# 	cv2.putText(output, str(w), (x,y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
		# 	cv2.rectangle(output, (x, y), (x + w, y + h), (36,255,12), 1)

		if len(contours) > 0:
			area = max(contours, key=cv2.contourArea)
			max_countours.append(area)

	if len(max_countours) > 0:
		area = max(max_countours, key=cv2.contourArea)

		if cv2.contourArea(area) > 7000:
			(xr,yr,wr,hr) = cv2.boundingRect(area)
			cv2.rectangle(image, (xr,yr),(xr+wr, yr+hr),(255,255,255),2)

			if max_max_contour := max_countours.index(area):
				cv2.putText(image,f'{boundaries[0 if max_max_contour == None else max_max_contour][2]} {hr}', (xr,yr), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

	cv2.imshow("images", image)


	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cv2.destroyAllWindows()
cap.release()