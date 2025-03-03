# New Version Of Sue Code

import time
import RPi.GPIO as GPIO
import board
#import adafruit_tca9548a
#import adafruit_vl53l0x
#import adafruit_apds9960.apds9960
from gpiozero import Button, DistanceSensor
from Raspi_MotorHAT_master import Raspi_MotorHAT, Raspi_DCMotor

####### NEEDS VALUE CHECKED FOR PINS #######

#GPIO Set Up#
GPIO.setmode(GPIO.BCM)

leftBack = Button(1) ######
rightBack = Button(2)  #######
leftSide = Button(3) ######
rightSide = Button(4) #####

lineSensor = 1		#####		#TRCT5000 is the sensor I think we should use.
GPIO.setup(lineSensor, GPIO.IN)

ballLeft = DistanceSensor(echo=17, trigger=4, threshold_distance=0.127) ######
ballRight = DistanceSensor(echo=17, trigger=4, threshold_distance=0.127)  ######
ballCenter = DistanceSensor(echo=17, trigger=4, threshold_distance=0.127) ######
startButton = Button(5) #######
testButton = Button(6) #######

def Test_Driver_Motors():
	leftDriver = mh.getMotor(1)
	rightDriver = mh.getMotor(2)
	print("Motors Set Up")
	#set speed
	leftDriver.setSpeed(100)
	rightDriver.setSpeed(100)
	print("Speed Set")
	#run test
	leftDriver.run(Raspi_MotorHAT.FORWARD)
	rightDriver.run(Raspi_MotorHAT.FORWARD)
	print("Moving Forward")
	#turn off
	leftDriver.run(Raspi_MotorHAT.RELEASE)
	rightDriver.run(Raspi_MotorHAT.RELEASE)
	print("Test Complete")
	
def Drive_Left():
	print("Going Left")
	# open left ramp
	leftDriver.run(Raspi_MotorHAT.FORWARD)
	rightDriver.run(Raspi_MotorHAT.FORWARD)
	leftSide.when_pressed	
	
def Drive_Right():
	print("Going Right")
	leftDriver.run(Raspi_MotorHAT.BACKWARD)
	rightDriver.run(Raspi_MotorHAT.BACKWARD)
	
def Drive_Stop():
	print("Stopped")
	leftDriver.run(Raspi_MotorHAT.RELEASE)
	rightDriver.run(Raspi_MotorHAT.RELEASE)

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
	leftDriver.run(Raspi_MotorHAT.FORWARD)
	rightDriver.run(Raspi_MotorHAT.FORWARD)
	leftSide.when_pressed = Drive_Stop()
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
	leftDriver.run(Raspi_MotorHAT.BACKWARD)
	rightDriver.run(Raspi_MotorHAT.BACKWARD)
	rightSide.when_pressed = Drive_Stop()
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
				
def Aiming():
	global onCenter, status
	if lastWall == "right":
		while True:
			if GPIO.input(lineSensor):	#not on line
				leftDriver.run(Raspi_MotorHAT.FORWARD)
				rightDriver.run(Raspi_MotorHAT.FORWARD)
			else:
				leftDriver.run(Raspi_MotorHAT.RELEASE)
				rightDriver.run(Raspi_MotorHAT.RELEASE)
				onCenter = True
				Take_Shot()			#need to write for now just have motor run continuous?
				status = pickup
				break
	elif lastWall == "left":
		while True:
			if GPIO.input(lineSensor):	#not on line
				leftDriver.run(Raspi_MotorHAT.BACKWARD)
				rightDriver.run(Raspi_MotorHAT.BACKWARD)
			else:
				leftDriver.run(Raspi_MotorHAT.RELEASE)
				rightDriver.run(Raspi_MotorHAT.RELEASE)
				onCenter = True
				Take_Shot()			#need to write for now just have motor run continuous?
				status = pickup
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
testButton.when_pressed = testDriverMotors()	#need to add test line sensors to test script.
startButton.when_pressed  = Start_Button()

while status != "ready":		# should run until startbutton is pressed again
	onCenter = On_Center()
	Balls()
	#shut ramps
	while status == "pickup":	# pickup sequence
		Left_Load()		# if we want it to go right first then this should be changed to Right_load()
		
	
	while status == "shooting":	# have balls going to shoot
		Aiming()
	
