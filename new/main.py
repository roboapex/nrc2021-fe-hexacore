# https://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/
# https://techvidvan.com/tutorials/detect-objects-of-similar-color-using-opencv-in-python/

import numpy as np
import cv2
# import serial

# ser = serial.Serial("/dev/ttyACM0", 115200, timeout=1)

boundaries = [
	([0,50,50], [110,255,255], "Red"), # red
	([35,50,50], [75,255,255], "Green"), # green
]

cap = cv2.VideoCapture(0)
index = 0

while True:
	isSuccess, image = cap.read()
	if not isSuccess:
		print("Camera Error")
		break

	image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	sub_max_countours = []

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
			sub_max_cnt = max(contours, key=cv2.contourArea)
			sub_max_countours.append(sub_max_cnt)

	if len(sub_max_countours) > 0:
		areas = [cv2.contourArea(x) for x in sub_max_countours]

		max_area = max(areas)
		max_cnt = sub_max_countours[areas.index(max_area)]

		if max_area > 7000:
			(xr,yr,wr,hr) = cv2.boundingRect(max_cnt)
			cv2.rectangle(image, (xr,yr),(xr+wr, yr+hr),(255,255,255),2)
			
			t = areas.index(max_area)
			color = boundaries[0 if t == None else t][2]
			height = hr
			print(color, height, index)
			cv2.putText(image,f'{color} {height}', (xr,yr), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

	# cv2.imshow("images", image)

	x = ("00000" + str(index))[-5:]
	cv2.imwrite(f"data/img{x}.jpg", image)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

	index += 1

cv2.destroyAllWindows()
cap.release()

vid_capture = cv2.VideoCapture('data/img%05d.jpg')