# New Version Of Sue Code

import time
import RPi.GPIO as GPIO
import board
from gpiozero import Button, DistanceSensor, LineSensor

####### NEEDS VALUE CHECKED FOR PINS AFTER WIRING #######
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
#######################################################
############# Sensor Setup ############################
leftBack = Button(14)
rightBack = Button(15)
leftSide = Button(4)
rightSide = Button(17)

lineSensor = LineSensor(27)

ballLeft = DistanceSensor(echo=23, trigger=24, threshold_distance=0.127)
ballRight = DistanceSensor(echo=22, trigger=10, threshold_distance=0.127)
ballCenter = DistanceSensor(echo=25, trigger=8, threshold_distance=0.127)
startButton = Button(20)
testButton = Button(21)

def Test_Driver_Motors():
	try:
		print("Starting test.")
		Drive_Left(50)
		time.sleep(2)
		Drive_Stop()
		time.sleep(2)
		Drive_Right(75)
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

def Balls():		# Might need to run in main so it can run continuously
	global leftBall, centerBall, rightBall
# Left Ball
	ballLeft.wait_for_in_range()
	leftBall = True
	print("Left Ball Loaded")
	ballLeft.wait_for_out_of_range()
	leftBall = False
	print("No Left Ball")
# Center Ball
	ballCenter.wait_for_in_range()
	centerBall = True
	print("Center Ball Loaded")
	ballCenter.wait_for_out_of_range()
	centerBall = False
	print("No Center Ball")
# Right Ball
	ballRight.wait_for_in_range()
	rightBall = True
	print("Right Ball Loaded")
	ballRight.wait_for_out_of_range()
	rightBall = False
	print("No Right Ball")

def Start_Button():
	global status
	if status == "ready":
		status = "pickup"	# This assumes the first thing we want to do is pickup. If we start with a ball we should change this to "shooting"
		print(status)
	else:
		status = "ready"
		print(status)

def Left_Load():
	global onLeft, lastWall, status
	#open left ramp
	Drive_Left(75)
	leftSide.when_pressed = Drive_Stop()	#This might need to be "wait for press"
	lastWall = "left"
	#shut left ramp MUST MOUNT SWITCH SO THAT RAMP IS NOT TOUCHING THE WALL WHEN IT IS PRESSED!!!
	Balls() # check if balls were loaded
	if centerBall == True:
		status = "shooting"
	else:
		Right_Load()

def Right_Load():
	global onRight, lastWall, status
	#open right ramp
	Drive_Right(75)
	rightSide.when_pressed = Drive_Stop()	#This might need to be "wait for press"
	lastWall = "right"
	#shut right ramp MUST MOUNT SWITCH SO THAT RAMP IS NOT TOUCHING THE WALL WHEN IT IS PRESSED!!!
	Balls() # check if balls were loaded
	if centerBall == True:
		status = "shooting"
	else:
		Left_Load()
	
def On_Center():
	global onCenter
	if GPIO.input(lineSensor) == False: # on line
		onCenter = True
	else:
		onCenter = False
				
def Aiming():	#NEED TO CHANGE WITH NEW DRIVE FUNCTIONS AND LINESENSOR FUNCTIONALITY
	global onCenter, status
	if lastWall == "right":
		while True:
			Drive_Left(25)	# Set to 25 so we are driving slower and can stop faster when she finds the line.
			lineSensor.wait_for_line()
			Drive_Stop()
			if lineSensor.active_state:	#not sure if this will actually work the way I am thinking which is that lineSensor.active_state will return True if it is on a line.
				onCenter = True
				Take_Shot()			#need to write for now just have motor run continuous?
				status = "pickup"
			else:
				Aiming()
			break
	elif lastWall == "left":
		while True:
			Drive_Right(25)
			lineSensor.wait_for_line()
			Drive_Stop()
			if lineSensor.active_state:	# see note above.
				Drive_Stop()
				onCenter = True
				Take_Shot()			#need to write for now just have motor run continuous?
				status = "pickup"
				break
				
def Take_Shot():			### NOT DONE ####
	#spin up flywheels
	#time.sleep(1) #wait for flywheels to get to speed
	#actuate kicker servor
	#Balls()		# check status of balls
		#if centerBall is False and leftBall is True and rightBall is True:	# move and shoot left ball, then move and shoot right ball.
			#actuate left ramp to push left ball into center
			#sleep(0.2)		# wait for ball to move
			#Balls()			# check to make sure it moved
			#if centerBall = True:		#shoot ball
				#sleep(0.2) 	# wait for spinners to get to speed
				# Acuate kicker arm
				#Balls()		# check to make sure it shot.
				#if centerBall = False and rightBall is True:
					#actuate right ramp to push right ball into center
					#sleep(0.2)		# wait for ball to move
					#Balls()			# check to make sure it moved
					#if centerBall = True:		#shoot ball
						#sleep(0.2) 	# wait for spinners to get to speed
						# Acuate kicker arm
						#Balls()		# check to make sure it shot.
						#if centerBall is False:		#all balls should be shot not and break out of shooting process
							#turn off spinner relay
		#elif centerBall is False and leftBall is True and rightBall is False:
			#actuate left ramp to push left ball into center
			#sleep(0.2)		# wait for ball to move
			#Balls()			# check to make sure it moved
			#if centerBall = True:		#shoot ball
				#sleep(0.2) 	# wait for spinners to get to speed
				# Acuate kicker arm
				#Balls()		# check to make sure it shot.
				#if centerBall is False:		#all balls should be shot not and break out of shooting process
							#turn off spinner relay
		#elif centerBall = False and rightBall is True and leftBall is False:
			#actuate right ramp to push right ball into center
					#sleep(0.2)		# wait for ball to move
					#Balls()			# check to make sure it moved
					#if centerBall = True:		#shoot ball
						#sleep(0.2) 	# wait for spinners to get to speed
						# Acuate kicker arm
						#Balls()		# check to make sure it shot.
						#if centerBall is False:		#all balls should be shot not and break out of shooting process
							#turn off spinner relay
		#elif centerBall = False and rightBall is False and leftBall is False:
			#turn off spinner relay
	print("not done")
	
	
########## Start Of Main Loop ###########	
			
# Global Variables
status = "ready"
onLeft = False
onRight = False
lastWall = ""		#changing this should change what direction the bot goes first. Left means bot goes right and vis versa
ballInLeft = False
ballInRight = False
ballInCenter = False	# this assumes we do not start with a ball in the bot. I think we should start with all 3 bals on one side so we can pick them up in one move.
onCenter = False	#Even if we do start with it lined up in the middle this value should be changed in test so we can make sure the line sensors are working.

#Test/Start Buttons
testButton.when_pressed = Test_Driver_Motors()	#need to add test line sensors to test script.
startButton.when_pressed  = Start_Button()

while status != "ready":		# should run until startbutton is pressed again
	onCenter = On_Center()
	Balls()
	#shut ramps
	while status == "pickup":	# pickup sequence
		Left_Load()		# if we want it to go right first then this should be changed to Right_load()
		
	
	while status == "shooting":	# have balls going to shoot
		Aiming()
	
