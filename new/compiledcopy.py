

# https://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/
# https://techvidvan.com/tutorials/detect-objects-of-similar-color-using-opencv-in-python/

import numpy as np
import cv2
import RPi.GPIO as GPIO					
import time
# import serial

# ser = serial.Serial("/dev/ttyACM0", 115200, timeout=1)

#Set-up
boundaries = [
	([0,50,50], [110,255,255], "Red"), # red
	([35,50,50], [75,255,255], "Green"), # green
]

cap = cv2.VideoCapture(0)
index = 0

in1 = 24
in2 = 23
in3 = 17
in4 = 27
en2 = 22
en1 = 25
temp1=1

TRIG = 6
ECHO = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en1,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
p1=GPIO.PWM(en1,1000)
p2=GPIO.PWM(en2,1000)


GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG, False)

print("Waiting For Sensor To Settle")

def get_distance():
	GPIO.output(TRIG, True)
	time.sleep(0.00001)
	GPIO.output(TRIG, False)
	
	while GPIO.input(ECHO) == 0:
		pulse_start = time.time()


	while GPIO.input(ECHO) == 1:
		pulse_end = time.time()
	pulse_duration = pulse_end - pulse_start
	distance = pulse_duration * 17150
	distance = round(distance, 2)

	return distance

p1.start(25)
p2.start(22)
p1.ChangeDutyCycle(100)
p2.ChangeDutyCycle(100)

def forward():
	GPIO.output(in1,GPIO.HIGH)
	GPIO.output(in2,GPIO.LOW)
	GPIO.output(in3,GPIO.HIGH)
	GPIO.output(in4,GPIO.LOW)

def backward():
	GPIO.output(in1,GPIO.LOW)
	GPIO.output(in2,GPIO.HIGH)
	GPIO.output(in3,GPIO.LOW)
	GPIO.output(in4,GPIO.HIGH)

def right():
	GPIO.output(in1,GPIO.HIGH)
	GPIO.output(in2,GPIO.LOW)
	GPIO.output(in3,GPIO.LOW)
	GPIO.output(in4,GPIO.HIGH)
	time.sleep(0.8)
	GPIO.output(in1,GPIO.LOW)
	GPIO.output(in2,GPIO.LOW)
	GPIO.output(in3,GPIO.LOW)
	GPIO.output(in4,GPIO.LOW)

def left():
	GPIO.output(in1,GPIO.LOW)
	GPIO.output(in2,GPIO.HIGH)
	GPIO.output(in3,GPIO.HIGH)
	GPIO.output(in4,GPIO.LOW)
	time.sleep(0.5)
	GPIO.output(in1,GPIO.LOW)
	GPIO.output(in2,GPIO.LOW)
	GPIO.output(in3,GPIO.LOW)
	GPIO.output(in4,GPIO.LOW)

def stop():
	GPIO.output(in1,GPIO.LOW)
	GPIO.output(in2,GPIO.LOW)
	GPIO.output(in3,GPIO.LOW)
	GPIO.output(in4,GPIO.LOW)

forward()

count = ["Green", 0]
colour2 = ""
c = 0
prevHeight = "nope"
while True:
	c += 1
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
			colour2 = color
			height = hr
			print(color, height, index)
			cv2.putText(image,f'{color} {height}', (xr,yr), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

	# cv2.imshow("images", image)

	x = ("00000" + str(index))[-5:]
	cv2.imwrite(f"data/img{x}.jpg", image)
	distance = get_distance()
	print("Distance", distance)
	# Contingency pLan: If all condition is not detected, this will run
	if distance > 500:
		if prevHeight == "nope":
			try:
				prevHeight = height
			except:
				prevHeight = 0
		if distance < 10:
			stop()
			time.sleep(1)
			backward()
			time.sleep(1)
			stop()
			time.sleep(0.5)
			right()
			stop()
			time.sleep(0.5)
			backward()
			time.sleep(1)
			stop()
			time.sleep(0.5)
			forward()
		# Green
		if colour2 == "Green" and height >= 220 and height != prevHeight:
			if count[0] == "Green":
				print("runs")
				prevHeight = height
				count[1] += 1
				if count[1] >= 6:
					print("turning")
					stop()
					time.sleep(1)
					backward()
					time.sleep(0.5)
					left()
					stop()
					time.sleep(0.4)
					forward()
					time.sleep(1)
					stop()
					time.sleep(0.4)
					right()
					forward()
					time.sleep(2)
					right()
					forward()
					time.sleep(1)
					left()
					forward()
					count[1] = 0
			else:
				count[0] = "Green"
				count[1] = 0
		elif colour2 == "Red" and height >= 220 and height != prevHeight:
			if count[0] == "Red":
				prevHeight = height
				count[1] += 1
				print("hi")
				if count[1] >= 6:
					print("turning")
					stop()
					time.sleep(1)
					backward()
					time.sleep(0.5)
					right()
					stop()
					time.sleep(0.4)
					forward()
					time.sleep(1)
					stop()
					time.sleep(0.4)
					left()
					forward()
					time.sleep(2)
					left()
					forward()
					time.sleep(1)
					right()
					forward()
					count[1] = 0
			else:
				count[0] = "Red"
				count[1] = 0
		print(count)
	else:
		# if distance <= 40:
		# 	stop()
		# 	time.sleep(1)
		# 	backward()
		# 	time.sleep(1)
		# 	right()
		# 	forward()
		time.sleep(1.7)
		right()
		forward()
		time.sleep(7.5)
		break







	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

	index += 1

cv2.destroyAllWindows()
cap.release()

vid_capture = cv2.VideoCapture('data/img%05d.jpg')