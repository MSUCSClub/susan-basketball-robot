from Raspi_MotorHAT_master import Raspi_MotorHAT, Raspi_DCMotor
import time
import atexit

########################################################################
# Speed is int from 0 to 255.
########################################################################

# Initialize Motor Hat
mh = Raspi_MotorHAT(addr=0x6f)

# Turns motors off at shutdown
def turnOffMotors():
	mh.getMotor(1).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(3).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(4).run(Raspi_MotorHAT.RELEASE)
	
atexit.register(turnOffMotors)

# Motor initialize and test
def testDriverMotors():
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

def driveLeft():
	print("Going Left")
	leftDriver.run(Raspi_MotorHAT.FORWARD)
	rightDriver.run(Raspi_MotorHAT.FORWARD)
	
def driveRight():
	print("Going Right")
	leftDriver.run(Raspi_MotorHAT.BACKWARD)
	rightDriver.run(Raspi_MotorHAT.BACKWARD)
	
def driveStop():
	print("Stopped")
	leftDriver.run(Raspi_MotorHAT.RELEASE)
	rightDriver.run(Raspi_MotorHAT.RELEASE)


