import time
import DriverMotors
from gpiozero import Button

##First Button Press For Test##
# button.wait_for_press()
# print("Button pressed")

# button.wait_for_release() 
# time.sleep(3.5)

test = True

while test is True:
	DriverMotors.testDriverMotors()
	Sensor.testSensors()
	
	test = False

##Second Button Press For Run##
# button.wait_for_press()
# print("Button pressed")

# button.wait_for_release() 
# time.sleep(3.5)

run
