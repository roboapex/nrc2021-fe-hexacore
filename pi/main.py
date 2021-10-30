import serial
import time
import motor

ser = serial.Serial("/dev/ttyACM0", 115200, timeout=1)

ser.setDTR(False)
time.sleep(1)
ser.flushInput()
ser.setDTR(True)
time.sleep(2)

while True:

  print('Telling the Arduino to start blinking...')
  ser.write(b'1')

  # read to get the acknowledgement from the Arduino
  while True:
    ack = ser.read()
    print(ack)
    if ack == b'A':
      break
  print('Arduino sent back %s' % ack)

  time.sleep(2)

  print('Telling the Arduino to stop blinking...')
  ser.write(b'0')

  # read to get the acknowledgement from the Arduino
  while True:
    ack = ser.read()
    if ack == b'A':
      break
  print('Arduino sent back %s' % ack)

  time.sleep(20)