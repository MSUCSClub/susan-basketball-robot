# New Version Of Sue Code

import time
import RPi.GPIO as GPIO
from gpiozero import Button, DistanceSensor, LineSensor

####### NEEDS VALUE CHECKED FOR PINS AFTER WIRING #######
GPIO.setmode(GPIO.BCM)
######## DRIVE MOTOR SET UP ##########
# Drive Motor 1 (M1)
M1enL = 5  # Set pins to where they are wired. Can change this value here instead of everywhere it is referenced.
M1enR = 6
M1pwmL = 12
M1pwmR = 13
# Drive Motor 2 (M2)
M2enL = 26
M2enR = 16
M2pwmL = 18
M2pwmR = 19
# Drive Motor 1 (M1)
GPIO.setup(M1enL,GPIO.OUT)  # Setting those pins as output pins so the board knows to output signal there.
GPIO.setup(M1enR,GPIO.OUT)
GPIO.setup(M1pwmL,GPIO.OUT)
GPIO.setup(M1pwmR,GPIO.OUT)
# Drive Motor 2 (M2)
GPIO.setup(M2enL,GPIO.OUT)
GPIO.setup(M2enR,GPIO.OUT)
GPIO.setup(M2pwmL,GPIO.OUT)
GPIO.setup(M2pwmR,GPIO.OUT)
# Set up the PWM pins so the board will send PWM signals.
M1pwmL = GPIO.PWM(M1pwmL,1000)  #1000 is the Hz frequency. We can maybe play with this value to change the motor speed.
M1pwmR = GPIO.PWM(M1pwmR,1000)
M2pwmL = GPIO.PWM(M2pwmL,1000)
M2pwmR = GPIO.PWM(M2pwmR,1000)  #NOTES ON CONTROLLING MOTORS WITH PWM SIGNALS
                                    #pwmL.start(100) will start the motor spinning left at 100% speed
                                    #pwmL.stop() will stop the motor
                                    #pwmL.ChangeDutyCycle(50) will set the speed of the motor to 50%
                                    
############## Servo Setup ############################
#Need to figure out what that angle is for servo functions. Assuming 0 for down, 90 for closed. 130 for pushing ball over.
down = 0
closed = 90
push = 130
#rightRamp = servo.Servo(pca.channels[0])
#leftRamp = servo.Servo(pca.channels[7])
#kickServo = servo.Servo(pca.channels[15])
#######################################################
############# Sensor Setup ############################
#leftBack = Button(14)
#rightBack = Button(15)
leftSide = Button(4)
rightSide = Button(17)

lineSensor = LineSensor(27)

#ballLeft = DistanceSensor(echo=23, trigger=24, threshold_distance=0.127)
#ballRight = DistanceSensor(echo=22, trigger=10, threshold_distance=0.127)
#ballCenter = DistanceSensor(echo=25, trigger=8, threshold_distance=0.127)
#startButton = Button(20)
#testButton = Button(21)

def Test_Driver_Motors():
	try:
		print("Starting test.")
		Drive_Left(20)
		time.sleep(2)
		Drive_Stop()
		time.sleep(2)
		Drive_Right(30)
		time.sleep(2)
		Drive_Stop()

		print("Test Complete.")

	except KeyboardInterrupt:
		print("Keyboard Interrupt")
		GPIO.cleanup()
	
def Drive_Left(speed):
	GPIO.output(M1enL, GPIO.HIGH)
	GPIO.output(M1enR, GPIO.HIGH)
	GPIO.output(M2enL, GPIO.HIGH)
	GPIO.output(M2enR, GPIO.HIGH)
	M1pwmL.start(speed)  # starts at a speed of whatever % int you call the function with.
	M2pwmL.start(speed)
	print(f"Going Left at {speed}% speed")
	
def Drive_Right(speed):
	GPIO.output(M1enL, GPIO.HIGH)
	GPIO.output(M1enR, GPIO.HIGH)
	GPIO.output(M2enL, GPIO.HIGH)
	GPIO.output(M2enR, GPIO.HIGH)
	M1pwmR.start(speed)  # starts at a speed of whatever % int you call the function with.
	M2pwmR.start(speed)
	print(f"Going Right at {speed}% speed")
	
def Drive_Stop():
	M1pwmL.stop()
	M1pwmR.stop()
	M2pwmL.stop()
	M2pwmR.stop()
	print("Stopped")
	
def Left_Load():
	global onLeft, lastWall, status, count
	count = count+1
	Drive_Left(50)
	leftSide.wait_for_press()
	Drive_Stop()
	lastWall = "left"
	print(lastWall)
	return

def Right_Load():
	global onRight, lastWall, status, count
	count = count+1
	Drive_Right(50)
	rightSide.wait_for_press()
	lastWall = "right"
	print(lastWall)
	if count <3:
		Left_Load()
	else:
		return

try:
	while True:
		key = input("Press l to start left load press r to start right load:")
		if key == "l":
			Drive_Left(35)
			leftSide.wait_for_press()
			Drive_Stop()
			lastWall = "Left"
			print(f"The last wall was {lastWall}")
		elif key == "r":
			Drive_Right(35)
			rightSide.wait_for_press()
			lastWall = "Right"
			Drive_Stop()
			print(f"The last wall was {lastWall}")
except KeyboardInterrupt:
	GPIO.cleanup()
