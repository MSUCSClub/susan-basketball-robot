import time
import RPi.GPIO as GPIO
from gpiozero import Button, DistanceSensor, LineSensor

leftSide = Button(4)
rightSide = Button(15)

def Left_Load():
	global onLeft, lastWall
	print("Drive left")
	leftSide.wait_for_press()
	lastWall = "left"
	print(f"On Left Side")
	Right_Load()

def Right_Load():
	global onRight, lastWall
	print("Drive Right")
	rightSide.wait_for_press()
	lastWall = "right"
	print(f"On right Side")
	Left_Load()
	
try:
	while True:
		Left_Load()
except KeyboardInterrupt:
	GPIO.cleanup()
