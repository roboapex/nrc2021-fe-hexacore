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

	# for i in range(len(contours)):
	# 	minRect = cv2.minAreaRect(np.zeros((contours[i]), dtype="uint8"))
	# 	rect_points = cv2.boxPoints(minRect)
	# 	for j in range(4):
	# 		cv2.line(image, rect_points[j], rect_points[(j+1)%4], (255,255,0,0))

	for c in contours:
		x,y,w,h = cv2.boundingRect(c)
		cv2.putText(output, str(w), (x,y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
		cv2.rectangle(output, (x, y), (x + w, y + h), (36,255,12), 1)

	# for (int i = 0;i<contours.size();i++)
  #   {
  #       RotatedRect minRect = minAreaRect( Mat(contours[i]) );
  #       Point2f rect_points[4];
  #       minRect.points( rect_points ); 
  #       for( int j = 0; j < 4; j++ )
  #           line( img, rect_points[j], rect_points[(j+1)%4],Scalar(255,255,0),2);
  #   }

	cv2.imshow("images", output)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cv2.destroyAllWindows()
cap.release()