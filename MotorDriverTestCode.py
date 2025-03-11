from time import sleep
import RPi.GPIO as GPIO

#GPIO Set Up#
GPIO.setmode(GPIO.BCM)  #BCM uses the GPIO numbering on pinouts, not the actual pin number sometimes printed on boards.
# Motor 1 (M1)
M1enL = 5  # Set pins to where they are wired. Can change this value here instead of everywhere it is referenced.
M1enR = 6
M1pwmL = 12
M1pwmR = 13
# Motor 2 (M2)
M2enL = 26
M2enR = 16
M2pwmL = 18
M2pwmR = 19
# Motor 1 (M1)
GPIO.setup(M1enL,GPIO.OUT)  # Setting those pins as output pins so the board knows to output signal there.
GPIO.setup(M1enR,GPIO.OUT)
GPIO.setup(M1pwmL,GPIO.OUT)
GPIO.setup(M1pwmR,GPIO.OUT)
# Motor 2 (M2)
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

def driveLeft(speed):   #I'm not actually sure if this is left so might need to change the name once we test on Sue.
    GPIO.output(M1enL,GPIO.HIGH)
    GPIO.output(M1enR,GPIO.HIGH)
    GPIO.output(M2enL,GPIO.HIGH)
    GPIO.output(M2enR,GPIO.HIGH)
    M1pwmL.start(speed)  #starts at a speed of whatever % int you call the function with.
    M2pwmL.start(speed)
    print(f"Going Left at {speed}% speed")

def driveRight(speed): #I'm not actually sure if this is Right so might need to change the name once we test on Sue.
    GPIO.output(M1enL,GPIO.HIGH)
    GPIO.output(M1enR,GPIO.HIGH)
    GPIO.output(M2enL,GPIO.HIGH)
    GPIO.output(M2enR,GPIO.HIGH)
    M1pwmR.start(speed)   #starts at a speed of whatever % int you call the function with.
    M2pwmR.start(speed)
    print(f"Going Right at {speed}% speed")

def driveStop():
    M1pwmL.stop()
    M1pwmR.stop()
    M2pwmL.stop()
    M2pwmR.stop()
    print("Stopped")

try:
    print("Starting test.")

    driveLeft(70)
    sleep(3)
    driveStop()
    sleep(2)
    driveRight(70)
    sleep(3)
    driveStop()

    print("Test Complete.")
    GPIO.cleanup()
except KeyboardInterrupt:
    print("Keyboard Interrupt")
    GPIO.cleanup()
