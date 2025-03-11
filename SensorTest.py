# Sensor Test

import time
#import RPi.GPIO as GPIO
import warnings
warnings.simplefilter('ignore')
#import adafruit_hcsr04
from gpiozero import Button, DistanceSensor, LineSensor

####### NEEDS VALUE CHECKED FOR PINS AFTER WIRING #######
#GPIO.setmode(GPIO.BCM)

#lineSensor = LineSensor(27)

#ballLeft = DistanceSensor(echo=23, trigger=24, threshold_distance=0.127)
ballRight = DistanceSensor(echo=22, trigger=10, threshold_distance=0.08)
# ballCenter = DistanceSensor(echo=25, trigger=8, threshold_distance=0.127)

#def Balls():		# Might need to run in main so it can run continuously
#	global leftBall, centerBall, rightBall
# Left Ball
#	ballLeft.wait_for_in_range()
#	leftBall = True
#	print("Left Ball Loaded")
#	ballLeft.wait_for_out_of_range()
#	leftBall = False
#	print("No Left Ball")
# Center Ball
#	ballCenter.wait_for_in_range()
#	centerBall = True
#	print("Center Ball Loaded")
#	ballCenter.wait_for_out_of_range()
#	centerBall = False
#	print("No Center Ball")
# Right Ball
#	ballRight.wait_for_in_range()
#	rightBall = True
#	print("Right Ball Loaded")
#	ballRight.wait_for_out_of_range()
#	rightBall = False
#	print("No Right Ball")

while True:
	ballRight.wait_for_in_range()
	print("Right Ball Loaded")
	ballRight.wait_for_out_of_range()
	print("No Right Ball")
	
