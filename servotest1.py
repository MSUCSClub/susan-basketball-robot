import time
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)


kit.servo[0].angle = 100
time.sleep(1)
kit.servo[0].angle = 0
