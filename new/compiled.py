

# https://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/
# https://techvidvan.com/tutorials/detect-objects-of-similar-color-using-opencv-in-python/

import numpy as np
import cv2
import RPi.GPIO as GPIO          
import time
# import serial

# ser = serial.Serial("/dev/ttyACM0", 115200, timeout=1)

#Set-up
image = cv2.imread("./test.png")

boundaries = [
  ([0,50,50], [15,255,255], "Red"), # red
  ([35,50,50], [75,255,255], "Green"), # green
]

cap = cv2.VideoCapture(0)

in1 = 24
in2 = 23
in3 = 17
in4 = 27
en2 = 22
en1 = 25
temp1=1

TRIG = 23
ECHO = 24

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
p=GPIO.PWM(en1,1000)
p2=GPIO.PWM(en2,1000)



GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.OUT)

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

p.start(25)
p2.start(22)
p.ChangeDutyCycle(75)
p2.ChangeDutyCycle(75)

TRIG = 23
ECHO = 24

def forward():
  GPIO.output(in1,GPIO.HIGH)
  GPIO.output(in2,GPIO.LOW)
  GPIO.output(in3,GPIO.HIGH)
  GPIO.output(in4,GPIO.LOW)
# hi
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

def left():
  GPIO.output(in1,GPIO.LOW)
  GPIO.output(in2,GPIO.HIGH)
  GPIO.output(in3,GPIO.HIGH)
  GPIO.output(in4,GPIO.LOW)

forward()
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
    #   x,y,w,h = cv2.boundingRect(c)
    #   cv2.putText(output, str(w), (x,y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
    #   cv2.rectangle(output, (x, y), (x + w, y + h), (36,255,12), 1)

    if len(contours)>0:
      # print(contours)
      area = max(contours, key=cv2.contourArea)
      # if cv2.contourArea(red_area) < 50: break
      max_countours.append(area)

  if len(max_countours) > 0:
    area = max(max_countours, key=cv2.contourArea)
    (xr,yr,wr,hr) = cv2.boundingRect(area)
    cv2.rectangle(image, (xr,yr),(xr+wr, yr+hr),(255,255,255),2)
    print(area)
    print(max_countours.index(area))
    print(max_countours)
    cv2.putText(image,f'{boundaries[max_countours.index(area)][2]} {hr}', (xr,yr), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

  # dist = get_distance()
  if area <= 100:
    right()
  elif area >= 200:
    if boundaries[max_countours.index(area)][2] == "Green":
      left()
    




  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cv2.destroyAllWindows()
cap.release()
